import cv2 as cv
import numpy as np
import time
from PIL import Image
start = time.time()
np.seterr(divide='ignore', invalid='ignore')

def segment_image_into_3x3(image):
    width, height = image.size
    # print("width:",width)
    # print("height:",height)
    seg_width = width // 3
    seg_height = height // 3
    # print("width:",seg_width)
    # print("height:",seg_height)
    # print(seg_height,"X",seg_width)
    segments = []
    for i in range(3):
        for j in range(3):
            left = i * seg_width
            upper = j * seg_height
            right = (i + 1) * seg_width if (i != 2) else width
            lower = (j + 1) * seg_height if (j != 2) else height
            segments.append(image.crop((left, upper, right, lower)))
    return segments

def rgb_to_hsv(image):
    # Normalize the RGB values
    image = image/255
    R, G, B = image[..., 0], image[..., 1], image[..., 2]
    Cmax = np.max(image, axis=-1)
    Cmin = np.min(image, axis=-1)
    delta = Cmax - Cmin

    H = np.zeros_like(Cmax)
    mask = delta > 0
    idx_r = (Cmax == R) & mask
    idx_g = (Cmax == G) & mask
    idx_b = (Cmax == B) & mask

    # To avoid dimensionality issues, we perform the operations only where the mask is True
    H[idx_r] = ((G[idx_r] - B[idx_r]) / delta[idx_r]) % 6
    H[idx_g] = ((B[idx_g] - R[idx_g]) / delta[idx_g]) + 2
    H[idx_b] = ((R[idx_b] - G[idx_b]) / delta[idx_b]) + 4
    H = (H * 60) % 360  # Convert to degrees
    
    S = np.where(Cmax == 0, 0, delta / Cmax)
    V = Cmax
    return np.stack((H, S, V), axis=-1)

def vector(image):
    image = image.convert('RGB')
    image = np.array(image)
    HSVNumpy = rgb_to_hsv(image)
    # Hbin = np.array([(20, 40), (40, 75), (75, 155), (155, 190), (190, 270), (270, 295), (295, 315),(0,20),(315,360)])
    Hbin = np.array([(316, 360), (1, 26), (26, 41), (41, 121), (121, 191), (191, 271), (271, 295),(295,316)])
    Sbin = np.array([(0, 0.2), (0.2, 0.7), (0.7, 1.1)])
    Vbin = np.array([(0, 0.2), (0.2, 0.7), (0.7, 1.1)])
    histogram = np.zeros((len(Hbin), len(Sbin), len(Vbin)), dtype='int64')

    # Create masks for each bin
    # h_masks = [(Hbin[i][0] <= HSVNumpy[:, :, 0]) & (HSVNumpy[:, :, 0] < Hbin[i][1]) for i in range(len(Hbin))]
    h_masks = [((Hbin[i][0] <= HSVNumpy[:, :, 0]) & (HSVNumpy[:, :, 0] < Hbin[i][1])) | (HSVNumpy[:, :, 0] == 0) if i == 0 else (Hbin[i][0] <= HSVNumpy[:, :, 0]) & (HSVNumpy[:, :, 0] < Hbin[i][1]) for i in range(len(Hbin))]
    s_masks = [(Sbin[j][0] <= HSVNumpy[:, :, 1]) & (HSVNumpy[:, :, 1] < Sbin[j][1]) for j in range(len(Sbin))]
    v_masks = [(Vbin[k][0] <= HSVNumpy[:, :, 2]) & (HSVNumpy[:, :, 2] < Vbin[k][1]) for k in range(len(Vbin))]

    # Count pixels for each bin combination
    for i in range(len(Hbin)):
        for j in range(len(Sbin)):
            for k in range(len(Vbin)):
                histogram[i, j, k] = np.sum(h_masks[i] & s_masks[j] & v_masks[k])

    return histogram.flatten()

def manual_dot_product(vec_a, vec_b):
    return np.sum(vec_a * vec_b)

def manual_norm(vec):
    return np.sqrt(np.sum(vec * vec))

def manual_cosine_similarity(vec_a, vec_b):
    dot_product = manual_dot_product(vec_a, vec_b)
    norm_a = manual_norm(vec_a)
    norm_b = manual_norm(vec_b)
    return dot_product / (norm_a * norm_b) if norm_a != 0 and norm_b != 0 else 0
#Masukin vektor kesini buat perbandingan
def calculate_weighted_cosine_similarity(histograms1, histograms2):
    weights = [5 if i == 4 else 3 if i in (3, 5) else 1 for i in range(9)]
    total_similarity = 0

    for i in range(9):
        similarity = manual_cosine_similarity(histograms1[i], histograms2[i])
        weighted_similarity = similarity * weights[i]
        total_similarity += weighted_similarity
    
    print (total_similarity / sum(weights) *100)
    return total_similarity / sum(weights) *100
#Intinya run ini untuk image path buat dapetin vektor
def create_histograms_for_segments(image_path):
    image = Image.open(image_path)
    segments = segment_image_into_3x3(image)
    histograms = [vector(segment) for segment in segments]
    return np.array(histograms)

def cbirColorCompare(img1,img2):
    res=0
    image1 = Image.open(img1)
    image2 = Image.open(img2)
    image1 = image1.convert('RGB')
    image2 = image2.convert('RGB')
    # image1 = image1.crop((0,0,100,200))
    # image2 = image2.crop((0,0,100,200))
    image1segment = segment_image_into_3x3(image1)
    image2segment = segment_image_into_3x3(image2)
    for i in range(9):
        image1segment[i] = np.array(image1segment[i])
        # print(image1segment[i])
        image2segment[i] = np.array(image2segment[i])
        # print(rgb_to_hsv(image1segment[i]))
        # print(rgb_to_hsv(image2segment[i]))
        vector1 = vector(image1segment[i])
        vector2 = vector(image2segment[i])
        # print(vector1)
        # print("=====================================")
        # print(vector2)
        similarity = manual_cosine_similarity(vector1,vector2)
        similarity *= 4 if i == 3 else 2 if i in (1,7) else 1
        # print(similarity)
        res = res+similarity
    print(res/14*100)     
    return(res/14*100)     

# image1 = "img/Harimau1.jpg"
# image2 = "img/Harimau2.jpg"
# # cbirColorCompare(image1,image2)
# vector_result = create_histograms_for_segments(image1)
# vector2_result = create_histograms_for_segments(image2)
# print(calculate_weighted_cosine_similarity(vector_result, vector2_result))
# # image1 = Image.open(image1)
# # image1 = image1.convert('RGB')
# # print(np.array(image1))
# # print(rgb_to_hsv(image2))
# end = time.time()
# print(end-start)
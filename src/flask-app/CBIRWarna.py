import cv2 as cv
import numpy as np
import time
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
    image = np.array(image)
    HSVNumpy = rgb_to_hsv(image)
    Hbin = np.array([(315,20),(20, 40), (40, 75), (75, 155), (155, 190), (190, 270), (270, 295), (295, 315)])
    Sbin = np.array([(0, 0.2), (0.2, 0.7), (0.7, 1)])
    Vbin = np.array([(0, 0.2), (0.2, 0.7), (0.7, 1)])
    histogram = np.zeros((len(Hbin), len(Sbin), len(Vbin)), dtype=int)

    # Create masks for each bin
    h_masks = [(Hbin[i][0] <= HSVNumpy[:, :, 0]) & (HSVNumpy[:, :, 0] < Hbin[i][1]) for i in range(len(Hbin))]
    s_masks = [(Sbin[j][0] <= HSVNumpy[:, :, 1]) & (HSVNumpy[:, :, 1] < Sbin[j][1]) for j in range(len(Sbin))]
    v_masks = [(Vbin[k][0] <= HSVNumpy[:, :, 2]) & (HSVNumpy[:, :, 2] < Vbin[k][1]) for k in range(len(Vbin))]

    # Count pixels for each bin combination
    for i in range(len(Hbin)):
        for j in range(len(Sbin)):
            for k in range(len(Vbin)):
                histogram[i, j, k] = np.sum(h_masks[i] & s_masks[j] & v_masks[k])

    return histogram.flatten()

def cosine_similarity(vec_a, vec_b):
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    return dot_product / (norm_a * norm_b)

def main(img1,img2):
    res=0
    image1 = Image.open(img1)
    image2 = Image.open(img2)
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
        similarity = cosine_similarity(vector1,vector2)
        similarity *= 4 if i == 4 else 2 if i in (1, 7) else 1
        # print(similarity)
        res = res+similarity
    print(res/14*100)
        
# def rgb_of_pixel(image,x,y):
#     r,g,b = image.getpixel((x,y))
#     return r/255,g/255,b/255
# def extract_HSV(R, G, B):
#     Cmax, Cmin = max(R, G, B), min(R, G, B)
#     delta = Cmax - Cmin
#     H = 0 if delta == 0 else (
#         60 * (
#             (G - B) / delta % 6 if Cmax == R else
#             (B - R) / delta + 2 if Cmax == G else
#             (R - G) / delta + 4
#         )
#     )
#     S = 0 if Cmax == 0 else delta / Cmax
#     V = Cmax
#     return [H, S, V]

# def dot_product(v1, v2):
#     return sum(a * b for a, b in zip(v1, v2))

# def magnitude(v):
#     return sum(a * a for a in v) ** 0.5

# def cosine_similarity(v1, v2):
#     dot_prod = dot_product(v1, v2)    
#     mag_v1 = magnitude(v1)
#     mag_v2 = magnitude(v2)
#     if mag_v1 == 0 or mag_v2 == 0:
#         return None
#     return dot_prod / (mag_v1 * mag_v2)

# def find_bin_index(value, bins):
#     for i, (start, end) in enumerate(bins):
#         if start <= value < end:
#             return i
#     return -1


# def calculate_histograms_for_blocks(segments):
#     H_bins = [(0, 40), (40, 80), (80, 120), (120, 160), (200, 240), (280, 320), (320, 360)]
#     S_bins = [(0, 0.6), (0.6, 1.3), (1.3, 2)]
#     V_bins = [(0, 0.6), (0.6, 1.3), (1.3, 2)]
#     combinations = [(h, s, v) for h in H_bins for s in S_bins for v in V_bins]
#     histogram = [0] * len(combinations)
#     for y in range(segments.size[1]):
#         for z in range(segments.size[0]): 
#             R,G,B = rgb_of_pixel(segments,z,y)
#             input_H,input_S,input_V = extract_HSV(R,G,B)
#             H_index = find_bin_index(input_H, H_bins)
#             S_index = find_bin_index(input_S, S_bins)
#             V_index = find_bin_index(input_V, V_bins)
#             if H_index != -1 and S_index != -1 and V_index != -1:
#                 combined_index = combinations.index((H_bins[H_index], S_bins[S_index], V_bins[V_index]))
#             else:
#                 combined_index = -1 
#             if combined_index != -1:
#                 histogram[combined_index] += 1
#     return histogram

# def BlockCBIR(img_path,img_path2):
#     similaritytable = []
#     image1 = Image.open(img_path)
#     image2 = Image.open(img_path2)
#     # image1segment = segment_image_into_3x3(image1)
#     # image2segment = segment_image_into_3x3(image2)
#     # for x in range(9):
#     # segment1 = image1segment[x]
#     # segment2 = image2segment[x]
#     # Vector1 = calculate_histograms_for_blocks(segment1)
#     # Vector2 = calculate_histograms_for_blocks(segment2)
#     Vector1 = calculate_histograms_for_blocks(image1)
#     Vector2 = calculate_histograms_for_blocks(image2)
#     similarity = cosine_similarity(Vector1,Vector2)
#     # similarity *= 3 if x == 4 else 2 if x in (1, 7) else 1
#     # similaritytable.append(similarity)
#     # endresult = (sum(similaritytable)/13)*100
#     # print(endresult)
#     # print(similaritytable)
#     print(similarity)
        
    
from PIL import Image
image1 = "src/flask-app/bebek1.jpeg"
image2 = "src/flask-app/bebek2.jpeg"
main(image1,image2)
# # gambar = segment_image_into_3x3(image1);
# # print(calculate_histograms_for_blocks(image1))
# BlockCBIR(image1,image2)
end = time.time()
print(end-start)
# # image1 = Image.open(image1)
# # segment = segment_image_into_3x3(image1)
# # segments = segment[4]
# # segments.show()
import cv2 as cv
import numpy as np
import time
import json
from PIL import Image
import os
start = time.time()
np.seterr(divide='ignore', invalid='ignore')
#Note
#Selama dataset masih sama, panggil aja fungsi writenya
#Cara pakai, setiap fungsi manualcosine dipanggil, akan diappend ke json SESUAI URUTAN SIMILARITY
#Kalau nanti mau caching, ada fungsi read_vectorJSON, itu paling iterate indexnya sesuai panjang dataset yang ada
#Kalau ganti dataset juga ada fungsi clearing
#Aku gatau bisa bikin lambat atau akurasinya pas ga, jadi paling nanti coba di dataset sama buat liat hasilnya sama persis ga, misal persen di
#paginationnya sama ga
def segment_image_into_3x3(image):
    width, height = image.size
    seg_width = width // 3
    seg_height = height // 3
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
    H[idx_r] = ((G[idx_r] - B[idx_r]) / delta[idx_r]) % 6
    H[idx_g] = ((B[idx_g] - R[idx_g]) / delta[idx_g]) + 2
    H[idx_b] = ((R[idx_b] - G[idx_b]) / delta[idx_b]) + 4
    H = (H * 60) % 360  
    S = np.where(Cmax == 0, 0, delta / Cmax)
    V = Cmax
    return np.stack((H, S, V), axis=-1)

def vector(image):
    image = image.convert('RGB')
    image = np.array(image)
    HSVNumpy = rgb_to_hsv(image)
    Hbin = np.array([(316, 360), (1, 26), (26, 41), (41, 121), (121, 191), (191, 271), (271, 295),(295,316)])
    Sbin = np.array([(0, 0.2), (0.2, 0.7), (0.7, 1.1)])
    Vbin = np.array([(0, 0.2), (0.2, 0.7), (0.7, 1.1)])
    histogram = np.zeros((len(Hbin), len(Sbin), len(Vbin)), dtype='int64')
    h_masks = [((Hbin[i][0] <= HSVNumpy[:, :, 0]) & (HSVNumpy[:, :, 0] < Hbin[i][1])) | (HSVNumpy[:, :, 0] == 0) if i == 0 else (Hbin[i][0] <= HSVNumpy[:, :, 0]) & (HSVNumpy[:, :, 0] < Hbin[i][1]) for i in range(len(Hbin))]
    s_masks = [(Sbin[j][0] <= HSVNumpy[:, :, 1]) & (HSVNumpy[:, :, 1] < Sbin[j][1]) for j in range(len(Sbin))]
    v_masks = [(Vbin[k][0] <= HSVNumpy[:, :, 2]) & (HSVNumpy[:, :, 2] < Vbin[k][1]) for k in range(len(Vbin))]
    for i in range(len(Hbin)):
        for j in range(len(Sbin)):
            for k in range(len(Vbin)):
                histogram[i, j, k] = np.sum(h_masks[i] & s_masks[j] & v_masks[k])
    return histogram.flatten()

def manual_dot_product(vec_a, vec_b):
    return np.sum(vec_a * vec_b)

def manual_norm(vec):
    return np.sqrt(np.sum(vec * vec))

def manual_cosine_similarity(hist1, hist2):
    if np.all(hist1 == 0) and np.all(hist2 == 0):
        return 1  
    dot_product = np.dot(hist1, hist2)
    norm_hist1 = np.linalg.norm(hist1)
    norm_hist2 = np.linalg.norm(hist2)
    if norm_hist1 != 0 and norm_hist2 != 0:
        return dot_product / (norm_hist1 * norm_hist2)
    else:
        return 0
    
def calculate_weighted_cosine_similarity(histograms1, histograms2):
    weights = [5 if i == 4 else 3 if i in (3, 5) else 1 for i in range(9)]
    total_similarity = 0
    for i in range(9):
        similarity = manual_cosine_similarity(histograms1[i], histograms2[i])
        similarity = 0 if np.isnan(similarity) else similarity
        weighted_similarity = similarity * weights[i]
        total_similarity += weighted_similarity
    print(total_similarity / sum(weights) *100)
    return total_similarity / sum(weights) *100


def caching(json_file_path, input_histogram):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None
    results = []
    for image_path, image_data in data.items():
        image_vector = np.array(image_data["image_vectors"])
        similarity = calculate_weighted_cosine_similarity(input_histogram, image_vector)
        results.append([image_path,similarity])

    return results

def createHistogram(folder, json_file):
    clear_json(json_file)
    data={}
    for filename in os.listdir(folder):
        image_path = os.path.join(folder, filename)

        if os.path.isfile(image_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            histogram = create_histograms_for_segments(image_path)
            results = {
                "image_path": image_path,
                "image_vectors": numpy_array_to_list(histogram)
            }

            data[image_path] = results
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)


def create_histograms_for_segments(image_path):
    image = Image.open(image_path)
    segments = segment_image_into_3x3(image)
    histograms = [vector(segment) for segment in segments]
    return np.array(histograms)
#Json Function 
def numpy_array_to_list(numpy_array):
    return numpy_array.tolist()
def read_vectorJSON(file_path, index):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        if index < len(data):
            return data[index]['image2_vectors']
        else:
            print("Index out of range.")
            return None
def append_to_json(json_file_path, data):
    # Append data to a JSON file
    try:
        with open(json_file_path, 'r+') as file:
            file_data = json.load(file)
            file_data.append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    except json.JSONDecodeError:
        # If the file is empty, write a new JSON array
        with open(json_file_path, 'w') as file:
            json.dump([data], file, indent=4)
#Pakai ini kalau dataset beda, jadi jsonnya di clear dulu biar ga overload
def clear_json(file_path):
    with open(file_path, 'w') as json_file:
        json_file.write('[]')
# clear_json('similarity_results.json')
#Testing
# image1 = "Testing_141.jpg"
# image2 = "Testing_142.jpg"
# with open('cache.json', 'r') as file:
#     try:
#         data = json.load(file)
#     except json.JSONDecodeError:
#         data = []
        
# tes = create_histograms_for_segments(image1)
# createHistogram('database','cache.json')
# print(caching('cache.json',tes))
# vector2_result = createHistogram(data,image2)

# Just in case mau panggil ulang, tinggal np.array dari fungsi si read_vectorJSON)
# vector2_result = np.array(read_vectorJSON('similarity_results.json',0))
# similarity = calculate_weighted_cosine_similarity(vector_result,vector2_result)
# print(calculate_weighted_cosine_similarity(vector_result, vector2_result))


end = time.time()
print(end-start)
#Tulis hasil ke json
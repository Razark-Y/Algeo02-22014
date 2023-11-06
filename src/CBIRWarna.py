import cv2 as cv
import numpy as np
def rgb_of_pixel(image,x,y):
    r,g,b = image.getpixel((x,y))
    return r/255,g/255,b/255
def extract_HSV(R, G, B):
    Cmax = max(R,G,B)
    Cmin = min(R,G,B)
    delta = Cmax - Cmin
    if delta == 0:
        H = 0
    elif Cmax == R:
        H = 60 * (((G - B) / delta) % 6)
    elif Cmax == G:
        H = 60 * (((B - R) / delta) + 2)
    elif Cmax == B:
        H = 60 * (((R - G) / delta) + 4)
    S = 0 if Cmax == 0 else delta / Cmax
    V = Cmax
    return [H,S,V]

def dot_product(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))

def magnitude(v):
    return sum(a * a for a in v) ** 0.5

def cosine_similarity(v1, v2):
    dot_prod = dot_product(v1, v2)
    mag_v1 = magnitude(v1)
    mag_v2 = magnitude(v2)
    if mag_v1 == 0 or mag_v2 == 0:
        return None
    return dot_prod / (mag_v1 * mag_v2)


def segment_image_into_3x3(image):
    width, height = image.size
    # print("width:",width)
    # print("height:",height)
    seg_width = width // 3
    seg_height = height // 3
    # print("width:",seg_width)
    # print("height:",seg_height)
    segments = []
    for i in range(3):
        for j in range(3):
            left = i * seg_width
            upper = j * seg_height
            right = (i + 1) * seg_width if (i != 2) else width
            lower = (j + 1) * seg_height if (j != 2) else height
            segments.append(image.crop((left, upper, right, lower)))
    return segments

def calculate_histograms_for_blocks(segments):
    H = 0;
    S = 0;
    count = 0;
    V = 0;
    #segments = list of image
    Hue_Range= [(0,20),(20,40),(40,75),(75,155),(155,190),(190,270),(270,295),(295,315),(315,360)]
    Saturation_Range = [(0,0.2),(0.2,0.7),(0.7,1)]
    Value_Range = [(0,0.2),(0.2,0.7),(0.7,1)]
    hue_histogram = [0] * 9
    saturation_histogram = [0] * 3
    value_histogram = [0] * 3
    # print(segments.size[0])
    for y in range(segments.size[1]):
        for z in range(segments.size[0]):
            R,G,B = rgb_of_pixel(segments,z,y)
            H,S,V = extract_HSV(R,G,B)
            for i,(low,high) in enumerate(Hue_Range):
                if low<H<=high:
                    hue_histogram[i] += 1
            for i,(low,high) in enumerate(Saturation_Range):
                if low<H<=high:
                    saturation_histogram[i] += 1
            for i,(low,high) in enumerate(Value_Range):
                if low<H<=high:
                    value_histogram[i] += 1
    feature_vector = hue_histogram + saturation_histogram + value_histogram 
    return feature_vector


def BlockCBIR(img_path,img_path2):
    similaritytable = []
    image1 = Image.open(img_path)
    image2 = Image.open(img_path2)
    image1segment = segment_image_into_3x3(image1)
    image2segment = segment_image_into_3x3(image2)
    for x in range(9):
        segment1 = image1segment[x]
        segment2 = image2segment[x]
        Vector1 = calculate_histograms_for_blocks(segment1)
        Vector2 = calculate_histograms_for_blocks(segment2)
        similarity = cosine_similarity(Vector1,Vector2)
        similarity *= 3 if x == 4 else 2 if x in (1, 7) else 1
        similaritytable.append(similarity)
    endresult = (sum(similaritytable)/13)*100
    print(endresult)
    # print(similaritytable)
        
    
from PIL import Image
image1 = "apple03_0.jpg"
image2 = "apple03_0.jpg"

BlockCBIR(image1,image2)
# image1 = Image.open(image1)
# segment = segment_image_into_3x3(image1)
# segments = segment[4]
# segments.show()
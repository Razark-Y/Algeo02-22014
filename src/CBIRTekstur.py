import cv2 as cv
import numpy as np
from PIL import Image
import math as MATH

def RGBtoGrayscale(r, g, b) :
    return round(0.2989*r + 0.587*g + 0.114*b)

def RGBImagetoGrayscale(img) :
    height, width = img.size
    res = [[] for i in range(height)]
    for i in range(height) :
        for j in range(width) :
            r, g, b = img.getpixel((i, j))
            res[i].append(RGBtoGrayscale(r, g, b))
    return res

def constructCoOccurenceMatrix(img) :
    GrayscaleMatrix = RGBImagetoGrayscale(img)
    res = [[0 for i in range(256)] for i in range(256)]
    for i in range(len(GrayscaleMatrix) - 1) :
        for j in range(len(GrayscaleMatrix[0])) :
            res[round(GrayscaleMatrix[i][j])][round(GrayscaleMatrix[i + 1][j])] += 1
    return res

# def constructCoOccurenceMatrix(img) :
#     GrayscaleMatrix = RGBImagetoGrayscale(img)
#     res = [[0 for i in range(4)] for i in range(4)]
#     for i in range(len(GrayscaleMatrix) - 1) :
#         for j in range(len(GrayscaleMatrix[0])) :
#             res[round((GrayscaleMatrix[i][j])/85)][round((GrayscaleMatrix[i + 1][j])/85)] += 1
#     return res

def constructNormalizedOccMatrix(img) :
    basicOcc = constructCoOccurenceMatrix(img)
    res = [[0 for i in range(256)] for i in range(256)]
    sum = 0
    for i in range(256) :
        for j in range(256) :
            res[i][j] = basicOcc[i][j] + basicOcc[j][i]
            sum += basicOcc[i][j] + basicOcc[j][i]

    for i in range(256) :
        for j in range(256) :
            res[i][j] /= sum
    return res

# def constructNormalizedOccMatrix(img) :
#     basicOcc = constructCoOccurenceMatrix(img)
#     res = [[0 for i in range(4)] for i in range(4)]
#     sum = 0
#     for i in range(4) :
#         for j in range(4) :
#             res[i][j] = basicOcc[i][j] + basicOcc[j][i]
#             sum += basicOcc[i][j] + basicOcc[j][i]

#     for i in range(4) :
#         for j in range(4) :
#             res[i][j] /= sum
#     return res

def getContHomEnt(img) :
    occ = constructNormalizedOccMatrix(img)
    con = 0.0
    hom = 0.0
    ent = 0
    for i in range(256) :
        for j in range(256) :
            el = occ[j][i]
            con += el*((i - j)**2)
            hom += el/(1 + ((i-j)**2))
            if (el != 0) :
                ent += el * -MATH.log(el, 2)
    return (con, hom, ent)

# def getContHomEnt(img) :
#     occ = constructNormalizedOccMatrix(img)
#     con = 0.0
#     hom = 0.0
#     ent = 0.0
#     for i in range(4) :
#         for j in range(4) :
#             el = occ[i][j]
#             con += el*((i - j)**2)
#             hom += el/(1 + ((i-j)**2))
#             if (el != 0) :
#                 ent += -(el * MATH.log(el))
#     return (con, hom, ent)

def cosineSimilarity(v1, v2) :
    length1 = 0
    length2 = 0
    dotProduct = 0

    for i in range(len(v1)) :
        length1 += v1[i]**2
        length2 += v2[i]**2
        dotProduct += v1[i]*v2[i]

    length1 = MATH.sqrt(length1)
    length2 = MATH.sqrt(length2)
    return abs(dotProduct/((length1)*(length2)))

def printMatrix(matrix) :
    for i in matrix :
        for j in i :
            print(j, end=" ")
        print()
    
# img = Image.open("C:/Users/HP/Desktop/test.png").convert('RGB')
# # matrix = constructCoOccurenceMatrix(img)
# matrix = RGBImagetoGrayscale(img)
# printMatrix(matrix)
# newMatrix = constructCoOccurenceMatrix(img)
# printMatrix(newMatrix)
# newMatrix2 = constructNormalizedOccMatrix(img)
# printMatrix(newMatrix2)
# thing = getContHomEnt(img)
# print(thing[0])
# print(thing[1])
# print(thing[2])

# image = Image.open("C:/Users/HP/Desktop/depollock.jpg").convert('RGB')
# occ = constructNormalizedOccMatrix(image)
# che1 = getContHomEnt(image)

# img2 = Image.open("C:/Users/HP/Desktop/rainbowroad.jpg").convert('RGB')
# che2 = getContHomEnt(img2)

# print(che1)
# print(che2)

# print(cosineSimilarity(che1, che2))

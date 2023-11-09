import numpy as np
from PIL import Image
import math as MATH
import time

def RGBtoGrayscale(r, g, b) :
    return np.round(0.2989*r + 0.587*g + 0.114*b)

def RGBImagetoGrayscale(img) :
    height, width = img.size
    res = [[0 for i in range(width)] for i in range(height)]
    for i in range(height) :
        for j in range(width) :
            r, g, b = img.getpixel((i, j))
            res[i][j] += (RGBtoGrayscale(r, g, b))
    return res

def constructCoOccurenceMatrix(img) :
    GrayscaleMatrix = RGBImagetoGrayscale(img)
    res = [[0 for i in range(256)] for i in range(256)]
    for i in range(len(GrayscaleMatrix) - 1) :
        for j in range(len(GrayscaleMatrix[0])) :
            res[round(GrayscaleMatrix[i][j])][round(GrayscaleMatrix[i + 1][j])] += 1
    return res

def constructNormalizedOccMatrix(img) :
    basicOcc = constructCoOccurenceMatrix(img)
    res = [[0 for i in range(256)] for i in range(256)]
    sum = 2 * (img.width - 1) * img.height
    for i in range(256) :
        for j in range(256) :
            res[i][j] = (basicOcc[i][j] + basicOcc[j][i]) / sum
    return res

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

def compareImage(path1, path2) :
    img1 = Image.open(path1).convert('RGB')
    img2 = Image.open(path2).convert('RGB')
    return cosineSimilarity(getContHomEnt(img1), getContHomEnt(img2))
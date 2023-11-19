import os
import subprocess
import time
import numpy as np

def writeCHE(path) :
    subprocess.run(["cHub/getche.exe", path])
    f = open("txt/CHEresult.txt", "r")
    che = (f.read().strip()).split(" ")

    resF = open("txt/CHE.txt", "a")
    resF.write(f'{che[0]} {che[1]} {che[2]} {path}\n')

def initializeDataset() :
    resF = open("txt/CHE.txt", "w")

def processDataset(folder_path) :
    initializeDataset()
    args = ["cHub/initializeDataset.exe"]
    args += [folder_path]
    subprocess.run(args)

def cosineSimilarity(CHE1, CHE2) :
    subprocess.run(["cHub/similarity.exe"] + CHE1 + CHE2)
    f = open("txt/similarity.txt", "r")
    sim = float(f.read())
    return sim

def compareImageWithDataset(path) :
    subprocess.run(["cHub/compdataset.exe", path])
    f = open("txt/comparedWithDataset.txt", "r")
    result = f.read().split("\n")
    result.pop()
    for i in range(len(result)) :
        result[i] = result[i].split(" ")
        result[i][0] = float(result[i][0])
    return result

def normalizeData(arr) :
    similarity = [i[0] for i in arr]
    path = [i[1] for i in arr]
    top = max(similarity)
    bottom = np.quantile(similarity, 0.25)
    finaldata = [100*(i - bottom)/(top - bottom) for i in similarity]
    return sorted([[finaldata[i], path[i]] for i in range(len(arr))], reverse=True)

def compareImage(path1, path2) :
    subprocess.run(["cHub/comp2img.exe", path1, path2])
    f = open("txt/CBIRTextureResult.txt", "r")
    result = float(f.read())
    return result

processDataset("reasonableArt")

# Cara Menggunakan Program dengan Dataset :
# panggil processDataset(folder_path), dengan folder_path adalah path ke folder berisi dataset image
# kemudian hasil perbandingan image dengan dataset dapat didapat dengan menggunakan
# normalizeData(compareImageWithDataset(path_image)) dengan path_image adalah path menuju ke image yang
# ingin dibandingkan dengan dataset,
# hasil dari pemanggilan berupa array berisi pasangan [similarity_value, image_original] yang terurut
# menurun berdasarkan similarity_value
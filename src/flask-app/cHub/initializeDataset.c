#define STB_IMAGE_IMPLEMENTATION
#include "stb-master/stb_image.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <stdio.h>
#include <conio.h>
#include <sys/types.h>
#include <dirent.h>

#define _XOPEN_SOURCE 700

void printInt(int x){
    printf("%d ", x);
}

void printDouble(double x){
    printf("%f ", x);
}

void printMatrix(unsigned char *data, int x, int y){
    int i, j;
    printf("width : %d\n", x);
    printf("height : %d\n", y);
    for(i = 0; i < y; i++){
        for(j = 0; j < x; j++){
            printf("%u ", data[i*x + j]);
        }
        printf("\n");
    }
}

int RGBtoGrayscale(int R, int G, int B){
    return (int)(0.299*(double)R + 0.587*(double)G + 0.114*(double)B);
}

void constructCoOccurenceMatrix(unsigned char* data, int x, int y, unsigned int* result){

    int i, j;

    for(i = 0; i < 256; i++){
        for(j = 0; j < 256; j++){
            result[256*i + j] = 0;
        }
    }

    for(i = 0; i < y; i++){
        for(j = 0; j < x - 1; j++){
            int firstId = RGBtoGrayscale(
                data[3*(i*x + j) + 0],
                data[3*(i*x + j) + 1],
                data[3*(i*x + j) + 2]
            );
            int secondId = RGBtoGrayscale(
                data[3*(i*x + j + 1) + 0],
                data[3*(i*x + j + 1) + 1],
                data[3*(i*x + j + 1) + 2]
            );
            result[256*firstId + secondId] += 1;
        }
    }
}

void constructNormalizedOccMatrix(unsigned char* img, int x, int y, double* result){

    int occMatrix[256*256];
    constructCoOccurenceMatrix(img, x, y, occMatrix);

    double sum = 2 * (x - 1) * y;

    int i, j;
    for(i = 0; i < 256; i++){
        for(j = 0; j < 256; j++){
            result[256*i + j] = (double)(occMatrix[256*i + j] + occMatrix[256*j + i])/sum;
        }
    }
}

void getCHE(unsigned char* img, int x, int y, double* C, double* H, double* E){
    double occMatrix[256*256];
    constructNormalizedOccMatrix(img, x, y, occMatrix);
    int i, j;
    double el;
    *C = (double)0;
    *H = (double)0;
    *E = (double)0;
    for(i = 0; i < 256; i++){
        for(j = 0; j < 256; j++){
            el = occMatrix[256*i + j];
            *C += el*(i - j)*(i - j);
            *H += el/(1 + ((i-j)*(i - j)));
            if (el != 0){
                *E += el * -log2(el);
            }
        }   
    }
}

double cosineSimilarity(double* v1, double* v2, int n){
    double length1 = 0;
    double length2 = 0;
    double dotProduct = 0;

    int i;
    for(i = 0; i < n; i++){
        length1 += v1[i]*v1[i];
        length2 += v2[i]*v2[i];
        dotProduct += v1[i]*v2[i];
    }

    length1 = sqrt(length1);
    length2 = sqrt(length2);
    
    return dotProduct/(length1*length2);
}

double compareImage(char* path1, char* path2){
    int x1, y1, n1;
    int x2, y2, n2;
    unsigned char *data1 = stbi_load(path1, &x1, &y1, &n1, 1);
    unsigned char *data2 = stbi_load(path2, &x2, &y2, &n2, 1);
    double v1[3];
    double v2[3];
    getCHE(data1, x1, y1, &v1[0], &v1[1], &v1[2]);
    getCHE(data2, x2, y2, &v2[0], &v2[1], &v2[2]);
    stbi_image_free(data1);
    stbi_image_free(data2);
    return cosineSimilarity(v1, v2, 3);
}

// int x,y,n;
// unsigned char *data = stbi_load("C:/Users/HP/Desktop/test2.png", &x, &y, &n, 1);
// ... process data if not NULL ...
// ... x = width, y = height, n = # 8-bit components per pixel ...
// ... replace '0' with '1'..'4' to force that many components per pixel
// ... but 'n' will always be the number that it would have been if you said 0

int main(int argc, char *argv[] ){
    FILE *fp;
    char output1[200];

    int x1, y1, n1;
    double v1[3];

    int i;
    fp = fopen("txt/CHE.txt", "w");

    DIR *dp;
    struct dirent *ep;      

    dp = opendir (argv[1]);
    i = 0;
    while ((ep = readdir (dp)) != NULL){
        if (i < 2){
            i++;
        }
        else{
            char* dir = ep -> d_name;
            char theDirectory[300];
            sprintf(theDirectory, "%s/%s", argv[1], dir);

            unsigned char *data1 = stbi_load(theDirectory, &x1, &y1, &n1, 3);
            getCHE(data1, x1, y1, &v1[0], &v1[1], &v1[2]);
            fprintf(fp, "%f %f %f %s\n", v1[0], v1[1], v1[2], dir);
            stbi_image_free(data1);
        }
    }   
    (void) closedir (dp);
    return 0;
}
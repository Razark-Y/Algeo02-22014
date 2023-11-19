#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>

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

int main(int argc, char *argv[] ){
    FILE *fp;
    char* output;

    double v1[3];
    double v2[3];

    v1[0] = atof(argv[1]);
    v1[1] = atof(argv[2]);
    v1[2] = atof(argv[3]);

    v2[0] = atof(argv[4]);
    v2[1] = atof(argv[5]);
    v2[2] = atof(argv[6]);

    double res = cosineSimilarity(v1, v2, 3);

    snprintf(output, 15, "%f", res);
    fp = fopen("txt/similarity.txt", "w");
    fprintf(fp, output);
}
#include "helpers.h"
#include <stdlib.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height ;  i ++)
    {
        //iterates through height of image
        for (int j = 0 ; j < width; j++)
        {
            float aver = round(((float)image[i][j].rgbtBlue + (float)image[i][j].rgbtRed + (float) image[i][j].rgbtGreen) / 3);
            image[i][j].rgbtBlue = (int)aver;
            image[i][j].rgbtRed = (int)aver;
            image[i][j].rgbtGreen = (int)aver;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[width];
    for (int i = 0; i < height ;  i ++)
    {
        //iterates through height of image
        for (int j = 0 ; j < width; j++)
        {
            temp[j] = image[i][j];
        }
        for (int c = 0 ; c < width; c++)
        {
            image[i][width - 1 - c] = temp[c];
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i ++)
    {
        for (int j = 0; j < width; j++)
        {
            int count = 0;
            float avrgb[] = {0, 0, 0};
            int a[3][3] = {{i - 1, i - 1, i - 1}, {i, i, i}, {i + 1, i + 1,i + 1}};
            int b[3][3] = {{j - 1, j, j + 1}, {j - 1, j, j + 1}, {j - 1, j, j + 1}};
            for (int c = 0 ; c < 3; c++)
            {
                for (int d = 0; d < 3 ; d++)
                {
                    if (a[c][d] >= 0 && b[c][d] >= 0 && a[c][d] < height && b[c][d] < width)
                    {
                        avrgb[0] += image[a[c][d]][b[c][d]].rgbtRed;
                        avrgb[1] += image[a[c][d]][b[c][d]].rgbtBlue;
                        avrgb[2] += image[a[c][d]][b[c][d]].rgbtGreen;
                        count++;
                    }
                }
            }
            avrgb[0] /= count;
            avrgb[1] /= count;
            avrgb[2] /= count;

            temp[i][j].rgbtRed = round(avrgb[0]);
            temp[i][j].rgbtBlue = round(avrgb[1]);
            temp[i][j].rgbtGreen = round(avrgb[2]);

        }
    }
    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i ++)
    {
        for (int j = 0; j < width; j++)
        {
            int count = 0;
            int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
            int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
            float totRx = 0, totGx = 0, totBx = 0, totRy = 0, totGy = 0, totBy = 0 ;
            int a[3][3] = {{i - 1, i - 1, i - 1}, {i, i, i}, {i + 1, i + 1, i + 1}};
            int b[3][3] = {{j - 1, j, j + 1}, {j - 1, j, j + 1}, {j - 1, j, j + 1}};
            for (int c = 0 ; c < 3; c++)
            {
                for (int d = 0; d < 3 ; d++)
                {
                    if (a[c][d] >= 0 && b[c][d] >= 0 && a[c][d] < height && b[c][d] < width)
                    {
                        totRx += image[a[c][d]][b[c][d]].rgbtRed * gx[c][d];
                        totGx += image[a[c][d]][b[c][d]].rgbtGreen * gx[c][d];
                        totBx += image[a[c][d]][b[c][d]].rgbtBlue * gx[c][d];
                        totRy += image[a[c][d]][b[c][d]].rgbtRed * gy[c][d];
                        totGy += image[a[c][d]][b[c][d]].rgbtGreen * gy[c][d];
                        totBy += image[a[c][d]][b[c][d]].rgbtBlue * gy[c][d];
                    }
                    else
                    {
                        totRx += 0;
                    }
                }
            }
            float finalR = sqrt(pow(totRx, 2) + pow(totRy, 2));
            if (finalR > 255)
            {
                finalR = 255;
            }
            float finalB = sqrt(pow(totBx, 2) + pow(totBy, 2));
            if (finalB > 255)
            {
                finalB = 255;
            }
            float finalG = sqrt(pow(totGx, 2) + pow(totGy, 2));
            if (finalG > 255)
            {
                finalG = 255;
            }

            temp[i][j].rgbtRed = round(finalR);
            temp[i][j].rgbtBlue = round(finalB);
            temp[i][j].rgbtGreen = round(finalG);
        }
    }

    for (int i = 0 ; i < height ; i++)
    {
        for (int j = 0 ; j < width ; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}

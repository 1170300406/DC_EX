# coding=utf-8
"""
Created on 2020/4/13 14:48
By cfsfine

"""

import numpy as np
import cv2


# 求两张图片的psnr
def psnr(img1, img2):
    mse = np.mean ((img1 / 255. - img2 / 255.) ** 2)
    if mse < 1.0e-10:
        return 100
    PIXEL_MAX = 1
    return 20 * np.math.log10 (PIXEL_MAX / np.math.sqrt (mse))


# dct变换后再反变换，返回psnr值。
# 传入n，取zigzag扫描后前2，3，5，8个系数结果。
# 输入其他数字表示全部系数恢复。
def dct(img, n):
    block_width = 8
    dct_arg = 1
    img_float = img.astype ('float')
    x_block_count = img.shape[0] / block_width
    y_block_count = img.shape[1] / block_width
    idct_img_recor = np.zeros (img.shape)

    if n == 2:
        zag = [[1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    elif n == 3:
        zag = [[1, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    elif n == 5:
        zag = [[1, 1, 0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    elif n == 8:
        zag = [[1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    else:
        zag = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]

    for y_num in range (0, int (y_block_count)):
        for x_num in range (0, int (x_block_count)):
            x_offset = x_num * block_width
            y_offset = y_num * block_width
            block_img = img_float[x_offset:x_offset + block_width, y_offset:y_offset + block_width]

            # dct
            block_img_dct1 = cv2.dct (block_img)
            block_img_dct = np.zeros ([8, 8])
            for i in range (block_width):
                for j in range (block_width):
                    block_img_dct[i][j] = int (block_img_dct1[i][j])

            for i in range (block_width):
                for j in range (block_width):
                    block_img_dct[i][j] *= zag[i][j]

            block_img_idct = cv2.idct (block_img_dct)
            idct_img_recor[x_offset:x_offset + block_width, y_offset:y_offset + block_width] = block_img_idct
    cv2.imwrite ('test1.jpg', idct_img_recor)
    return psnr (img, idct_img_recor)


# dct变换后,量化，再反变换。
# 返回psnr值。k为量化系数。
def dct_quality(img, k):
    block_width = 8
    dct_arg = 1
    img_float = img.astype ('float')
    x_block_count = img.shape[0] / block_width
    y_block_count = img.shape[1] / block_width
    idct_img_recor = np.zeros (img.shape)

    q = [[16, 11, 10, 16, 24, 40, 51, 61], [12, 12, 14, 19, 26, 58, 60, 55],
         [14, 13, 16, 24, 40, 57, 69, 56], [14, 17, 22, 29, 51, 87, 80, 62],
         [18, 22, 37, 56, 68, 109, 103, 77], [24, 35, 55, 64, 81, 104, 113, 92],
         [49, 64, 78, 87, 103, 121, 120, 101], [72, 92, 95, 98, 112, 100, 103, 99]]

    for y_num in range (0, int (y_block_count)):
        for x_num in range (0, int (x_block_count)):
            x_offset = x_num * block_width
            y_offset = y_num * block_width
            block_img = img_float[x_offset:x_offset + block_width, y_offset:y_offset + block_width]
            # dct
            block_img_dct1 = cv2.dct (block_img)
            block_img_dct = np.zeros ([8, 8])
            for i in range (block_width):
                for j in range (block_width):
                    block_img_dct[i][j] = int (block_img_dct1[i][j])
            # 量化
            for i in range (block_width):
                for j in range (block_width):
                    block_img_dct[i][j] = int (block_img_dct[i][j] / (k * q[i][j]))

            # 反量化
            for i in range (block_width):
                for j in range (block_width):
                    block_img_dct[i][j] = int (block_img_dct[i][j] * (k * q[i][j]))

            # idct
            block_img_idct = cv2.idct (block_img_dct)
            idct_img_recor[x_offset:x_offset + block_width, y_offset:y_offset + block_width] = block_img_idct
    cv2.imwrite ('test1.jpg', idct_img_recor)
    return psnr (img, idct_img_recor)


if __name__ == '__main__':
    img = cv2.imread ("test.jpg", 0)
    # 题一
    print (dct (img, 1))
    # 题二
    print (dct (img, 2))
    print (dct (img, 3))
    print (dct (img, 5))
    print (dct (img, 8))
    # 题三
    print (dct_quality (img, 1))
    print (dct_quality (img, 2))
    print (dct_quality (img, 3))
    print (dct_quality (img, 4))
    print (dct_quality (img, 5))
    print (dct_quality (img, 6))
    print (dct_quality (img, 7))
    print (dct_quality (img, 8))
    print (dct_quality (img, 9))
    print (dct_quality (img, 10))

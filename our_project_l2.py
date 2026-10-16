import numpy as np
from random import randint
from PIL import Image
from math import floor, ceil


# изображение по своей сути - интовый беззнаковый восьмибитный массив
# img_mat[y, x] = 255 - постановка точки

img_mat = np.zeros((1000, 1000, 3), dtype=np.uint8)
z_buf = np.full((1000, 1000), np.inf, dtype=np.float32)

def line(img_mat, x0, y0, x1, y1):

    dmax = max(abs(floor(x0) - floor(x1)), abs(floor(y0) - floor(y1)))
    L = dmax + 1
    if L == 1:
        img_mat[floor(y0), floor(x0)] = [147, 197, 114]
        return
    dx = (x1 - x0) / (L - 1)
    dy = (y1 - y0) / (L - 1)
    for _ in range(L):
        img_mat[floor(y0), floor(x0)] = [147, 197, 114]
        x0 += dx
        y0 += dy

def barocent(y, z, y0, z0, y1, z1, y2, z2):
    lambda0 = ((y - y2) * (z1 - z2) - (y1 - y2) * (z - z2)) / ((y0 - y2) * (z1 - z2) - (y1 - y2) * (z0 - z2))
    lambda1 = ((y0 - y2) * (z - z2) - (y - y2) * (z0 - z2)) / ((y0 - y2) * (z1 - z2) - (y1 - y2) * (z0 - z2))
    lambda2 = 1.0 - lambda0 - lambda1
    return lambda0, lambda1, lambda2


def triangle(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    xmin = floor(min(x0, x1, x2))
    ymin = floor(min(y0, y1, y2))
    zmin = floor(min(z0, z1, z2))
    xmax = ceil(max(x0, x1, x2))
    ymax = ceil(max(y0, y1, y2))
    zmax = ceil(max(z0, z1, z2))

    normal = np.cross([x1 - x2, y1 - y2, z1 - z2], [x1 - x0, y1 - y0, z1 - z0])
    l = [0, 0, 1]
    normal_ized = np.dot(normal, l)/(np.linalg.norm(normal) * np.linalg.norm(l))

    if (xmin < 0):
        xmin = 0
    if (ymin < 0):
        ymin = 0
    if (xmax > img_mat.shape[1]):
        xmax = img_mat.shape[1]
    if (ymax > img_mat.shape[0]):
        ymax = img_mat.shape[0]

    if normal_ized < 0:
        color = [-147 * normal_ized, -197 * normal_ized, -114 * normal_ized]
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                lambda0, lambda1, lambda2 = barocent(x, y, x0, y0, x1, y1, x2, y2)
                if (lambda0 >= 0) and (lambda1 >= 0) and (lambda2 >= 0):
                    z = lambda0 * z0 + lambda1 * z1 + lambda2 * z2
                    if (z < z_buf[y,x]):
                        img_mat[y,x] = color
                        z_buf[y, x] = z



v = []
f = []

file = open('cat.obj')

for s in file:
    s_spl = s.split()
    if (s_spl[0] == 'v'):
        v.append([float(i) for i in s_spl[1:4]])
    if (s_spl[0] == 'f'):
        f.append([int(i.split('/')[0]) for i in s_spl[1:4]])

file.close()

'''for i in range(len(v)):
    img_mat[floor(-v[i][1] - 200), floor(v[i][2] + 500)] = [147, 197, 114]'''

for i in f:
    y0 = v[(i[0]) - 1][2] + 500
    z0 = -v[(i[0])-1][1] + 800
    x0 = v[(i[0]) - 1][0] + 300

    y1 = v[(i[1]) - 1][2] + 500
    z1 = -v[(i[1])-1][1] + 800
    x1 = v[(i[1]) - 1][0] + 300

    y2 = v[(i[2]) - 1][2] + 500
    z2 = -v[(i[2])-1][1] + 800
    x2 = v[(i[2]) - 1][0] + 300

    '''line(img_mat, y0, z0, y1, z1)
    line(img_mat, y1, z1, y2, z2)
    line(img_mat, y2, z2, y0, z0)'''

    triangle(y0, z0, x0, y1, z1, x1, y2, z2, x2)



img = Image.fromarray(img_mat)
img.save('img.png')

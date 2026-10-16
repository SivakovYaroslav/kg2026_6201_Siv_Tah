import numpy as np
from PIL import Image
from math import floor

# изображение по своей сути - интовый беззнаковый восьмибитный массив
# img_mat[x, y[ = 255 - постановка точки
# [y, x]

img_mat = np.zeros((1000, 1000, 3), dtype=np.uint8)

def line(img_mat, y0, z0, y1, z1):

    dmax = max(abs(floor(y0) - floor(y1)), abs(floor(z0) - floor(z1)))
    L = dmax + 1
    if L == 1:
        img_mat[floor(z0), floor(y0)] = [147, 197, 114]
        return
    dy = (y1 - y0) / (L - 1)
    dz = (z1 - z0) / (L - 1)
    for _ in range(L):
        img_mat[floor(z0), floor(y0)] = [147, 197, 114]
        y0 += dy
        z0 += dz

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

for i in range(len(v)):
    img_mat[floor(-v[i][1] - 200), floor(v[i][2] + 500)] = [147, 197, 114]

for i in f:
    z0 = -v[(i[0])-1][1] - 200
    y0 = v[(i[0])-1][2] + 500

    z1 = -v[(i[1])-1][1] - 200
    y1 = v[(i[1])-1][2] + 500

    z2 = -v[(i[2])-1][1] - 200
    y2 = v[(i[2])-1][2] + 500

    line(img_mat, y0, z0, y1, z1)
    line(img_mat, y1, z1, y2, z2)
    line(img_mat, y2, z2, y0, z0)

img = Image.fromarray(img_mat)
img.save('img.png')
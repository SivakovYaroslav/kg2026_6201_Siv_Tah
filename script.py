import numpy as np
from PIL import Image
from math import floor

# изображение по своей сути - интовый беззнаковый восьмибитный массив
# img_mat[x, y[ = 255 - постановка точки
# [y, x]

img_mat = np.zeros((1000, 1000, 3), dtype=np.uint8)
x0, y0, x1, y1 = 12.34, 43.21, 123.45, 987.65

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



'''line(img_mat, x0, y0, x1, y1)
img = Image.fromarray(img_mat)
img.save('img.png')'''




v = []
f = []
file = open('model.obj')
for s in file:
    s_spl = s.split()
    if (s_spl[0] == 'v'):
        v.append([float(i) for i in s_spl[1:4]])
    if (s_spl[0] == 'f'):
        f.append([int(i.split('/')[0]) for i in s_spl[1:4]])
file.close()

for i in range(len(v)):
    img_mat[floor(-v[i][1] * 7000 - 200), floor(v[i][0] * 7000 + 500)] = [147, 197, 114]

for i in f:
    y0 = -v[(i[0])-1][1] * 7000 - 200
    x0 = v[(i[0])-1][0] * 7000 + 500

    y1 = -v[(i[1])-1][1] * 7000 - 200
    x1 = v[(i[1])-1][0] * 7000 + 500

    y2 = -v[(i[2])-1][1] * 7000 - 200
    x2 = v[(i[2])-1][0] * 7000 + 500

    line(img_mat, x0, y0, x1, y1)
    line(img_mat, x1, y1, x2, y2)
    line(img_mat, x2, y2, x0, y0)

img = Image.fromarray(img_mat)
img.save('img.png')




'''
for i in range(1000):
    for j in range(1000):
        img_mat[i,j] = (i+j) % 200
img = Image.fromarray(img_mat)
img.save('img.png')
'''
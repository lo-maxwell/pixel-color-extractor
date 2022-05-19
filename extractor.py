# source env/bin/activate
#python3 extracter.py

import cv2
import time
import os
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

pageDir = 'pages'
subDirs = [f for f in os.listdir(pageDir)]

pixels = {}
avgClusteredPixels = {n: 0 for n in range(0, 26)}

for dir in subDirs:
    pages = [os.path.join(pageDir, os.path.join(dir,f)) for f in os.listdir(os.path.join(pageDir, dir)) if f.lower().endswith(('jpg', '.jpeg'))]
    print(pages)
    for p in pages:
        image = Image.open(p, 'r')
        pix_val = list(image.getdata())
        #print(pix_val)
        for pix in pix_val:
            if isinstance(pix, int):
                pix = (pix, pix, pix)
            pixels.setdefault(pix, 0)
            pixels.update({pix: pixels.get(pix) + 1})
            # print("pixel : " + str(pix[0]))
            avgPix = (pix[0] + pix[1] + pix[2])/3
            # print(int(avgPix//10), avgClusteredPixels.get(int(avgPix//10)))
            avgClusteredPixels.update({int(avgPix//10) : avgClusteredPixels.get(int(avgPix//10)) + 1})


sorted_pixels = {key:pixels[key] for key in sorted(pixels.keys())}
sorted_pixels_2 = dict(sorted(sorted_pixels.items(), key=lambda item: item[1], reverse=True))
f = open('stats.txt', 'w')
for i in sorted_pixels_2:
    f.write(str(i) + " : " + str(sorted_pixels_2[i]) + "\n")
f.close()

lists = sorted(sorted_pixels_2.items())[:20]
# plt.plot(x,y)
# plt.show()

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
x_axis = [str("(" + str(key[0]) + ", " + str(key[1]) + ", " + str(key[2]) + ")") for key in sorted_pixels_2][:20]
print(x_axis)
y_axis  = [sorted_pixels_2.get(key) for key in sorted_pixels_2][:20]
print(y_axis)
ax.bar(x_axis,y_axis)
plt.show()

maxDiff = -1000
maxDiffPixel = (-1,-1,-1)
for p in pixels:
    val1, val2, val3 = p[0], p[1], p[2]
    if abs(val1 - val2) > maxDiff or abs(val2 - val3) > maxDiff or abs(val1 - val3) > maxDiff:
        maxDiff = max(abs(val1 - val2), abs(val2 - val3), abs(val1 - val3))
        maxDiffPixel = p
print(maxDiff)
print(maxDiffPixel)

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
x_axis = [key for key in avgClusteredPixels]
print(x_axis)
y_axis = [avgClusteredPixels.get(key) for key in avgClusteredPixels]
print(y_axis)
ax.bar(x_axis,y_axis)
plt.show()

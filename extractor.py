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
fileName = 'non_mainstream'

pixels = {}
avgClusteredPixels_5 = {n: 0 for n in range(0, 52)}
avgClusteredPixels_10 = {n: 0 for n in range(0, 26)}

for dir in subDirs:
    if fileName == 'mainstream' and dir != 'mainstream':
        continue
    if fileName == 'non_mainstream' and dir == 'mainstream':
        continue
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
            avgPix = (pix[0] + pix[1] + pix[2])/3
            avgClusteredPixels_5.update({int(avgPix//5) : avgClusteredPixels_5.get(int(avgPix//5)) + 1})
            avgClusteredPixels_10.update({int(avgPix//10) : avgClusteredPixels_10.get(int(avgPix//10)) + 1})

totalPixels = 0
for key in pixels:
    totalPixels += pixels[key]

sorted_pixels = {key:pixels[key] for key in sorted(pixels.keys())}
sorted_pixels_2 = dict(sorted(sorted_pixels.items(), key=lambda item: item[1], reverse=True))


lists = sorted(sorted_pixels_2.items())[:20]
# plt.plot(x,y)
# plt.show()

#plot of most common pixels
# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])
# x_axis = [str("(" + str(key[0]) + ", " + str(key[1]) + ", " + str(key[2]) + ")") for key in sorted_pixels_2][:20]
# print(x_axis)
# y_axis  = [sorted_pixels_2.get(key) for key in sorted_pixels_2][:20]
# print(y_axis)
# ax.bar(x_axis,y_axis)
# plt.show()

#find largest non gray pixel
# maxDiff = -1000
# maxDiffPixel = (-1,-1,-1)
# for p in pixels:
#     val1, val2, val3 = p[0], p[1], p[2]
#     if abs(val1 - val2) > maxDiff or abs(val2 - val3) > maxDiff or abs(val1 - val3) > maxDiff:
#         maxDiff = max(abs(val1 - val2), abs(val2 - val3), abs(val1 - val3))
#         maxDiffPixel = p
# print(maxDiff)
# print(maxDiffPixel)

#plot of clustered pixels
# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])
# x_axis = [key for key in avgClusteredPixels_5]
# print(x_axis)
# y_axis = [avgClusteredPixels_5.get(key) for key in avgClusteredPixels_5]
# print(y_axis)
# ax.bar(x_axis,y_axis)
# plt.show()

f = open('stats/' + fileName + '.txt', 'w')
for i in sorted_pixels_2:
    f.write(str(i) + " : " + str(sorted_pixels_2[i]) + " : " + str("{:.2f}".format((100.0 * sorted_pixels_2[i])/totalPixels)) + "%\n")
f.close()

f = open('stats/' + fileName + '_cluster_5.txt', 'w')
for i in avgClusteredPixels_5:
    f.write(str(i) + " : " + str(avgClusteredPixels_5[i]) + " : " + str("{:.2f}".format((100.0 * avgClusteredPixels_5[i])/totalPixels)) + "%\n")
f.close()

f = open('stats/' + fileName + '_cluster_10.txt', 'w')
for i in avgClusteredPixels_10:
    f.write(str(i) + " : " + str(avgClusteredPixels_10[i]) + " : " + str("{:.2f}".format((100.0 * avgClusteredPixels_10[i])/totalPixels)) + "%\n")
f.close()

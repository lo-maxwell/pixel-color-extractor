# source env/bin/activate
# python3 extractor.py pageDir fileName plotData cluster
# python3 extractor.py pages cumulative True 5

import cv2
import time
import os
import sys
import numpy as np
import argparse
from matplotlib import pyplot as plt
from PIL import Image

# data: dictionary, numElements: int
def show_plot(data, numElements = -1):
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    if numElements > 0:
        x_axis = [(str("(" + str(key[0]) + ", " + str(key[1]) + ", " + str(key[2]) + ")")) if not isinstance(key, int) else key for key in data][:numElements]
        y_axis  = [data.get(key) for key in data][:numElements]
    else:
        x_axis = [(str("(" + str(key[0]) + ", " + str(key[1]) + ", " + str(key[2]) + ")")) if not isinstance(key, int) else key for key in data]
        y_axis  = [data.get(key) for key in data]
    ax.bar(x_axis,y_axis)
    plt.show()

# fileName: string, data: dictionary, totalPixels: int
def write_stats_file(fileName, data, totalPixels):
    f = open('stats/' + fileName + '.txt', 'w')
    for i in data:
        f.write(str(i) + " : " + str(data[i]) + " : " + str("{:.4f}".format((100.0 * data[i])/totalPixels)) + "%\n")
    f.close()

# myDict: dicitonary, key: int or tuple
def update_dict(myDict, key):
    myDict.setdefault(key, 0)
    myDict.update({key: myDict.get(key) + 1})

def main(args):
    pageDir = args[0] if len(args) > 0 else 'pages'
    fileName = args[1] if len(args) > 1 else 'cumulative'
    plotData = args[2] if len(args) > 2 else True
    cluster = int(args[3]) if len(args) > 3 else 5

    pixels = {}
    avgClusteredPixels = {n: 0 for n in range(0, int(255//cluster))}

    subDirs = [f for f in os.listdir(pageDir)]
    for dir in subDirs:
        #If not in cumulative mode, only search through folder named fileName
        if fileName != 'cumulative' and fileName != dir:
            continue

        #Get list of pages in folder
        pages = [os.path.join(pageDir, os.path.join(dir,f)) for f in os.listdir(os.path.join(pageDir, dir)) if f.lower().endswith(('jpg', '.jpeg'))]
        for p in pages:
            image = Image.open(p, 'r')
            pix_val = list(image.getdata())
            for pix in pix_val:
                if isinstance(pix, int):
                    pix = (pix, pix, pix)
                update_dict(pixels, pix)
                avgPix = (pix[0] + pix[1] + pix[2])/3
                update_dict(avgClusteredPixels, int(avgPix//cluster))

    totalPixels = sum([pixels[key] for key in pixels])

    # sorted_pixels = {key:pixels[key] for key in sorted(pixels.keys())}
    # sorted_pixels_2 = dict(sorted(sorted_pixels.items(), key=lambda item: item[1], reverse=True))
    sorted_pixels = dict(sorted(pixels.items(), key=lambda item: item[1], reverse=True))

    if plotData:
        show_plot(sorted_pixels, 20)
        show_plot(avgClusteredPixels)


    write_stats_file(fileName, sorted_pixels, totalPixels)
    write_stats_file(fileName + '_cluster_' + str(cluster), avgClusteredPixels, totalPixels)



if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Create a pixel extractor')
    # parser.add_argument('--folderName', metavar='path', required=True,
    #                     help='the path to top level directory containing directories of pages')
    # parser.add_argument('--dem', metavar='path', required=True,
    #                     help='path to dem')
    # args = parser.parse_args()
    # main(workspace=args.workspace, schema=args.schema, dem=args.dem)

    main(sys.argv[1:])

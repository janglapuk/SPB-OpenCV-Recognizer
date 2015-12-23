'''
The MIT License (MIT)

Copyright (c) 2015 Thami Rusdi Agus - https://github.com/janglapuk/SPB-OpenCV-Recognizer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import cv2, os, numpy as np
from PIL import Image

def get_cameras(max_cam=3):
    _list = []

    for i in range(0, max_cam):
        tmp_vc = cv2.VideoCapture(i)
        if tmp_vc.isOpened():
            tmp_vc.release()
            _list.append(i)

    return _list


def proportion_resize(baseheight, orig_w, orig_h):
    pct = float(baseheight) / float(orig_h)
    final_w = int(float(orig_w) * pct)
    final_h = baseheight

    #print("Percent: %.02f | Original: %d x %d | Resized: %d x %d" % (pct, orig_w, orig_h, final_w, final_h))
    return (final_w, final_h)


def read_csv(csv_file):
    if not os.path.exists(csv_file):
        print('[read_csv] CSV file does not exists!')
        return

    images, labels = [], []

    with open(csv_file) as f:
        for line in f:
            image, label = line.replace('\n', '').split(';')
            image = Image.open(image)

            images.append(np.asarray(image))
            labels.append(int(label))

    print("[read_csv] Loaded %d images and %d labels" % (len(images), len(labels)))
    return images, labels

def cascade_file(casc_file):
    '''
    Fungsi yang mengembalikan nilai path cascade file
    :param casc_file: nama file cascade dengan ekstensi XML
    :return: string
    '''
    return os.path.join(os.path.dirname(__file__), "res", "haarcascades", casc_file)
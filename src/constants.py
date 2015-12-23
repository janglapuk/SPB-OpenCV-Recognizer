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

import os

APP_NAME = 'SPB Aplikasi Pengenal Wajah dan Pelacak Objek'
APP_VERSION = 'v0.1'

BASE_DIR = os.path.join(os.path.dirname(__file__))
UI_DIR = os.path.join(BASE_DIR, 'ui')
UI_MAIN_FILE = os.path.join(UI_DIR, 'main.ui')
RESOURCE_DIR = os.path.join(BASE_DIR, 'res')
RESOURCE_MASK_DIR = os.path.join(RESOURCE_DIR, 'mask')
DATABASE_DIR = os.path.join(RESOURCE_DIR, 'database')

TRAIN_IMAGE_SIZE = (256, 256)

OT_MAX_BUFFER = 30
OT_GREEN_LOWER = (29, 86, 6)
OT_GREEN_UPPER = (64, 255, 255)
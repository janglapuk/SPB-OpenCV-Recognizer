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
import constants

class RebuildCsv:
    def __init__(self):
        #os.chdir(constants.FACE_BASE_DATABASE_DIR)

        f = open(os.path.join(constants.DATABASE_DIR, 'database.csv'), 'w')
        names = open(os.path.join(constants.DATABASE_DIR, 'names.csv'), 'w')

        label_id = 1
        for root, dirs, files in os.walk(constants.DATABASE_DIR):
            if root == '.':
                continue

            dir = root.replace('.', '')

            if not dir.endswith("database"):
                for file in files:
                    if file.endswith(".pgm"):
                        output = os.path.join(dir, file) + ';' + str(label_id)
                        f.write(output + '\n')

                name = dir.split(os.sep)
                names.write("%d;%s\n" % (label_id, name[-1]))

                label_id += 1

        f.close()
        names.close()


if __name__ == '__main__':
    csv = RebuildCsv()
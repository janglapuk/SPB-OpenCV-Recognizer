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
import cv2, threading
from PIL import Image, ImageTk
import constants
import numpy as np
import util
from collections import deque

CAMERA_MODE_DEFAULT = 0
CAMERA_MODE_FACE_RECOG = 1
CAMERA_MODE_GEST_RECOG = 2
CAMERA_MODE_FACE_CHANGER = 3

class Camera:
    # objek opencv video
    _video = None

    # mode kamera
    camera_mode = CAMERA_MODE_DEFAULT

    # objek opencv cascade
    face_cascade = None

    # toggle DB snap
    snap_enabled = False

    # direktori user untuk menyimpan database wajah
    snap_user_dir = None

    # objek recognizer (LBPH)
    recognizer = None

    # kamus/dict nama-nama pada database
    recognized_names = None

    # objek mask
    mask = None

    # nama file mask
    mask_name = None

    ot_pts = deque(maxlen=constants.OT_MAX_BUFFER)

    def __init__(self, gui, cam_id=-1):
        self.cam_id = cam_id
        self.gui = gui
        self.run = False

        self._init_cascade()


    def _init_cascade(self):
        '''
        Fungsi inisiasi objek cascade
        :return: cascade object
        '''
        self.face_cascade = cv2.CascadeClassifier(util.cascade_file('haarcascade_frontalface_alt.xml'))


    def _snap_guidelines(self, frame):
        '''
        Fungsi untuk menggambar garis petunjuk untuk pengambilan database wajah
        :param frame: frame dari objek VideoCapture
        :return: frame object
        '''
        # vertikal simetris
        frame = cv2.line(frame, (400, 0), (400, 600), (0, 0, 0), 1)
        cv2.putText(frame, "Garis Simetris", (330, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        # horiz mata
        frame = cv2.line(frame, (0, 250), (800, 250), (0, 0, 0), 1)
        cv2.putText(frame, "Garis Mata", (10, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        # horiz mulut
        frame = cv2.line(frame, (0, 400), (800, 400), (0, 0, 0), 1)
        cv2.putText(frame, "Garis Mulut", (10, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)


    def _snap_thread_crop(self, user_dir, seq):
        '''
        Fungsi thread untuk cropping temp file
        :param user_dir:
        :param seq:
        :return:
        '''

        any_face_detected = False

        img_file_bmp = "%d.%s" % (seq, 'bmp')
        img_file_pgm = "%d.%s" % (seq, 'pgm')
        save_file = os.path.join("%s" % user_dir, img_file_pgm)
        save_tmp_file = os.path.join("%s" % user_dir, "_tmp_" + img_file_bmp)

        buffer = cv2.imread(save_tmp_file, cv2.IMREAD_GRAYSCALE)

        faces = self.face_cascade.detectMultiScale(buffer, scaleFactor=1.3, minNeighbors=4)

        for (x, y, w, h) in faces:
            x -= 30
            y -= 30
            w += 30
            h += 30

            grayFrame = cv2.equalizeHist(buffer[y:y+h, x:x+w])
            grayFrame = cv2.resize(grayFrame, constants.TRAIN_IMAGE_SIZE, interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(save_file, grayFrame)

            os.remove(save_tmp_file)

            any_face_detected = True

        if any_face_detected:
            self.gui.log("DB: sukses => " + img_file_pgm)
        else:
            self.gui.log("DB: gagal")
            print("[{0}] Deteksi region wajah sequence {1} gagal :(".format(__name__, seq))


    def _snap(self, frame):
        seq = self._get_sequence_number(self.snap_user_dir)

        img_file_bmp = "%d.%s" % (seq, 'bmp')

        save_tmp_file = os.path.join("%s" % self.snap_user_dir, "_tmp_" + img_file_bmp)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        buffer = Image.fromarray(gray)
        buffer.save(save_tmp_file)

        threading.Thread(target=self._snap_thread_crop, args=(self.snap_user_dir, seq)).start()

        self.snap_enabled = False
        self.snap_user_dir = None

    def _get_sequence_number(self, dir):
        seq = 1
        while True:
            if os.path.exists(os.path.join(dir, "%d.%s" % (seq, 'pgm'))):
                seq += 1
                continue
            else:
                break

        return seq

    def _face_recognizer(self, frame_):
        if self.recognizer is None:
            self.recognizer = cv2.face.createLBPHFaceRecognizer() #threshold=110.0, radius=5, neighbors=8, grid_x=8, grid_y=8)
            #self.recognizer = cv2.face.createFisherFaceRecognizer()
            #self.recognizer = cv2.face.createEigenFaceRecognizer()

            csv_file = os.path.join(constants.DATABASE_DIR, 'database.csv')
            images, labels = util.read_csv(csv_file)

            self.recognized_names = self._get_recognized_names()
            self.recognizer.train(np.asarray(images), np.asarray(labels))
            #self.recognizer.save(os.path.join(constants.FACE_BASE_DATABASE_DIR, 'lbph.xml'))
            #self.recognizer.load(os.path.join(constants.FACE_BASE_DATABASE_DIR, 'lbph.yml'))

        frame = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)

        faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=4)

        for (x, y, w, h) in faces:
            grayFrame = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)
            currDetectedObj = cv2.equalizeHist(grayFrame[y:y+h, x:x+w])
            currDetectedObj = cv2.resize(currDetectedObj, constants.TRAIN_IMAGE_SIZE, interpolation=cv2.INTER_CUBIC)

            label, confidence = self.recognizer.predict(currDetectedObj)

            if label is not -1:
                predicted_name = self.recognized_names[int(label)].upper()
            else:
                predicted_name = 'Unknown'
                confidence = -1

            print("Faces: %d | Label %d | Name: %s | Confidence: %f" % (len(faces), label, predicted_name, confidence))

            cv2.putText(frame, "%s" % predicted_name, (x, y-15), cv2.FONT_HERSHEY_PLAIN, 1, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 1)

        return frame

    def _draw_face_overlay(self, background, overlay, rect, zoom_scale=0):
        x, y, w, h = rect

        try:
            # Aspect ratio
            base_height = h + 50 + zoom_scale
            ratio_w, ratio_h = util.proportion_resize(base_height, overlay.shape[1], overlay.shape[0])
            resized_mask = cv2.resize(overlay, (ratio_w, ratio_h))
            resized_mask = cv2.cvtColor(resized_mask, cv2.COLOR_BGRA2RGBA)

            # Cari titik tengah wajah
            xc = int(x + (w/2))
            yc = int(y + (h/2))

            # Cari titik tengah gambar berdasarkan titik tengah wajah
            x_offset = int(xc - (ratio_w / 2))
            y_offset = int(yc - (ratio_h / 2))

            for c in range(0,3):
                background[y_offset:y_offset + resized_mask.shape[0], x_offset:x_offset + resized_mask.shape[1], c] = \
                    resized_mask[:,:,c] * (resized_mask[:,:,3]/255.0) + background[y_offset:y_offset + resized_mask.shape[0], \
                    x_offset:x_offset+resized_mask.shape[1], c] * (1.0 - resized_mask[:,:,3]/255.0)

        except Exception as e:
            print("Exception on _draw_overlay: " + str(e))
            pass


    def _face_changer(self, frame_):
        '''
        Fungsi callback
        :param frame_: frame yang berasal dari VideoSource
        :return: numpy array
        '''
        frame = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
        faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=4)

        for (x, y, w, h) in faces:
            current_mask_name = self.gui.get_mask_name()
            if self.mask_name is not current_mask_name:
                self.mask_name = current_mask_name
                self.mask = cv2.imread(os.path.join(constants.RESOURCE_MASK_DIR, current_mask_name), -1)

            zoom_scale = int(self.gui.get_mask_zoom_value())
            self._draw_face_overlay(frame, self.mask, (x, y, w, h), zoom_scale)

        return frame

    def _object_tracking(self, frame):
        # Buat frame background sedikit lebih blur
        cv2.GaussianBlur(frame, (11, 11), 0)

        # Konversi frame untuk diubah ke mode warna HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Buat mask yang hanya mendeteksi range warna tertentu, dalam kasus ini hijau
        mask = cv2.inRange(hsv, constants.OT_GREEN_LOWER, constants.OT_GREEN_UPPER)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Cari kontur-kontur yang diwakili
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        center = None
        circle_drawn = False

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                circle_drawn = True

        if circle_drawn:
            self.ot_pts.appendleft(center)

            for i in range(1, len(self.ot_pts)):
                if self.ot_pts[i - 1] is None or self.ot_pts[i] is None:
                    continue

                thickness = int(np.sqrt(constants.OT_MAX_BUFFER / float(i + 1)) * 2.5)
                cv2.line(frame, self.ot_pts[i - 1], self.ot_pts[i], (0, 255, 0), thickness)

        return frame

    def _get_recognized_names(self):
        '''
        Fungsi ini untuk membaca label dan nama pada file 'database/names.csv'
        :return: dictionary
        '''
        name_file = os.path.join(constants.DATABASE_DIR, 'names.csv')
        dict_name = {}

        with open(name_file) as f:
            for line in f:
                label, name = line.replace('\n', '').split(';')
                dict_name[int(label)] = name

        print("[_get_recognized_names] Loaded %d names" % (len(dict_name),))
        return dict_name

    def __camera_feeder(self):

        video = None

        if self.run == False:
            video = cv2.VideoCapture(self.cam_id)
            video.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
            video.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

            if video.isOpened():
                self.run = True

        def update_frame():

            _, frame = video.read()

            if self.camera_mode == CAMERA_MODE_FACE_RECOG:
                frame = self._face_recognizer(frame)

            elif self.camera_mode == CAMERA_MODE_GEST_RECOG:
                frame = self._object_tracking(frame)

            elif self.camera_mode == CAMERA_MODE_FACE_CHANGER:
                frame = self._face_changer(frame)

            else:
                # Snap from default mode
                if self.snap_enabled:
                    self._snap(frame)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if self.gui.DB_toggle:
                self._snap_guidelines(frame)

            if self.run:
                buffer = Image.fromarray(frame)
                image = ImageTk.PhotoImage(buffer)

                self.gui.update_image(image=image).after(0, update_frame)

            else:
                video.release()

        if self.run:
            update_frame()

    def start(self):
        self.thread = thread = threading.Thread(target=self.__camera_feeder)
        thread.start()

    def stop(self):
        self.run = False

    def setmode(self, mode):
        self.camera_mode = mode

        if mode is CAMERA_MODE_FACE_RECOG:
            self._read_csv()

    def snap_face(self, name):
        user_dir = os.path.join(constants.DATABASE_DIR, name)

        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        self.snap_user_dir = user_dir
        self.snap_enabled = True
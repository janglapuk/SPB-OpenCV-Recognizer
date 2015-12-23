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

from tkinter import messagebox, Tk
import pygubu, re
import util
import camera
from PIL import ImageTk, Image
import constants
import os, sys

# import custom widgets
sys.path.append(constants.UI_DIR)

class GUI:
    camera = None
    camera_run = False
    camera_list = []
    canvas = None
    DB_toggle = False

    def __init__(self):
        self.root = root = Tk()
        self.builder = builder = pygubu.Builder()

        toplevel = root.winfo_toplevel()
        toplevel.title("%s %s" % (constants.APP_NAME, constants.APP_VERSION))

        builder.add_from_file(constants.UI_MAIN_FILE)
        builder.get_object('frame_main', root)
        builder.connect_callbacks(self)

        self._make_center(toplevel)
        self._init_camera_sources()
        self._init_masks()

    def _init_camera_sources(self):
        cam_list = util.get_cameras(2)
        cam_source = self.builder.get_object('combo_source')

        cam_dict = {}
        for cam in cam_list:
            cam_dict['Camera #%d' % cam] = int(cam)

        cam_source.setdict(cam_dict)
        cam_source.current(0)
        cam_source.configure(state='readonly')

        if cam_source.dictlength() == 0:
            cam_toggle = self.builder.get_object('chk_cam_toggle')
            cam_toggle.configure(state='disabled')
            def show_error():
                messagebox.showerror("Kesalahan",
                                     "Nampaknya tidak ada sumber kamera yang dapat digunakan pada aplikasi ini. " +
                                     "Silakan periksa perangkat kamera anda dan pastikan telah bekerja dengan baik.")

            cam_toggle.after(1000, show_error)

    def _init_masks(self):
        combox = self.builder.get_object('combo_mask')
        masks = []
        for _, _, files in os.walk(constants.RESOURCE_MASK_DIR):
            for file in files:
                if file.endswith('.png'):
                    masks.append(file)

        combox.configure(values=masks)
        combox.current(0)

    def _make_center(self, top_level):
        top_level.update_idletasks()
        w = top_level.winfo_screenwidth()
        h = top_level.winfo_screenheight()
        size = tuple(int(_) for _ in top_level.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        top_level.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def _combo_source_handler(self, event):
        print(event)
        pass

    def _set_default_screen(self):
        canvas = self.builder.get_object('canvas_cam')

        im = Image.open(os.path.join(constants.RESOURCE_DIR, 'bg.jpg'))
        canvas.image = ImageTk.PhotoImage(im)

        canvas.delete('all')
        canvas.create_image(0, 0, anchor='nw', image=canvas.image)
        canvas.update()

    def _on_cam_toggle(self):
        var = self.builder.get_variable('var_cam_toggle')
        activated = bool(var.get())
        cam_source = self.builder.get_object('combo_source')

        if activated:
            cam_source.configure(state='disabled')
            self.builder.get_object('btn_DB_toggle').configure(state='normal')
            self.start_camera()
            self.log("Camera: ON")
        else:
            cam_source.configure(state='readonly')
            self.builder.get_object('btn_DB_toggle').configure(state='disabled')
            self.stop_camera()
            self.log("Camera: OFF")

    def _on_face_recognizer_clicked(self):
        print('_on_face_recognize_clicked')
        if self.camera is not None:
            self.camera.setmode(camera.CAMERA_MODE_FACE_RECOG)
            self.log("Mode: Pengenalan wajah")

    def _on_default_clicked(self):
        print('_on_default_clicked')
        if self.camera is not None:
            self.camera.setmode(camera.CAMERA_MODE_DEFAULT)
            self.log("Mode: Default")

    def _on_face_changer_clicked(self):
        if self.camera is not None:
            self.camera.setmode(camera.CAMERA_MODE_FACE_CHANGER)
            self.log("Mode: Pengubah Wajah")

    def _on_object_tracking_clicked(self):
        if self.camera is not None:
            self.camera.setmode(camera.CAMERA_MODE_GEST_RECOG)
            self.log("Mode: Pelacak Objek")

    def _on_db_toggle(self):
        self.DB_toggle = not self.DB_toggle

        if self.DB_toggle:
            self.builder.get_object('btn_DB_toggle').configure(text='Off')
            self.builder.get_object('btn_DB_snap').configure(state='normal')
            entry = self.builder.get_object('entry_DB_name')
            entry.configure(state='normal')
            entry.focus_set()
            self.log("Database ON")

        else:
            self.builder.get_object('btn_DB_toggle').configure(text='On')
            self.builder.get_object('btn_DB_snap').configure(state='disabled')
            self.builder.get_object('entry_DB_name').configure(state='disabled')
            self.builder.get_variable("var_entry_DB_name").set('')
            self.log("Database: OFF")


    def _on_db_snap_clicked(self):
        var_db_name = self.builder.get_variable("var_entry_DB_name")
        if len(var_db_name.get()) < 3:
            messagebox.showerror("Error", "Nama untuk database kurang dari 3 karakter!")
            self.builder.get_object('entry_DB_name').focus_set()
        else:
            if self.camera is not None:
                var = self.builder.get_variable('var_entry_DB_name')
                self.camera.snap_face(var.get())


    def _selected_cam(self):
        '''
        !DEPRECATED!
        :return:
        '''
        var = self.builder.get_variable('var_selected_cam')
        sel = re.findall(r'\d', var.get())

        if len(sel) > 0:
            return sel[0]

        return -1

    def log(self, text):
        tv = self.builder.get_object('tv_log')
        tv.insert("", 0, text=text)

    def update_image(self, image):
        if self.canvas is None:
            self.canvas = self.builder.get_object('canvas_cam')

        self.canvas.delete('all')
        self.canvas.create_image(0, 0, anchor='nw', image=image)
        self.canvas.update()

        return self.canvas

    def start_camera(self):
        cam_num = int(self._selected_cam())
        if cam_num >= 0:
            self.camera = camera.Camera(self, cam_num)
            self.camera.start()
        else:
            print('Error on camera')

    def stop_camera(self):
        self.camera.stop()
        self._set_default_screen()
        self.camera = None

    def show(self):
        self._set_default_screen()
        self.root.mainloop()

    def get_mask_zoom_value(self):
        scale = self.builder.get_object('scale_zoom')
        return scale.get()

    def get_mask_name(self):
        var = self.builder.get_variable('var_combo_mask')
        return var.get()

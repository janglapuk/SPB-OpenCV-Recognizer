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

from tkinter import Tk, ttk
import collections

class DictCombobox(ttk.Combobox):
    __DEBUG = False
    __dictionary = {}

    def __init__(self, master=None, **kw):
        ttk.Combobox.__init__(self, master, **kw)

        if self.__DEBUG:
            self.bind('<<ComboboxSelected>>', self.__on_selected) # Debugging only

    def setdict(self, dict):
        self.__dictionary = collections.OrderedDict(sorted(dict.items()))

        values = []
        for key, value in self.__dictionary.items():
            values.append(str(key))

        self.configure(values=values)

    def getdict(self):
        return self.__dictionary

    def dictlength(self):
        return len(self.__dictionary)

    def value(self):
        return self.__dictionary[self.get()]

    def __on_selected(self, event):
        print(self.value())
        pass
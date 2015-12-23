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

from pygubu import BuilderObject, register_widget
#import os, sys
#sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from dictcombobox import DictCombobox

class DictComboboxBuilder(BuilderObject):
    OPTIONS_SPECIFIC = ('exportselection', 'justify', 'height',
                        'postcommand', 'state', 'textvariable', 'values',
                        'width', 'validate', 'validatecommand',
                        'invalidcommand', 'xscrollcommand')
    OPTIONS_CUSTOM = ('validatecommand_args', 'invalidcommand_args')

    class_ = DictCombobox

    container = False
    properties = (BuilderObject.OPTIONS_STANDARD + OPTIONS_SPECIFIC + OPTIONS_CUSTOM)
    command_properties = ('postcommand', 'validatecommand',
                          'invalidcommand', 'xscrollcommand')

    def _set_property(self, target_widget, pname, value):
        if pname in ('validatecommand_args', 'invalidcommand_args'):
            pass
        else:
            super(DictComboboxBuilder, self)._set_property(target_widget, pname, value)

    def _create_callback(self, cpname, command):
        callback = command
        if cpname in ('validatecommand', 'invalidcommand'):
            args = self.properties.get(cpname + '_args', '')
            if args:
                args = args.split(' ')
                callback = (self.widget.register(command),) + tuple(args)
            else:
                callback = self.widget.register(command)
        return callback


register_widget('dictcomboboxwidget.dictcombobox', DictComboboxBuilder, 'DictCombobox', ('ttk', 'Custom Controls'))
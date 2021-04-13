#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'GPL v3'
__copyright__ = '2013, Stanislav Kazmin'
__docformat__ = 'restructuredtext en'

from PyQt5.Qt import QWidget, QVBoxLayout, QLabel, QLineEdit

from calibre.utils.config import JSONConfig

# This is where all preferences for this plugin will be stored
# Remember that this name (i.e. plugins/interface_demo) is also
# in a global namespace, so make it as unique as possible.
# You should always prefix your config file name with plugins/,
# so as to ensure you dont accidentally clobber a calibre config file
prefs = JSONConfig('plugins/recoll_fulltext_search')

# Set defaults
prefs.defaults['pathToLibrary'] = '$HOME/Calibre Library'
prefs.defaults['pathToCofig'] = '$HOME/.config/calibre'
prefs.defaults['pathToRecoll'] = '/usr/bin'

class ConfigWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.l = QVBoxLayout()
        self.setLayout(self.l)
                
        self.labelText = QLabel('Set the paths to the different directories.\nDo not use "/" at the end of the path.\nDefaults are:\nPath to Calibre Library directory: $HOME/Calibre Library\nPath to Calibre Cofig directory: $HOME/.config/calibre\nPath to recoll bin directory: /usr/bin')
        
        
        self.l.addWidget(self.labelText)

        self.labelLibrary = QLabel('Path to Calibre Library directory:')
        self.l.addWidget(self.labelLibrary)

        self.pathToLibrarySetting = QLineEdit(self)
        self.pathToLibrarySetting.setText(prefs['pathToLibrary'])
        self.l.addWidget(self.pathToLibrarySetting)
        self.labelLibrary.setBuddy(self.pathToLibrarySetting)
        
        self.labelCofig = QLabel('Path to Calibre Cofig directory:')
        self.l.addWidget(self.labelCofig)        
        
        self.pathToCofigSetting = QLineEdit(self)
        self.pathToCofigSetting.setText(prefs['pathToCofig'])
        self.l.addWidget(self.pathToCofigSetting)
        self.labelCofig.setBuddy(self.pathToCofigSetting)
        
        self.labelRecoll = QLabel('Path to recoll bin directory:')
        self.l.addWidget(self.labelRecoll)        
        
        self.pathToRecollSetting = QLineEdit(self)
        self.pathToRecollSetting.setText(prefs['pathToRecoll'])
        self.l.addWidget(self.pathToRecollSetting)
        self.labelRecoll.setBuddy(self.pathToRecollSetting)

    def save_settings(self):
        prefs['pathToLibrary'] = self.pathToLibrarySetting.text()
        prefs['pathToCofig'] = self.pathToCofigSetting.text()
        prefs['pathToRecoll'] = self.pathToRecollSetting.text()


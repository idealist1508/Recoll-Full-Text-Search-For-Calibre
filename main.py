#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'GPL v3'
__copyright__ = '2013, Stanislav Kazmin'
__docformat__ = 'restructuredtext en'

if False:
    # This is here to keep my python error checker from complaining about
    # the builtin functions that will be defined by the plugin loading system
    # You do not need this code in your plugins
    get_icons = get_resources = None


from PyQt5.Qt import (QDialog, QVBoxLayout, QPushButton, QMessageBox, QLabel, 
                      QLineEdit, QComboBox,  QCompleter,  QMainWindow,  QWidget,  QTextEdit)
from calibre_plugins.recoll_fulltext_search.config import prefs

from subprocess import Popen, PIPE, STDOUT
import re

class AboutWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.create_main_frame()       

    def create_main_frame(self):        
        page = QWidget()        

        self.button = QPushButton('OK', page)
        self.textWindow = QTextEdit()

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.textWindow)
        vbox1.addWidget(self.button)
        page.setLayout(vbox1)
        self.setCentralWidget(page)

        self.button.clicked.connect(self.clicked)

    def clicked(self):
        self.close()

class RecollFulltextSearchDialog(QDialog):

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config

        # The current database shown in the GUI
        # db is an instance of the class LibraryDatabase2 from database.py
        # This class has many, many methods that allow you to do a lot of
        # things.
        self.db = gui.current_db

        self.l = QVBoxLayout()
        self.setLayout(self.l)
        


        # Label
        self.labelText = QLabel('Use "and" and "or" for the search.')
        self.l.addWidget(self.labelText)

        # Title
        self.setWindowTitle('Recoll Full Text Search')
        self.setWindowIcon(icon)

        # Search window
        self.searchTextWindow = QComboBox()
        self.searchTextWindow.setEditable(True)
        self.l.addWidget(self.searchTextWindow)
        self.searchTextWindow.setFocus()
        self.searchTextWindow.setInsertPolicy(QComboBox.NoInsert)
        self.searchTextWindow.setDuplicatesEnabled(False)
        
        #Completer for the seach window
        self.completer = QCompleter()
        self.completer.setCompletionMode( QCompleter.UnfilteredPopupCompletion )
        self.searchTextWindow.setCompleter(self.completer)
        
        # output window
        self.outputWindow = QLabel()
        self.l.addWidget(self.outputWindow)
        
        # search button 1
        self.doSearchButton = QPushButton('Search and replace the filter', self)
        self.doSearchButton.clicked.connect(self.recollSearchNew)
        self.l.addWidget(self.doSearchButton)
        self.doSearchButton.setDefault(True)
                
        # search button 2
        self.doSearchButton = QPushButton('Search and add to filter', self)
        self.doSearchButton.clicked.connect(self.recollSearchAdd)
        self.l.addWidget(self.doSearchButton)
    
        # update database button 1
        self.updateDatabaseButton = QPushButton('Update recoll database', self)
        self.updateDatabaseButton.clicked.connect(self.updateDatabase)
        self.l.addWidget(self.updateDatabaseButton)
        
        # update database button 2
        self.newDatabaseButton = QPushButton('Make new recoll database', self)
        self.newDatabaseButton.clicked.connect(self.newDatabase)
        self.l.addWidget(self.newDatabaseButton)
        
        # config button
        self.configButton = QPushButton('Configure this plugin', self)
        self.configButton.clicked.connect(self.config)
        self.l.addWidget(self.configButton)
        
        # about button
        self.aboutButton = QPushButton('About', self)
        self.aboutButton.clicked.connect(self.about)
        self.l.addWidget(self.aboutButton)

        self.resize(self.sizeHint())
        #self.resize(500, self.height())
        

    def about(self):
        # Get the about text from a file inside the plugin zip file
        # The get_resources function is a builtin function defined for all your
        # plugin code. It loads files from the plugin zip file. It returns
        # the bytes from the specified file.
        
        text = get_resources('about.txt')
        #box = QMessageBox()
        #box.about(self, 'About the Recoll Full Text Search \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t',text.decode('utf-8'))
        #self.resize(600, self.height())
        
        self.box = AboutWindow()
        self.box.setWindowTitle("About the Recoll Full Text Search Plugin")
        self.box.textWindow.setText(text)
        self.box.textWindow.setReadOnly(True)
        self.box.resize(600, 500)
        self.box.show()
        

    def updateDatabase(self):
        self.replaceDatabase =False
        self.makeDatabase()

    def newDatabase(self):
        self.replaceDatabase = True
        self.makeDatabase()

    def recollSearchNew(self):
        self.searchAdd = False
        self.recollSearch()
    
    def recollSearchAdd(self):
        self.searchAdd = True
        self.recollSearch()

    def makeDatabase(self):
        '''Runs recollindex outside calibre like in a terminal. 
        Look for recollindex for more information about the flags and options'''
        self.cmd = [prefs['pathToRecoll'] + '/recollindex', '-c', prefs['pathToCofig'] + '/plugins/recollFullTextSearchPlugin']
        #TODO: Fix for Linux
        #self.cmd = 'LD_LIBRARY_PATH="" ' + prefs['pathToRecoll'] + '/recollindex -c ' + prefs['pathToCofig'] + '/plugins/recollFullTextSearchPlugin'
        if self.replaceDatabase == True :
            self.cmd += [' -z']
        self.p = Popen(self.cmd,  shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        # TODO: Was close_fds nessesary? check it on linux
        #self.p = Popen(self.cmd,  shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

        box = QMessageBox()
        box.about(self, 'Please read! \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t','Depending on you library size this operation can take a lot of time.\nThe process runs outside calibre so you can use or close it, but do not use this plugin.\nFor now there is no information about when recoll finishs,\nso look up, whether a recoll of recollindex process is running on you system.')

    def recollSearch(self):
        '''Runs recoll outside calibre like in a terminal. 
        Look for recollindex for more information about the flags and options'''
        self.searchText = str(self.searchTextWindow.currentText())# search text from the plugin gui
        self.searchTextWindow.insertItem(0, self.searchText)
        #TODO: Fix Linux
        #self.cmd = 'LD_LIBRARY_PATH="" ' + prefs['pathToRecoll'] + '/recoll -c ' + prefs['pathToCofig'] + '/plugins/recollFullTextSearchPlugin -b -t '
        self.cmd = [prefs['pathToRecoll'] + '/recoll', '-c', prefs['pathToCofig'] + '/plugins/recollFullTextSearchPlugin', '-b', '-t']
        self.cmdString = self.cmd + [self.searchText]
        # TODO: Was close_fds nessesary? check it on linux
        #self.p = Popen(self.cmdString,  shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        self.p = Popen(self.cmdString,  shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        self.output = self.p.stdout.read()# output from the recoll search
     
        self.found = list(set(re.findall(r" \((\d+)\)\/[^/]*", self.output)))# regex to find the calibre ids in the folder names
     
        self.wholeString = ''
        if len(self.found) == 0 :
            self.outputWindow.setText('no books found' + ' for ' + self.searchText)
        else :
            self.wholeString = 'id:'
            for elem in self.found[:300]:
                self.wholeString += '=' + elem + ' or '
            self.wholeString = self.wholeString[:-4]
            if len(self.found) > 300 :
                self.outputWindow.setText(str(len(self.found)) + ' books found' + ' for ' + self.searchText+ '. Only the first 300 books are shown')
            else :
                self.outputWindow.setText(str(len(self.found)) + ' books found' + ' for ' + self.searchText)

        if self.searchAdd == True :
            self.oldFilter = self.gui.search.text()
            self.wholeString = self.oldFilter + ' and (' + self.wholeString + ')'
        
        self.searchTextWindow.clearEditText()
        self.gui.search.setEditText(self.wholeString) # set calibre search to the string found by recoll
        self.gui.search.do_search()

    def config(self):
        self.do_user_config(parent=self)


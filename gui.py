#!/usr/bin/env python3

import sys
from PyQt4 import QtGui, QtCore, QtWidgets

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 300

BUTTON_WIDTH = 80
BUTTON_HEIGHT = 30

search_query = {
	"search": "",
	"days_since_posting": "",
	"file_name": "",
	"location": "desktop",
	"semester": "",
	"co_op": "False",
	"internship": "False",
}

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle("Linkedin Webscraper")
        self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        self.home()

    def home(self):
    	self.add_exit_button()
    	self.add_search_button()
    	self.add_search_bar()
    	self.show()

    def add_search_bar(self):
    	search_input = QtGui.QLineEdit()

    def add_search_button(self):
    	btn = QtGui.QPushButton("Search", self)
    	btn.clicked.connect(self.scrape_linkedin)
    	btn.resize(BUTTON_WIDTH, BUTTON_HEIGHT)
    	btn.move(0, WINDOW_HEIGHT - BUTTON_HEIGHT)

    def add_exit_button(self):
    	btn = QtGui.QPushButton("Quit", self)
    	btn.clicked.connect(self.close_application)
    	btn.resize(BUTTON_WIDTH, BUTTON_HEIGHT)
    	btn.move(WINDOW_WIDTH - BUTTON_WIDTH, WINDOW_HEIGHT - BUTTON_HEIGHT)

    def scrape_linkedin(self):
    	print("\"Scraping\"")

    def close_application(self):
    	sys.exit()

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

run()
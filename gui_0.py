#!/usr/bin/env python3

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QComboBox, QCheckBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize    

search_query = {
    'search': '',
    'days_since_posting': '',
    'file_name': '',
    'location': 'desktop',
    'semester': '',
    'coop': 'False',
    'internship': 'False',
}

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(400, 150))    
        self.setWindowTitle("Linkedin Scraper") 

        # Making all labels
        self.searchLabel = QLabel(self)
        self.searchLabel.setText('Search:')
        self.daysLabel = QLabel(self)
        self.daysLabel.setText('Days since posted:')
        self.semesterLabel = QLabel(self)
        self.semesterLabel.setText('Semester:')
        self.coopLabel = QLabel(self)
        self.coopLabel.setText('Co-op')
        self.internshipLabel = QLabel(self)
        self.internshipLabel.setText('Internship')

        # Making all line edits
        self.searchLine = QLineEdit(self)
        self.dayLine = QLineEdit(self)

        # Making all combo boxes
        self.semesterBox = QComboBox(self)

        # Making all checkboxes
        self.coopBox = QCheckBox(self)
        self.internshipBox = QCheckBox(self)

        # Modifying search line
        self.searchLine.move(80, 20)
        self.searchLine.resize(306, 32)
        self.searchLabel.move(20, 20)

        # Modifying day line
        self.dayLine.move(160, 60)
        self.dayLine.resize(32, 32)
        self.daysLabel.move(20, 65)
        self.daysLabel.adjustSize()

        # Modifying semester line
        self.semesterBox.addItem("Summer")
        self.semesterBox.addItem("Fall")
        self.semesterBox.addItem("Spring")
        self.semesterBox.addItem("Winter")
        self.semesterBox.move(287, 60)
        self.semesterLabel.move(212, 60)

        # Modifying search button
        pybutton = QPushButton('Search', self)
        pybutton.clicked.connect(self.searchLinkedin)
        pybutton.resize(200, 32)
        pybutton.move(40, 102)   

        # Modifying checkboxes  
        self.coopBox.move(260, 95)
        self.coopLabel.move(280, 95)
        self.coopBox.stateChanged.connect(self.checkCoop)
        self.internshipBox.move(260, 110)
        self.internshipLabel.move(280, 110)
        self.internshipBox.stateChanged.connect(self.checkInternship)

    def searchLinkedin(self):
        print('Your search: ' + self.searchLine.text())
        print('Days since posted: ' + self.dayLine.text())
        print('Semester: ' + self.semesterBox.currentText())
        print('Co-op: ' + str(self.coopBox.isChecked()))
        print('Internship: ' + str(self.internshipBox.isChecked()))
        
        # Populate search query dictionary
        search_query['search'] = self.searchLine.text()
        search_query['days_since_posting'] = self.dayLine.text()
        search_query['semester'] = self.semesterBox.currentText()
        search_query['coop'] = str(self.coopBox.isChecked())
        search_query['internship'] = str(self.internshipBox.isChecked())
        print(search_query)


    def checkCoop(self, state):
        if state == QtCore.Qt.Checked:
            print('Checked')
        else:
            print('Unchecked')

    def checkInternship(sefl, state):
        if state == QtCore.Qt.Checked:
            print('Checked')
        else:
            print('Unchecked')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
#!/usr/bin/env python3

import sys
import datetime
import dateutil.parser

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QComboBox, QCheckBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize    
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from datetime import datetime, timedelta

search_query = {
	'search': '',
	'days_since_posting': '',
	'file_name': '',
	'location': 'desktop',
	'semester': '',
	'coop': '',
	'internship': '',
}	

class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)

		# Making window
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
		query = search_query['search'] + ' ' + search_query['semester'] + ' ' + search_query['coop'] + ' ' + search_query['internship']
		print(query.split())

		url = self.format_url(query.split())
		self.scrape(url)

	def checkCoop(self, state):
		if state == QtCore.Qt.Checked:
			search_query['coop'] = 'coop'
		else:
			search_query['coop'] = ''

	def checkInternship(sefl, state):
		if state == QtCore.Qt.Checked:
			search_query['internship'] = 'internship'
		else:
			search_query['internship'] = ''

	def format_url(self, query):
		url_start = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPostings/jobs?keywords='
		url_end = '&location=United%20States&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&start=0'
		url_keywords = ''
		for word in query:
			url_keywords = url_keywords + word + '%20'
		url_keywords = url_keywords[0:len(url_keywords) - 3]
		linkedin_api_url = url_start + url_keywords + url_end
		return linkedin_api_url

	def scrape_soup(self, page_soup, file):
		# Grabs the list elements(li) from the web page with the job search results
		# Note: if the html classes ever change for Linkedin the
		# "result-card job-result-card result-card--with-hover-state"
		# may need to be updated to reflect this
		job_list = page_soup.findAll("li", 
			"result-card job-result-card result-card--with-hover-state")

		for job in job_list:

			print(job)

			job_company = job.find("h4", "result-card__subtitle job-result-card__subtitle").text

			job_position = job.find("h3", "result-card__title job-result-card__title").text

			job_link = job.find("a", "result-card__full-card-link")["href"]

			posted = job.find("time", "job-result-card__listdate")
			if posted == None:
				posted = job.find("time", "job-result-card__listdate--new")

			days_posted = posted["datetime"]
			print(days_posted)

			insertion_date = dateutil.parser.parse(days_posted)
			print("Insertion date: " + str(insertion_date))

			oldest_permitted_date = datetime.today() - timedelta(days = int(search_query['days_since_posting']))
			print("Oldest permitted date: " + str(oldest_permitted_date))

			if insertion_date > oldest_permitted_date:
				# print("job_company: " + job_company)
				# print("job_position: " + job_position)
				# print("job_link: " + job_link)
				print("added")

				file.write(job_company.replace(",", "|") + "," + 
					job_position.replace(",", "|") + "," + 
					job_link.replace(",", "|") + "\n")

	def scrape(self, url):

		filename = "companies.csv"
		file = open(filename, "w")

		header = "Company,Position,Link\n"

		file.write(header)

		page_start = '0'

		while True:
			# Opening and connecting to web client
			uClient = uReq(url)
			page_html = uClient.read()
			uClient.close()

			# Parse the html into a soup
			page_soup = soup(page_html, "html.parser")
			#print("THIS IS THE PAGE SOUP" + page_soup.text)
			if page_soup.text == '':
				print("break")
				break

			self.scrape_soup(page_soup, file)
			url = url[0:len(url) - len(page_start)]
			page_start = str(int(page_start) + 25) # Changes the start page of the url to 25 further than before
			url = url + page_start
			print(url)

		file.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
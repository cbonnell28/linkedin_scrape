#!/usr/bin/env python3

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# NOTE: Currenly hard coded url
linkedin_api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPostings/jobs?keywords=Spring%202019%20Co-op&location=United%20States&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&start=0'

# Gets the inpu from the user
def reqest_query_from_user():
	input_query = input("Please enter your search query: ")
	return input_query.split()

def format_url(query):
	url_start = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPostings/jobs?keywords='
	url_end = '&location=United%20States&trk=guest_job_search_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0&start=0'
	url_keywords = ''
	for word in query:
		url_keywords = url_keywords + word + '%20'
	url_keywords = url_keywords[0:len(url_keywords) - 3]
	linkedin_api_url = url_start + url_keywords + url_end
	return linkedin_api_url

def scrape_soup(page_soup, file):
	# Grabs the list elements(li) from the web page with the job search results
	# Note: if the html classes ever change for Linkedin the
	# "result-card job-result-card result-card--with-hover-state"
	# may need to be updated to reflect this
	job_list = page_soup.findAll("li", 
		"result-card job-result-card result-card--with-hover-state")

	for job in job_list:
		job_company = job.find("h4", "result-card__subtitle job-result-card__subtitle").text

		job_position = job.find("h3", "result-card__title job-result-card__title").text

		job_link = job.find("a", "result-card__full-card-link")["href"]

		print("job_company: " + job_company)
		print("job_position: " + job_position)
		print("job_link: " + job_link)

		file.write(job_company.replace(",", "|") + "," + 
			job_position.replace(",", "|") + "," + 
			job_link.replace(",", "|") + "\n")

def scrape(url):

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

		scrape_soup(page_soup, file)
		url = url[0:len(url) - len(page_start)]
		page_start = str(int(page_start) + 25) # Changes the start page of the url to 25 further than before
		url = url + page_start
		print(url)

	file.close()

if __name__ == "__main__":
	user_query = reqest_query_from_user()
	url = format_url(user_query)
	scrape(url)
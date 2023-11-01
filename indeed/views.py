from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from base.models import Lead
import datetime
import random
import re

def index(request):
	headers = [
	{
		'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; vivo 1719) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36',
		'Accept-Language': 'en-GB,en;q=0.5',
		'Referer': 'https://google.com',
		'DNT': '1'
	},
	{
		'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-M236L) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/17.0 Chrome/96.0.4664.104 Mobile Safari/537.36',
		'Accept-Language': 'en-GB,en;q=0.5',
		'Referer': 'https://www.indeed.com/',
		'DNT': '2',
		'John': 'subtomplease'
	},
	{
		'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; InfoPath.3; MS-RTC LM 8; .NET4.0C; .NET4.0E)',
		'Accept-Language': 'en-GB,en;q=0.5',
		'Referer': 'https://bing.com',
		'DNT': '1',
	},
	{
		'User-Agent': 'Mozilla/5.0 (Linux; arm_64; Android 9; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.148 YaApp_Android/22.74.1 YaSearchBrowser/22.74.1 BroPP/1.0 SA/3 Mobile Safari/537.36',
		'Accept-Language': 'en-GB,en;q=0.5',
		'Referer': 'https://ask.com',
		'DNT': '1',
	},
	{
		'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; SM-P355) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
		'Accept-Language': 'en-GB,en;q=0.5',
		'Referer': 'https://www.indeed.com/',
		'DNT': '1',
	},
	{
		'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532G Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 Mobile Safari/537.36 Puffin/9.7.0.51211',
		'Accept-Language': 'en-GB,en;q=0.5',
		'Referer': 'https://duckduckgo.com',
		'DNT': '1',
	},
	{
		'User-Agent': 'Mozilla/5.0 (Linux; Android 9; moto g(6)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.70 Mobile Safari/537.36',
		'Accept-Language': 'en-GB,en;q=0.5',
		'Referer': 'https://www.indeed.com/',
		'DNT': '1',
	},
	{
		'User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-A205GN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
		'Accept-Language': 'en-GB,en;q=0.5',
		'Referer': 'https://google.com',
		'DNT': '1',
	},
	{
		'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Nokia C1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.116 Safari/537.36',
		'Accept-Language': 'en-GB,en;q=0.5',
		'Referer': 'https://bing.com',
		'DNT': '1',
	},
	{
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
		'Accept-Language': 'en-GB,en;q=0.5',
		'Referer': 'https://www.indeed.com/',
		'DNT': '1',
	}
	]
	results = []
	for x in range(0, 100, 10):
		URLs = []
		site = "https://www.indeed.com/jobs?q=developer&l=United%20States&sc=0kf%3Aattr(DSQF7)jt(contract)%3B&fromage=7&start=f'{x}'&vjk=617eb7264de4bdbf"
		page = requests.get(site, headers=headers[random.randint(0,9)])
		soup = BeautifulSoup(page.content, "html.parser")
		jobs_urls = soup.find_all('div', class_='job_seen_beacon')
		for job_url in jobs_urls:
			url = 'https://www.indeed.com' + job_url.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0')['href']
			URLs.append(url)

		
		for URL in URLs:
			page = requests.get(URL, headers=headers[random.randint(0,9)])
			soup = BeautifulSoup(page.content, "html.parser")
			jobs = soup.find('div', class_='jobsearch-ViewJobLayout-jobDisplay icl-Grid-col icl-u-xs-span12 icl-u-lg-span7')
		try:
			job_title = jobs.find('h1', class_='icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title')
			job_title = job_title.text
		except:
			job_title = None
		try:
			company_name = jobs.find('div', class_='jobsearch-CompanyInfoWithoutHeaderImage')
			company_name = company_name.find('span', class_='jobsearch-JobInfoHeader-companyNameSimple').text
		except:
			company_name = None
		try:
			job_description = jobs.find('div', class_='jobsearch-jobDescriptionText').text
		except:
			job_description = None
		try:
			job_type = re.findall("Job Type:.*$",job_description,re.MULTILINE) or re.findall("Job Types:.*$",job_description,re.MULTILINE)
			job_type = ' '.join(job_type)
		except:
			job_type = None
		try:
			date_posted = jobs.find('div', class_='jobsearch-JobMetadataFooter').text
			date_posted = re.match("[0-9][0-9]? days ago",date_posted, re.IGNORECASE).group(0)
		except:
			date_posted = None
		job = [job_title, company_name, job_description, job_type, date_posted, URL]
		results.append(job)
	
	
	# Inserting Each Job in DB
	for record in results:
		flag = Lead.objects.filter(job_source_url = record[4]) & Lead.objects.filter(job_posted_date = record[4])
		if flag.exists():
			continue
		else:
			if record[0] != None:
				instance = Lead(
					company_name = record[1], 
					client_name = '', 
					job_title = record[0],
					job_source = 'indeed',
					job_source_url = record[5],
					technologies = '',
					job_description = record[2],
					email = '',
					phone = '',
					linkedin = '',
					address = record[3],
					job_type = '',
					employee_range = '', 
					job_posted_date = record[4],
					status = 0,
					created_at = datetime.datetime.now()
				)
				instance.save()
			else:
				continue

	return render(request, 'indeed.html')
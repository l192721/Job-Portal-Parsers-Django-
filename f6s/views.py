from django.shortcuts import render
import requests
from base.models import Lead
import datetime
from bs4 import BeautifulSoup
import time
# Create your views here.


def index(request):
	headers ={
			'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36',
			'Accept-Language': 'en-GB,en;q=0.5',
			'Referer': 'https://bing.com',
			'DNT': '1'
		}


	for x in range(1,25):
		URL = "https://www.f6s.com/jobs?page=f'{x}'&page_alt=1&sort=newest&sort_dir=desc"
		page = requests.get(URL, headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")
		time.sleep(30)
		results = []
		jobs = soup.find_all('div', class_='bordered-list-item result-item')
		for job in jobs:
			job_title=job.find('div',class_='title')
			job_title = job.find('a', attrs={'class':'action main noline'}).get_text()
			job_url = 'https://www.f6s.com/' + job.find('a', class_='action main noline')['href']
			company_names = job.find('div',attrs={'class':'subtitle'})
			temp= company_names.find('span').get_text()
			temp = temp.split('•')
			company_name = temp[0].replace("\n", "") and temp[0].strip()
			address = temp[1].strip()
			try:
				job_type = temp[2].strip()
			except:
				continue
			job =[job_title,job_url,company_name,address,job_type]
			results.append(job)
		
		for record in results:
			flag = Lead.objects.filter(job_source_url = record[1])
			if flag.exists():
				continue
			else:
				instance = Lead(
					company_name = record[2], 
					client_name = '', 
					job_title = record[0],
					job_source = 'F6S',
					job_source_url = record[1],
					technologies = '',
					job_description = '',
					email = '',
					phone = '',
					linkedin = '',
					address = record[3],
					job_type = record[4],
					employee_range = '', 
					job_posted_date ='',
					status = 0,
					created_at = datetime.datetime.now()
				)
				instance.save()
	return render(request, 'f6s.html')
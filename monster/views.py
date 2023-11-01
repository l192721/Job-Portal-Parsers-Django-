from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from base.models import Lead
import datetime
import pandas as pd
import random

# def rnd_n():
# 	n = random. randint(1,1000)*9
# 	return n

def index(request):
	url = "https://appsapi.monster.io/jobs-svx-service/v2/monster/search-jobs/samsearch/en-US"

	querystring = {"apikey":"ulBrClvGP6BGnOopklreIIPentd101O2"}

	payload = {
		"jobQuery": {
			"query": "It",
			"locations": [
				{
					"country": "us",
					"address": "usa",
					"radius": {
						"unit": "mi",
						"value": 20
					}
				}
			]
		},
		"jobAdsRequest": {
			"position": [1, 2, 3, 4, 5, 6, 7, 8, 9],
			"placement": {
				"channel": "MOBILE",
				"location": "JobSearchPage",
				"property": "monster.com",
				"type": "JOB_SEARCH",
				"view": "CARD"
			}
		},
		"fingerprintId": "57da61d4dcba667826514f7ba330de3d",
		"offset": "9",
		"pageSize": '50',
		"histogramQueries": ["count(company_display_name)", "count(employment_type)"],
		"searchId": "f2f6c41c-5178-402a-a4f2-6cb4df349cc0"
	}
	headers = {
		"authority": "appsapi.monster.io",
		"accept": "application/json",
		"accept-language": "en-US,en;q=0.9",
		"content-type": "application/json; charset=UTF-8",
		"origin": "https://www.monster.com",
		"referer": "https://www.monster.com/jobs/search?q=It&where=usa&page=2&so=m.h.l",
		"request-starttime": "1659088508361",
		"sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
		"sec-ch-ua-mobile": "?0",
		"sec-ch-ua-platform": '"macOS"',
		"sec-fetch-dest": "empty",
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "cross-site",
		"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
	}

	response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
	data = response.json()

	jobs = data['jobResults']


	res = []
	for job in jobs:
		res.append(job)

	df = pd.json_normalize(res)
	df = df[["jobPosting.title", "createdDate", "jobPosting.url", "jobPosting.hiringOrganization.name", "normalizedJobPosting.jobLocationType", "normalizedJobPosting.jobLocation", "jobPosting.description"]]
	df.columns = ['job_title', 'job_posted_date', 'job_source_url', 'company_name', 'job_type', 'address', 'job_description']
	results = []
	for x in range(0, len(df.index)):
		job = df.iloc[x]
		job_title = job[0]
		job_posted_date = job[1]
		job_source_url = job[2]
		company_name = job[3]
		job_description = job[6]
		job_description = BeautifulSoup(job_description)
		job_description = job_description.get_text()
		job_type = job[4]
		try:
			address = job[5][0]["address"]["addressLocality"]
		except:
			address = ''
		job = [job_title, job_posted_date, job_source_url, company_name, job_type, address, job_description]
		results.append(job)
	
	for record in results:
		flag = Lead.objects.filter(job_source_url = record[2]) & Lead.objects.filter(job_posted_date = record[1])
		if flag.exists():
			continue
		else:
			instance = Lead(
				company_name = record[3], 
				client_name = '', 
				job_title = record[0],
				job_source = 'Monster',
				job_source_url = record[2],
				technologies = '',
				job_description = record[6],
				email = '',
				phone = '',
				linkedin = '',
				address = record[5],
				job_type = record[4],
				employee_range = '', 
				job_posted_date = record[1],
				status = 0,
				created_at = datetime.datetime.now()
			)
			instance.save()
	return render(request, 'monster.html')
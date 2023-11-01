from asyncio.windows_events import NULL
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from base.models import Lead
import datetime
import pandas as pd

def index(request):
	return render(request, 'dice_index.html')

def scrape(request):
	if request.method == 'POST':
		# search = requests.POST['job']
		# location = requests.POST['loc']
		for x in  range(1, 10):
			url = "https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search"

			jobs_per_page = 100 # 10, 20, 50, 100
			# current_page = 1

			querystring = {"q":"developer","countryCode2":"US","radius":"30","radiusUnit":"mi","page":f'{x}',"pageSize":f'{jobs_per_page}',"searchId":"561f0d5e-0915-468e-9100-7bd1e8d8f2c0","facets":"employmentType^%^7CpostedDate^%^7CworkFromHomeAvailability^%^7CemployerType^%^7CeasyApply^%^7CisRemote","filters.employmentType":"CONTRACTS","filters.postedDate":"SEVEN","filters.isRemote":"true","fields":"id^%^7CjobId^%^7Csummary^%^7Ctitle^%^7CpostedDate^%^7CmodifiedDate^%^7CjobLocation.displayName^%^7CdetailsPageUrl^%^7Csalary^%^7CclientBrandId^%^7CcompanyPageUrl^%^7CcompanyLogoUrl^%^7CpositionId^%^7CcompanyName^%^7CemploymentType^%^7CisHighlighted^%^7Cscore^%^7CeasyApply^%^7CemployerType^%^7CworkFromHomeAvailability^%^7CisRemote","culture":"en","recommendations":"true","interactionId":"1","fj":"true","includeRemote":"true","eid":"a6zd7NUgR0Wy8Tzf36TS2Q_"}

			headers = {
				"authority": "job-search-api.svc.dhigroupinc.com",
				"accept": "application/json, text/plain, */*",
				"accept-language": "en-US,en;q=0.9",
				"origin": "https://www.dice.com",
				"referer": "https://www.dice.com/",
				"sec-ch-ua": """.Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103""",
				"sec-ch-ua-mobile": "?0",
				"sec-ch-ua-platform": "Windows",
				"sec-fetch-dest": "empty",
				"sec-fetch-mode": "cors",
				"sec-fetch-site": "cross-site",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
				"x-api-key": "1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8"
			}

			response = requests.request("GET", url, headers=headers, params=querystring)

			data = response.json()

			jobs = data['data']

			res = []
			for job in jobs:
				res.append(job)
				
			df = pd.json_normalize(res)
			df = df[["title", "postedDate", "detailsPageUrl", "companyName", "employmentType", "jobLocation.displayName", "summary"]]
			df.columns = ['job_title', 'job_posted_date', 'job_source_url', 'Company_name', 'job_type', 'address', "job_description"]
			
			for i in range(0, len(df.index)):
				job = df.iloc[i]

				flag = Lead.objects.filter(job_source_url = job[2]) & Lead.objects.filter(job_posted_date = job[1])
				if flag.exists():
					continue
				else:
					instance = Lead(
						company_name = job[3], 
						client_name = '', 
						job_title = job[0],
						job_source = 'dice',
						job_source_url = job[2],
						technologies = '',
						job_description = job[6],
						email = '',
						phone = '',
						linkedin = '',
						address = job[5],
						job_type = job[4],
						employee_range = '', 
						job_posted_date = job[1],
						status = 0,
						created_at = datetime.datetime.now()
					)
					instance.save()

	return render(request, 'dice_scrape.html')

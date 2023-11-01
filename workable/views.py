from django.shortcuts import render
import datetime
import pandas as pd
import requests
from base.models import Lead
import time

def index(request):
    for x in range(10, 100, 10):
        url = "https://jobs.workable.com/api/v1/jobs"

        querystring = {"query":"DEVELOPER","location":"united^%^20states","remote":"true","offset":f'{x}'}

        payload = ""
        headers = {
            "cookie": "__hs_do_not_track=yes; __hs_opt_out=yes; wmc=^%^7B^%^22cookie_id^%^22^%^3A^%^2219a909f8-f017-49e3-8c36-edc01d5f07c1^%^22^%^7D",
            "authority": "jobs.workable.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "referer": "https://jobs.workable.com/search?query=full^%^20stack&location=United^%^20States^%^20of^%^20America&remote=false",
            "sec-ch-ua": "^\^.Not/A",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\^Windows^^",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        time.sleep(30)
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        data = response.json()
        jobs = data['jobs']

        res = []
        for job in jobs:
            res.append(job)

        df = pd.json_normalize(res)
        df = df[["title", "created", "url", "company.title", "employmentType", "locations", "description"]]
        df.columns = ['job_title', 'job_posted_date', 'job_source_url', 'Company_name', 'job_type', 'address', 'job_description']
        df.head()

        # Inserting Each Job in DB
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
                    job_source = 'workable',
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
    return render(request, 'workable.html')
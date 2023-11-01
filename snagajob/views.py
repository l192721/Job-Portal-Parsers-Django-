from django.shortcuts import render
import requests
import datetime
from bs4 import BeautifulSoup
import time
from base.models import Lead
# Create your views here.
def index(request):
    headers ={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Referer': 'https://bing.com',
            'DNT': '1'
        }

    URL = "https://www.snagajob.com/search?w=new+york,+ny&radius=20"
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    results=[]
    jobs= soup.find_all('div', class_='job-overview')
    for x in jobs:
        company_name = x.find('h3', class_= 'body-md mb-0 mt-0 text-gray-700 ng-star-inserted').text
        job_title = x.find('a',class_='heading-300 text-gray-900').text
        job_url = 'https://www.snagajob.com/' + x.find('a', class_='heading-300 text-gray-900')['href']
        job_type = x.find_all('div', class_='text-gray-900 ui-text-md ng-star-inserted')
        job_type= job_type[0].text
        address = x.find_all('div',class_='text-gray-900 ui-text-md ng-star-inserted')
        address = address[1].text
        x =[company_name,job_title,job_url,job_type,address]
        results.append(x)
        
    for record in results:
        flag = Lead.objects.filter(job_source_url = record[2])
        if flag.exists():
            continue
        else:
            instance = Lead(
                company_name = record[0],
                client_name = '', 
                job_title = record[1],
                job_source = 'SnagaJob',
                job_source_url = record[2],
                technologies = '',
                job_description = '',
                email = '',
                phone = '',
                linkedin = '',
                address = record[4],
                job_type = record[3],
                employee_range = '', 
                job_posted_date ='',
                status = 0,
                created_at = datetime.datetime.now()
            )
            instance.save()
    return render(request, 'snagajob.html')

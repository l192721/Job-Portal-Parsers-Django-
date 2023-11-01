from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from base.models import Lead
import datetime
import random

def index(request):
    headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-X906C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://google.com',
        'DNT': '1'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://startup.jobs/',
        'DNT': '2',
        'John': 'subtomplease'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://bing.com',
        'DNT': '1',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://ask.com',
        'DNT': '1',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://startup.jobs/',
        'DNT': '1',
    },
    {
        'User-Agent': 'Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://duckduckgo.com',
        'DNT': '1',
    },
    {
        'User-Agent': 'Roku4640X/DVP-7.70 (297.70E04154A)',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://startup.jobs/',
        'DNT': '1',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://google.com',
        'DNT': '1',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; AFTWMST22 Build/PS7233; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.152 Mobile Safari/537.36',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://bing.com',
        'DNT': '1',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox Series X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36 Edge/20.02',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://startup.jobs/',
        'DNT': '1',
    }
    ]

    # # Scraping Categories (Job Types and Links)
    # URL = "https://startup.jobs/tags"
    # page = requests.get(URL, headers=headers[random.randint(0,9)])
    # soup = BeautifulSoup(page.content, "html.parser")
    # categs = soup.find_all('a', class_='tag')

    # # Making a list of Categories i.e. [[Catergory_1, URL], [Catergory_2, URL],............[Catergory_N, URL]]
    # categories = []
    # for categ in categs:
    #     url = 'https://startup.jobs' + categ['href']
    #     name = categ.text.replace('\n', ' ')
    #     category = [name, url]
    #     categories.append(category)
    
    # Scraping Jobs from each category and stroing in a new list
    results = []
    for x in range(1, 7):
        URL = 'https://startup.jobs/?q=developer&remote=true&c=Contractor&page=f"x"'
        page = requests.get(URL, headers=headers[random.randint(0,9)])
        soup = BeautifulSoup(page.content, "html.parser")
        jobs = soup.find_all('div', class_='postCard')
        
        if len(jobs) > 1:
            for job in jobs:
                company_name = job.find('div', attrs={'class':'postCard__companyName'})
                company_name = company_name.find('a').text
                job_title = job.find('a', class_='postCard__title').text
                job_location = job.find('div', class_='postCard__location').text.replace('\n', '')
                technologies = job.find('div', class_='postCard__tags').text.replace('\n', '')
                job_url = 'https://startup.jobs' + job.find('a', class_='postCard__title')['href']
                result = [job_title, company_name, technologies, job_location, job_url]
                results.append(result)
        else:
            pass
    
    # Inserting Each Job in DB
    for record in results:
        flag = Lead.objects.filter(job_source_url = record[4]) & Lead.objects.filter(job_title = record[0])
        if flag.exists():
            continue
        else:
            instance = Lead(
                company_name = record[1], 
                client_name = '', 
                job_title = record[0],
                job_source = 'startupjobs',
                job_source_url = record[4],
                technologies = record[2],
                job_description = '',
                email = '',
                phone = '',
                linkedin = '',
                address = record[3],
                job_type = '',
                employee_range = '', 
                job_posted_date = '',
                status = 0,
                created_at = datetime.datetime.now()
            )
            instance.save()

    return render(request, 'startupjobs_index.html', {'results': results})
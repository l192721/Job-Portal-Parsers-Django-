from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from base.models import Lead
import datetime
import random
import time

def index(request):
    #Scraping Script
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

    for x in range(1, 20):
        url = 'https://getwork.com/search/results/developer-jobs-in-usa?title_contains=remote&distance=100&pageNum=f"x"'
        time.sleep(5)
        page = requests.get(url, headers=headers[random.randint(0,9)])

        soup = BeautifulSoup(page.content, "html.parser")
        time.sleep(5)
        jobs = soup.find_all('div', class_='row job-listing sponsored-clickable') + soup.find_all('div', class_='row job-listing job-listing-clickable')
        res = []
        for job in jobs:
            time.sleep(10)
            try:
                description = job.find('div', class_='row m-b-0 hide-on-med-and-down').text
            except:
                description = ''
            try:
                date_posted = job.find('div', class_='f-s-14 text-right').text
            except:
                date_posted = ''
            try:
                title = job.find('h4', class_='search-result-link non-organic-link').text
            except:
                title = ''
            try:
                company_name = job.find('span', class_='semi-bold').text
            except:
                company_name = ''
            try:
                address = job.find('div', class_='f-s-14').text
            except:
                address = ''
            try:
                url = job['data-job-url']
                if url.startswith('https'):
                    continue
                else:
                    url = 'https://getwork.com' + url
            except:
                url=''
            job = [title, company_name, address, description, date_posted, url]
            res.append(job)

    # Inserting Each Job in DB
    for record in res:
        flag = Lead.objects.filter(job_source_url = record[5]) & Lead.objects.filter(job_posted_date = record[4])
        if flag.exists():
            continue
        else:
            instance = Lead(
                company_name = record[1], 
                client_name = '', 
                job_title = record[0],
                job_source = 'GetWork',
                job_source_url = record[5],
                technologies = '',
                job_description = record[3],
                email = '',
                phone = '',
                linkedin = '',
                address = record[2],
                job_type = '',
                employee_range = '', 
                job_posted_date = record[4],
                status = 0,
                created_at = datetime.datetime.now()
            )
            instance.save()
    return render(request, '_index.html')
from django.shortcuts import render
from audioop import add
from importlib import import_module
from django import urls
from django.shortcuts import redirect, render
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from base.models import Lead


def home(request):
    return render(request,"flexjob/index.html")

def button(request):
    data='https://www.flexjobs.com/search?search=python&location=New+york'
    url=str(data)
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    #Extraxting Job Titles Here:-
    parent= soup.find_all('a',class_="job-title job-link")
    titles=[]
    for x in parent:
        titles.append(x.getText())

    
    #Extracting company urlss here
    parent= soup.find_all('a',class_="job-title job-link")
    urls=[]
    for x in parent:
        if 'href' in x.attrs:
            urls.append("https://www.flexjobs.com/"+ x.attrs['href'])
         
    #Extracting Time
    parent= soup.find_all('div',class_="job-age")
    Times=[]
    for x in parent:
        Times.append(x.getText())

    #Extrading job descriptions
    parent=soup.find_all('div', class_="job-description")
    desc=[]
    for x in parent:
        desc.append(x.getText())

    
    for x in range(0,len(titles)):
        cl=Lead.objects.filter(job_source_url=urls[x])
        if(cl.exists()):
            continue
        else:
                ins = Lead(job_title=titles[x],job_posted_date=Times[x],job_source_url=urls[x])
                ins.save()
    return render(request,"flexjob/button.html",{'data': "DONE"})
    

 
    

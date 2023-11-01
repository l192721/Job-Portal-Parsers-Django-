from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from slack.models import JOB
from base.models import Lead


class JOBS: 
    def __init__(self,title, address, url): 
        self.title = title 
        self.address = address
        self.url=url
        

# Create your views here.

def home(request):
    return render(request,"slack/index.html")


def button(request):
    data='https://slack.com/careers'
    #data=request.POST.get('search')
    url=str(data)
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    #Extraxting Job Titles Here:-
    headings = soup.find_all('td',class_="job-listing__table--title-col for-desktop-only--table-cell")
    job_titles=[]
    for x in headings:
        job_titles.append(x.getText())
        
    #Extracting Addresses here
    headings = soup.find_all('td',class_="job-listing__table--location-col for-desktop-only--table-cell")
    address=[]
    for x in headings:
       address.append(x.getText())
       
    #Extracting Job Source URLs here
    headings = soup.find_all('a',class_="o-section--feature__link")
    URLs=[]
    for x in headings:
        if 'href' in x.attrs:
            URLs.append(x.attrs['href'])
            
    URLs.pop(0)
    URLs.pop(0)
    
    List_of_Jobs=[] 
    for x in range(0,len(job_titles)):
        List_of_Jobs.append("Job Title: " + job_titles[x])
        List_of_Jobs.append("Address: " + address[x])
        List_of_Jobs.append("Job Source URL: " + URLs[x])
        
        #DB working
        currentLead = Lead.objects.filter(job_source_url=URLs[x])
        if (currentLead.exists()):
            continue
        else:
            ins = Lead(job_title=job_titles[x],address=address[x],job_source_url=URLs[x])
            ins.save()
    return render(request,"slack/button.html",{'data': List_of_Jobs})
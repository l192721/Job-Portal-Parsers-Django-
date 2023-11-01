from audioop import add
from importlib import import_module
from wsgiref import headers
from django.shortcuts import redirect, render
import requests
from bs4 import BeautifulSoup
from base.models import Lead

# Create your views here.

def home(request):
    return render(request,"glassdoor/index.html")

def button(request):
    
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    html=requests.get('https://www.glassdoor.com/Job/new-york-jobs-SRCH_IL.0,8_IC1132348.htm',headers=headers)
    bsobj = BeautifulSoup(html.content, 'lxml')
    
    url_list=[]
    for i in range (1,6):
        url = 'https://www.glassdoor.com/Job/new-york-jobs-SRCH_IL.0,8_IC1132348.htm?p='+str(i)
        
        
        
    #Extracting Job Titles Here:-
    headings = bsobj.find_all('a',attrs={"class":"jobLink job-search-key-1rd3saf eigr9kq1","data-test":"job-link"})
    titles=[]
    for x in headings:
      titles.append(x.getText())      
                   


    #Extracting Company Names Here:-
    headings = bsobj.find_all('div',attrs={"class":"d-flex justify-content-between align-items-start"})
    coyname=[]
    for x in headings:
        coyname.append(x.getText()) 


    #Extracting Job locations here
    headings = bsobj.find_all('span' ,class_="css-1buaf54 pr-xxsm job-search-key-iii9i8 e1rrn5ka4")
    locations=[]
    for x in headings:
        locations.append(x.getText()) 
        
                
            
            
    #Extracting Job Source URLs here
    headings = bsobj.find_all('a',attrs={"class":"jobLink job-search-key-1rd3saf eigr9kq1","data-test":"job-link"})
    URLs=[]
    for x in headings:
        if 'href' in x.attrs:
            URLs.append("https://www.glassdoor.com"+x.attrs['href'])        


             
    #Extracting Time
    headings = bsobj.find_all('div',attrs={"data-test":"job-age"})
    times=[]
    for x in headings:
        times.append(x.getText())
        
        
    #DB working    
    for x in range(0,len(titles)):
        currentLead = Lead.objects.filter(job_source_url=URLs[x])
        if (currentLead.exists()):
            continue
        else:
            ins = Lead(job_title=titles[x],address=locations[x],job_source_url=URLs[x],company_name=coyname[x],job_posted_date=times[x])
            ins.save()
    return render(request,"glassdoor/button.html",{'data': "Data Entered Successfully to DB"})
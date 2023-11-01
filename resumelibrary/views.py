from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from slack.models import JOB
from base.models import Lead

def home(request):
    return render(request,"resumelibrary/index.html")

def button(request):
    
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    html=requests.get('https://www.resume-library.com/jobs/developer-in-new-york-city-ny?pp=250&pd=1&job_type=Contract&order_by=date',headers=headers)
    bsobj = BeautifulSoup(html.content, 'lxml')
    
    url_list=[]
    for i in range (1,6):
        url = 'https://www.resume-library.com/jobs/developer-in-new-york-city-ny?pp=250&pd=1&job_type=Contract&order_by=date?p='+str(i)
        
        

    #Extracting Job Titles Here:-
    headings = bsobj.find_all('h2',attrs={"class":"search-result-info-title"})
    titles=[]
    for x in headings:
      titles.append(x.getText())      
                   


    #Extracting Company Names Here:-
    headings = bsobj.find_all('p',attrs={"class":"search-result-info-posted"})
    temp=[]
    for x in headings:
        temp.append(x.getText()) 
        
    coyname=[]
    for x in range (0,len(temp)):
            f=temp[x].split('by\n ')
            coyname.append(f[1])



    #Extracting Job locations here
    headings = bsobj.find_all('dd',attrs={"search-result-info-desc desc--location"})
    locations=[]
    for x in headings:
        locations.append(x.getText()) 
        
            
            

    #Extracting Description
    headings = bsobj.find_all('p',attrs={"class":"search-result-description"})
    Description=[]
    for x in headings:
        Description.append(x.getText())
                        
            
            
    #Extracting Job Source URLs here
    headings = bsobj.find_all('a',attrs={"class":"search-network-job-title-link"})
    URLs=[]
    for x in headings:
        URLs.append('https://www.resume-library.com'+x.attrs['href'])
        
        
    for x in range(0,len(titles)):
        
        #DB working
        currentLead = Lead.objects.filter(job_source_url=URLs[x])
        if (currentLead.exists()):
            continue
        else:
            ins = Lead(job_title=titles[x],company_name=coyname[x],address=locations[x],job_source_url=URLs[x],job_description=Description[x])
            ins.save()
     
    return render(request,"resumelibrary/button.html",{'data': "Data Entered Successfully to DB"})
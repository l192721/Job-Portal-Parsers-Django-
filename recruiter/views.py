from audioop import add
from importlib import import_module
from django.shortcuts import redirect, render
import requests
from bs4 import BeautifulSoup
from base.models import Lead



# Create your views here.

def home(request):
    return render(request,"recruiter/index.html")

def button(request):
    
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    html=requests.get('https://jobs.recruiter.com/crypto-jobs/search?utf8=%E2%9C%93&keyword=developer&location=new+york',headers=headers)
    bsobj = BeautifulSoup(html.content, 'lxml')
    
    url_list=[]
    for i in range (1,6):
        url = 'https://jobs.recruiter.com/crypto-jobs/search?utf8=%E2%9C%93&keyword=developer&location=new+york?p='+str(i)
        
        
        
        
    #Extracting Job Titles Here:- 
    headings = bsobj.find_all('div',attrs={"class":"job-info-container"})
    titles=[]
    for x in headings:
      titles.append(x.contents[1].getText())     

               
               
                   
    #Extracting Company Names Here:-
    headings = bsobj.find_all('div',class_="job-info-container")
    temp=[]
    for x in headings:
      temp.append(x.p.text)
    
    coyname=[]
    for x in range (0,len(temp)):
            f=temp[x].split('-')
            coyname.append(f[0])
      


    #Extracting Job locations here
    headings = bsobj.find_all('span',attrs={"class":"location"})
    addresses=[]
    for x in headings:
        addresses.append(x.getText()) 
         
    locations=[]
    counter=-1
    for y in addresses:
        counter=counter+1
        if(counter%3==0):
            locations.append(y)
            




    #Extracting Descriptions here
    headings = bsobj.find_all('span',attrs={"class":"location"})
    addresses=[]
    for x in headings:
        addresses.append(x.getText())
    addresses.pop(0)
    addresses.pop(0)
    Descriptions=[]
    counter=-1
    for y in addresses:
        counter=counter+1
        if(counter%3==0):
            Descriptions.append(y)
          
            
    #Extracting Job Source URLs here
    headings = bsobj.find_all('div',attrs={"class":"job-info-container"})
    URLs=[]
    for x in headings:
        URLs.append('https://jobs.recruiter.com/'+x.a['href'])
        
    
    for x in range(0,len(titles)):
        #DB working
        currentLead = Lead.objects.filter(job_source_url=URLs[x])
        if (currentLead.exists()):
            continue
        else:
            ins = Lead(job_title=titles[x],address=locations[x],job_source_url=URLs[x],company_name=coyname[x],job_description=Descriptions[x])
            ins.save()    
     
     
    return render(request,"recruiter/button.html",{'data': "Data Entered Successfully to DB"})
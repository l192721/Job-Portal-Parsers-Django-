from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from base.models import Lead


# Create your views here.

def home(request):
    return render(request,"linkedin/index.html")

def button(request):
    
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    html=requests.get('https://www.linkedin.com/jobs/search?keywords=Developer&location=New%20York%2C%20New%20York%2C%20United%20States&locationId=&geoId=102571732&f_TPR=r86400&distance=25&f_JT=C&f_WT=2&f_C=16127%2C15228%2C934754%2C11219&position=1&pageNum=0',headers=headers)
    bsobj = BeautifulSoup(html.content, 'lxml')
    
    url_list=[]
    for i in range (1,6):
        url = 'https://www.linkedin.com/jobs/search?keywords=Developer&location=New%20York%2C%20New%20York%2C%20United%20States&locationId=&geoId=102571732&f_TPR=r86400&distance=25&f_JT=C&f_WT=2&f_C=16127%2C15228%2C934754%2C11219&position=1&pageNum=0?p='+str(i)
        

    #b=bsobj.find('div',attrs={"class":"base-search-card__info"})
    #Extraxting Job Titles here
    headings = bsobj.find_all('h3', class_="base-search-card__title")
    titles=[]
    for x in headings:
        titles.append(x.getText())
        


    #Extracting company names here
    headings = bsobj.find_all('a',class_="hidden-nested-link")
    coyname=[]
    for x in headings:
        coyname.append(x.getText())
    

    
            
        
    #Extracting Job locations here
    headings = bsobj.find_all('span',class_="job-search-card__location")
    locations=[]
    for x in headings:
        locations.append(x.getText())
    
    
    
       
    #Extracting Time
    headings = bsobj.find_all('time',attrs={"class":"job-search-card__listdate--new"})
    times=[]
    for x in headings:
        times.append(x['datetime'])
        
        
        
               
    #Extracting Job Source URLs here
    headings = bsobj.find_all('a', class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]")
    URLs=[]
    for x in headings:
        if 'href' in x.attrs:
            URLs.append(x.attrs['href'])


            
    
    for x in range(0,len(titles)):
        #DB working
        currentLead = Lead.objects.filter(job_source_url=URLs[x])
        if (currentLead.exists()):
            continue
        else:
            currentLead = Lead.objects.filter(job_title=titles[x],job_posted_date=times[x],company_name=coyname[x],address=locations[x])
            if(currentLead.exists()):
               continue
            else:
                ins = Lead(job_title=titles[x],address=locations[x],job_source_url=URLs[x],company_name=coyname[x],job_posted_date=times[x])
                ins.save()
    return render(request,"linkedin/button.html",{'data': "Record Updated Successfully in DB"})
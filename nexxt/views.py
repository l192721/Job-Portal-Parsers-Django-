from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from base.models import Lead


# Create your views here.

def home(request):
    return render(request,"nexxt/index.html")

def button(request):
    data='https://www.nexxt.com/jobs/search?k=&l=new+york'
    #data=request.POST.get('search')
    url=str(data)
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    
    
    #Extraxting Job Titles Here:-
    headings = soup.find_all('h2' ,class_="h3 theme-primary-link-color no-margin")
    titles=[]
    for x in headings:
        titles.append(x.getText())
    l=len(titles)   
    titles.pop(l-1) 
        
        



    #Extracting company names here
    headings = soup.find_all('span',class_="job-title-company")
    coyname=[]
    for x in headings:
        coyname.append(x.getText())
    l=len(coyname)   
    coyname.pop(l-1)
    l=len(coyname)   
    coyname.pop(l-1)
    
    
    
            
        
    #Extracting Job locations here
    headings = soup.find_all('div',class_="job-header-sub job-header-sub-cards")
    locations=[]
    for x in headings:
        locations.append(x.contents[2].getText())   
    l=len(locations)
    locations.pop(l-1)
    
    
    
    
       
    #Extracting Description
    headings = soup.find_all('div',attrs={"class":"hidden-xs"})
    Description=[]
    for x in headings:
        Description.append(x.getText())
        
        
        
               
    #Extracting Job Source URLs here
    headings = soup.find_all('a', attrs={"class":"job-title","byd-uxc":"Job", "byd-uxn":"Title"})
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
            ins = Lead(job_title=titles[x],address=locations[x],job_source_url=URLs[x],company_name=coyname[x],job_description=Description[x])
            ins.save()
    return render(request,"nexxt/button.html",{'data': "Record Updated Successfully in DB"})
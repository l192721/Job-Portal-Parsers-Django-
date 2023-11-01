"""gfg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('', include('base.urls')),
    path('admin/', admin.site.urls),

    # Mashable Job Portal 
    path('mashable', include('mashable.urls')),

    # F6S Job Portal 
    path('f6s', include('f6s.urls')),
    # Monster Job Portal 
    path('monster', include('monster.urls')),
    # Monster Job Portal 
    path('snagajob', include('snagajob.urls')),
    # SatrupJobs Job Portal
    path('dice/', include('dice.urls')),
    # Indeed Job Portal 
    path('indeed', include('indeed.urls')),
    # GetWork Job Portal 
    path('getwork', include('getwork.urls')),
    # SatrupJobs Job Portal
    path('startupjobs/', include('startupjobs.urls')),
    # Workable Job Portal 
    path('workable', include('workable.urls')),
    # Itjobpro
    path('itjobpro',include('itjobpro.urls')),
    # Glassdoor
    path('glassdoor/', include('glassdoor.urls')),        
    # Career Builders
    path('careerbuilder/',include('careerbuilder.urls')),
    # FlexJobs
    path('flexjob/',include('flexjob.urls')),
    # Linkedin
    path('linkedin/', include('linkedin.urls')),
    # Nexxt 
    path('nexxt/', include('nexxt.urls')),
    # Resume Library
    path('resumelibrary/', include('resumelibrary.urls')), 
    # Recruiter
    path('recruiter/', include('recruiter.urls')),    
]


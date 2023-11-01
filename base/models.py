from django.db import models

# Create your models here.
class Lead(models.Model):
    company_name = models.CharField(max_length=191, null=True, blank=True)
    client_name = models.CharField(max_length=100, null=True, blank=True)
    job_title = models.CharField(max_length=191, null=True, blank=True)
    job_source = models.CharField(max_length=50, null=True, blank=True)
    job_source_url = models.CharField(max_length=191, null=True, blank=True)
    technologies = models.CharField(max_length=191, null=True, blank=True)
    job_description = models.CharField(max_length=191, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    linkedin = models.CharField(max_length=191, null=True, blank=True)
    address = models.CharField(max_length=191, null=True, blank=True)
    job_type = models.CharField(max_length=20, null=True, blank=True)
    employee_range = models.CharField(max_length=30, null=True, blank=True)
    job_posted_date = models.CharField(max_length=20, null=True, blank=True)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

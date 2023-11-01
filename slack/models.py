from django.db import models

# Create your models here.

class JOB(models.Model):
    title = models.CharField(max_length=100)
    address = models.TextField()
    url = models.TextField()
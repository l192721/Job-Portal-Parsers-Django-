# Generated by Django 4.0.4 on 2022-07-20 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=191, null=True)),
                ('client_name', models.CharField(blank=True, max_length=100, null=True)),
                ('job_title', models.CharField(blank=True, max_length=191, null=True)),
                ('job_source', models.CharField(blank=True, max_length=50, null=True)),
                ('job_source_url', models.CharField(blank=True, max_length=191, null=True)),
                ('technologies', models.CharField(blank=True, max_length=191, null=True)),
                ('job_description', models.CharField(blank=True, max_length=191, null=True)),
                ('email', models.CharField(blank=True, max_length=30, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=191, null=True)),
                ('address', models.CharField(blank=True, max_length=191, null=True)),
                ('job_type', models.CharField(blank=True, max_length=20, null=True)),
                ('employee_range', models.CharField(blank=True, max_length=30, null=True)),
                ('job_posted_date', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]

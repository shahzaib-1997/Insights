from django.db import models
from django.contrib.auth.models import User



class Currency(models.Model):
    name = models.CharField(max_length=20)

class Company(models.Model):
    name = models.CharField(max_length=255)
    default_currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1)

class CompanyDetail(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=8)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

class company_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

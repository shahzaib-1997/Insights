from django.db import models


# Create your models here.
class AccountTypes(models.Model):
    name = models.CharField(null=True, max_length=255)


class Tax(models.Model):
    tax_name = models.CharField(max_length=100)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)


class AccountTypeDetails(models.Model):
    account_type = models.ForeignKey(
        AccountTypes, on_delete=models.CASCADE, related_name="detail_types"
    )
    name = models.CharField(null=True, max_length=255)


class Account(models.Model):
    name = models.CharField(null=True, max_length=255)
    description = models.CharField(null=True, max_length=255)
    sub_account = models.BooleanField(default=False)
    sub_account_id = models.IntegerField(null=True)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, related_name="accounts")
    balance = models.FloatField(null=True)
    as_of_date = models.DateField(null=True)

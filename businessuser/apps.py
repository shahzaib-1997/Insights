from django.apps import AppConfig


class BusinessuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'businessuser'
    dependencies = ['companydetails']

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('', login, name='login'),
    path('logout/', logoutt, name='logout'),
    path('signup/', signup, name='signup'),
    path('company_create/', company_create, name='company_create'),
    path('forget_password/', forget_password, name='forget_password'),
    path('otp/', verify_otp_view, name='verify_otp_view'),
    path('reset_password_view', reset_password_view, name='reset_password_view'),
    path('sales/', sales, name='sales'),
    path('invoice/', invoice, name='invoice'),
    path('expense/', expense, name='expense'),
    path('customer/', customer, name='customer'),
    path('supplier/', supplier , name = 'supplier'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
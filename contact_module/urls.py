from django.urls import path
from . import views

urlpatterns=[
    path('',views.ContactUsView,name='contact_us_page')
]
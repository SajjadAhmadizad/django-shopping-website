from django.urls import path
from home_module import views

urlpatterns = [
    path('',views.index,name='home_page')
]
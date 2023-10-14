from django.urls import path
from . import views

urlpatterns = [
    path('',views.UserDashboardView,name='user_dashboard_page'),
    path('order-list/',views.PurchasedProducts,name='orders_page'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('add-product-to-order',views.AddProductToOrder,name='add_product_to_order'),
    path('change-product-count',views.ChangeProductCount,name='change_product_count'),
    path('delete-product',views.DeleteProduct,name='delete_product'),
    path('',views.OrdersListView,name='orders_list_page'),
]
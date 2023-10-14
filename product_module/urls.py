from django.urls import path
from product_module import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list_page'),
    path('category/<cat>', views.ProductListView.as_view(), name='product_category_page'),
    path('delete-product-comment/', views.DeleteProductComment, name='delete_product_comment'),
    path('search-product-component/', views.SearchProductComponent, name='search_product_component'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail_page'),
]

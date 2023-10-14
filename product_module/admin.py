from django.contrib import admin
from . import models
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price','create_date']
    list_filter = ['is_active','is_delete','category','brand']

admin.site.register(models.ProductCategory)
admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.ProductTags)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductGallery)
admin.site.register(models.ProductVisitModel)
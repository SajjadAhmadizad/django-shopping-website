from django.db.models import Min
from django.shortcuts import render

from product_module.models import ProductCategory
from site_module.models import SiteModel


# Create your views here.

def index(request):
    site = SiteModel.objects.filter(is_active=True).first()
    categories = ProductCategory.objects.annotate(min_price=Min('product__price')).filter(image__isnull=False).all()[:9]

    product_list = []
    for category in categories:
        cheapest_product = category.product_set.order_by('price').first()
        if cheapest_product:
            product_list.append({
                'category': category,
                'cheapest_product': cheapest_product
            })
    return render(request, 'home_module/index.html',
                  {'copy_right': site.copy_right, 'address': site.address, 'phone': site.phone, 'product_list':product_list})

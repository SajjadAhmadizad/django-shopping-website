import requests.utils
from django.db.models import Max, Q, Count
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView

from account_module.models import User
from order_module.models import Order, OrderItems
from product_module.forms import ProductCommentModelForm
from product_module.models import Product, ProductCategory, ProductTags, ProductBrand, ProductGallery, \
    ProductVisitModel, ProductCommentModel, ProductCommentLikeModel
from utils.convertor import group_list
from utils.http_service import get_client_ip


# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'product_module/product-list.html'

    def get_paginate_by(self, queryset):
        request = self.request
        url_paginate_by = request.GET.get('paginate_by')
        if url_paginate_by == '2' or url_paginate_by == '12' or url_paginate_by == '24' or url_paginate_by == '48':
            if url_paginate_by != request.session.get('paginate_by'):
                request.session['paginate_by'] = url_paginate_by
                request.session.save()
        return request.session.get('paginate_by', 2)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        context['categories'] = ProductCategory.objects.prefetch_related('productcategory_set').filter(parent=None)
        context['selected_category'] = ProductCategory.objects.prefetch_related('parent').filter(
            url_title=self.kwargs.get('cat')).first()
        # =-=-=-=-==-=-=-===-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-
        request: HttpRequest = self.request
        url_display = request.GET.get('list-display')
        session_display = request.session.get('display')
        if url_display == 'list' or url_display == 'normal':
            if url_display != session_display:
                request.session['display'] = url_display
                request.session.save()
        context['display'] = request.session.get('display')
        # =-=-=-=-==-=-=-===-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-
        brands = ProductBrand.objects.all()
        selected_brands = request.GET.get('brands')
        brands_for_fill_checkboxes = selected_brands
        if selected_brands:
            selected_brands = selected_brands.split(',')
            context['selected_brands'] = selected_brands
            context['brands_for_fill_checkboxes'] = brands_for_fill_checkboxes
        context['brands'] = brands
        # =-=-=-=-==-=-=-===-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-
        context['selected_order_by'] = request.GET.get('order_by')
        # =-=-=-=-==-=-=-===-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-
        max_db_price = Product.objects.aggregate(Max('price'))['price__max'] or 9990000
        context['max_db_price'] = max_db_price
        context['max_value_price'] = request.GET.get('max_price', max_db_price)
        context['min_value_price'] = request.GET.get('min_price', 0)
        # =-=-=-=-==-=-=-===-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-
        # search
        search_text = self.request.GET.get('q')
        if search_text is not None and search_text != '':
            context['search_text'] = search_text

        return context

    def get_queryset(self, **kwargs):
        data = super().get_queryset(**kwargs)
        category_name = self.kwargs.get('cat')
        data.filter(is_active=True, is_delete=False).all()
        if category_name:
            category: ProductCategory = ProductCategory.objects.filter(url_title=category_name).values(('url_title'))
            category = [category]
            data = data.filter(Q(category__url_title__in=category) | Q(category__parent__url_title__in=category))
        # =-=-=-=-==-=-=-===-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-
        brands = self.request.GET.get('brands')
        if brands:
            brands: list = brands.split(',')  # example : ['samsung', 'apple']
            if len(brands) == 0:
                return data
            else:
                data = data.filter(brand__url_title__in=brands)
        # =-=-=-=-==-=-=-===-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-
        order_by = self.request.GET.get('order_by')
        if order_by == 'گران ترین':
            data = data.order_by('-price')
        elif order_by == 'ارزان ترین':
            data = data.order_by('price')
        elif order_by == 'تاریخ':
            data = data.order_by('create_date')
        elif order_by == 'پربازدید ترین':
            data = data.annotate(visit_count=Count('productvisitmodel')).order_by('-visit_count')
        # =-=-=-=-==-=-=-===-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price is not None:
            data = data.filter(price__gte=min_price)
        if max_price is not None:
            data = data.filter(price__lte=max_price)
        # =-=-=-=-==-=-=-===-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-
        # search
        search_text = self.request.GET.get('q')
        if search_text is not None and search_text != '':
            data = data.filter(
                Q(title__icontains=search_text) |
                Q(title__startswith=search_text) |
                Q(title__endswith=search_text) |
                Q(title__isnull=True) |
                Q(slug__icontains=search_text) |
                Q(slug__startswith=search_text) |
                Q(slug__endswith=search_text)
            ).all()
        return data


class ProductDetailView(DetailView):
    template_name = 'product_module/product-detail.html'
    model = Product

    def post(self, request, *args, **kwargs):
        # ======================like : =======================
        request = self.request
        liked_comment_id = request.POST.get('comment_id') or -1
        if request.user.is_authenticated and liked_comment_id != -1 and liked_comment_id.isdigit():
            deleted_count, deleted_item = ProductCommentLikeModel.objects.filter(comment_id=int(liked_comment_id),
                                                                                 user_id=request.user.id).delete()
            comment = ProductCommentModel.objects.filter(id=int(liked_comment_id)).first()
            if deleted_count == 0:
                new_like = ProductCommentLikeModel(user_id=request.user.id, comment_id=comment.id)
                new_like.save()
                like_count = ProductCommentModel.objects.annotate(count=Count('productcommentlikemodel')).filter(
                    id=comment.id).first()
                return JsonResponse(
                    {'status': 'success', 'comment_id': comment.id, 'count': like_count.count}
                )
            else:
                like_count = ProductCommentModel.objects.annotate(count=Count('productcommentlikemodel')).filter(
                    id=comment.id).first()
                return JsonResponse(
                    {'status': 'success', 'comment_id': comment.id, 'count': like_count.count}
                )

        # =======================comment : ====================
        loaded_product_slug = self.kwargs.get('slug')
        find_product_by_slug: Product = Product.objects.filter(slug__iexact=loaded_product_slug).first()
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': 'not_auth'
            })
        if find_product_by_slug is not None:
            comment_form = ProductCommentModelForm(self.request.POST)
            if comment_form.is_valid():
                # -------- for reply : --------------------
                try:
                    parent: ProductCommentModel = ProductCommentModel.objects.filter(id=int(request.POST.get('parent')),
                                                                                     product_id=find_product_by_slug.id).first()
                    parent = parent.id
                except:
                    parent = None
                new_comment = ProductCommentModel(product_id=find_product_by_slug.id,
                                                  user_id=request.user.id, comment=request.POST.get('comment'),
                                                  parent_id=parent)
                new_comment.save()
                comments = ProductCommentModel.objects.prefetch_related('productcommentmodel_set').filter(
                    product_id=find_product_by_slug.id, parent_id=None).all().order_by('-create_date')
                return JsonResponse({
                    'status': 'success',
                    'body': render_to_string('product_module/component/comments_area_component.html',
                                             {'comments': comments, 'request': request, 'csrf': get_token(request)})
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': comment_form.errors
                })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'مشکلی در ثبت کامنت وجود دارد'
            })

    def get_queryset(self, **kwargs):
        data = super().get_queryset(**kwargs)
        data.filter(is_active=True, is_delete=False)
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        images = list(ProductGallery.objects.filter(product_id=loaded_product.id))
        images.insert(0, loaded_product)
        context['product_list_gallery'] = group_list(images[0:4], 4)

        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            order, x = Order.objects.get_or_create(user_id=user_id, is_paid=False)
            order_item: OrderItems = OrderItems.objects.filter(order_id=order.id, product_id=loaded_product.id).first()
            if order_item is not None:
                context['count_in_order'] = order_item.count
                context['order_item'] = order_item.id
            else:
                context['count_in_order'] = 0
        # =-=-=-=-==-=-=-===-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-
        user_ip = get_client_ip(self.request)
        user = None
        if self.request.user.is_authenticated:
            user = User.objects.filter(id=self.request.user.id).first()
            has_been_visited = ProductVisitModel.objects.filter(user_id=user.id, product_id=loaded_product.id).exists()
            if not has_been_visited:
                new_visit = ProductVisitModel(user_id=user.id, ip=user_ip, product_id=loaded_product.id)
                new_visit.save()
        else:
            has_been_visited = ProductVisitModel.objects.filter(ip=user_ip, product_id=loaded_product.id).exists()
            if not has_been_visited:
                new_visit = ProductVisitModel(ip=user_ip, product_id=loaded_product.id)
                new_visit.save()
        # =-=-=-=-==-=-=-===-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-
        context['comment_form'] = ProductCommentModelForm()
        context['comments'] = ProductCommentModel.objects.prefetch_related('productcommentmodel_set').filter(
            product_id=loaded_product.id, parent=None).annotate(
            like_count=Count('productcommentlikemodel')).order_by('-create_date').all()
        # =-=-=-=-==-=-=-===-=---=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-

        return context


def DeleteProductComment(request):
    if request.method == "GET":
        # =======================delete comment : ====================
        comment_id = request.GET.get('commentId') or -1
        if comment_id != -1 and comment_id.isdigit():
            comment_id = int(comment_id)
            comment:ProductCommentModel = ProductCommentModel.objects.filter(id=comment_id, user_id=request.user.id).first()
            deleted_comment_count, dict = ProductCommentModel.objects.filter(id=comment_id,
                                                                             user_id=request.user.id).delete()
            if deleted_comment_count >= 1:

                comments = ProductCommentModel.objects.prefetch_related('productcommentmodel_set').filter(
                    product_id=comment.product_id, parent=None).annotate(
                    like_count=Count('productcommentlikemodel')).order_by('-create_date').all()
                return JsonResponse({
                    'status': 'success',
                    'icon': 'success',
                    'message': 'کامنت مورد نظر با موفقیت حذف شد',
                    'body': render_to_string('product_module/component/comments_area_component.html',
                                             {'comments': comments, 'request': request, 'csrf': get_token(request)})
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'icon': 'error',
                    'message': 'مقدار وارد شده نادرست است'
                })
        else:
            return JsonResponse({
                'status': 'error',
                'icon': 'error',
                'message': 'مقدار وارد شده نادرست است'
            })
    else:
        return JsonResponse({
            'status': 'error',
            'icon': 'error',
            'message': 'ابتدا وارد شوید!'
        })


def SearchProductComponent(request):
    if request.method == 'POST':
        text = request.POST.get('product-search')
        if text is not None:
            founded_products = Product.objects.filter(
                Q(title__icontains=text) |
                Q(title__startswith=text) |
                Q(title__endswith=text) |
                Q(title__isnull=True) |
                Q(slug__icontains=text) |
                Q(slug__startswith=text) |
                Q(slug__endswith=text)
            ).all()[:4]
        return JsonResponse({
            'status': "success",
            'body': render_to_string('components/site_header_search_bar_component.html',
                                     {'founded_products': founded_products, 'count': founded_products.count(),
                                      'search_text': text})
        })

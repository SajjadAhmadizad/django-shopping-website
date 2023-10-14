from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from order_module.models import Order, OrderItems
from product_module.models import Product


# Create your views here.
def AddProductToOrder(request):
    product = Product.objects.filter(pk=int(request.GET.get('product_id'))).first()
    if request.user.is_authenticated:
        count = int(request.GET.get('count'))
        if product is not None:
            if count > 0:
                current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
                current_order_items = current_order.orderitems_set.filter(product_id=product.id).first()
                if current_order_items is not None:
                    current_order_items.count += count
                    current_order_items.save()
                    current_count = current_order_items.count
                else:
                    current_order_items = OrderItems(order_id=current_order.id, count=count, product_id=product.id)
                    current_order_items.save()
                    current_count = current_order_items.count
                return JsonResponse({
                    'status': 'success',
                    'order_item_id':current_order_items.id,
                    "message": 'محصول موردنظر با موفقیت به سبد خرید اضافه شد',
                    'current_count':current_count,
                    'icon': 'success',
                    'button': 'باشه!'
                })
            else:
                return JsonResponse({
                    'status': 'count error!',
                    "message": 'تعداد وارد شده برای محصول نامعتبر است!',
                    'icon': 'error',
                })
        else:
            return JsonResponse({
                'status': 'count error!',
                "message": 'محصول موردنظر یافت نشد!',
                'icon': 'error',
            })
    else:
        return JsonResponse({
            'status': 'not auth',
            "message": 'برای افزودن محصول به سبد خرید ابتدا باید در سایت لاگین کنید!',
            'icon': 'warning',
            'button': 'ورود به سایت',
            'redirectTo': reverse('register_page') + '?next=' + product.get_absolute_url()
        })

@login_required
def OrdersListView(request):
    current_order, created = Order.objects.prefetch_related('orderitems_set').get_or_create(user_id=request.user.id,
                                                                                            is_paid=False)
    return render(request, 'order_module/orders_list.html', {'order': current_order})


def ChangeProductCount(request):
    order_items_id = request.GET.get('orderItemsId')
    todo = request.GET.get('todo')
    order_item: OrderItems = OrderItems.objects.filter(id=order_items_id, order__user_id=request.user).first()
    status = 'failed'
    if order_item is not None:
        if todo == 'increase':
            order_item.count+=1
            order_item.save()
            status='success'
        elif todo == 'decrease':
            if order_item.count > 1:
                order_item.count -= 1
                order_item.save()
                status = 'success'
            elif order_item.count <=1:
                order_item.delete()
                status='success'
        if status == 'success':
            current_order, created = Order.objects.prefetch_related('orderitems_set').get_or_create(user_id=request.user.id,is_paid=False)
            return JsonResponse({
                'status':status,
                'body':render_to_string('order_module/component/orders-list-component.html',{'order':current_order})
            })
    else:
        return JsonResponse({
            'message': 'آیتم مئردنظر یافت نشد!',
            'status': status,
            'icon': 'error',
            'button': 'باشه'
        })


def DeleteProduct(request):
    deleted_count,deleted_dict = OrderItems.objects.filter(id=int(request.GET.get('orderItemsId')),order__user_id=request.user.id,order__is_paid=False).delete()
    if deleted_count != 0:
        current_order,created = Order.objects.prefetch_related('orderitems_set').get_or_create(is_paid=False,user_id=request.user.id)
        return JsonResponse({
            'm1':'حذف شد!',
            'm2':'محصول موردنظر از سبد خرید حذف شد',
            'status':'success',
            'body':render_to_string('order_module/component/orders-list-component.html',{'order':current_order})
        })
    else:
        return JsonResponse({
            'm1': 'ارور!',
            'm2': 'محصول موردنظر یافت نشد!',
            'status': 'error'
        })
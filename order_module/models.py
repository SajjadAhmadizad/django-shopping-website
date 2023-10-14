from django.db import models
from account_module.models import User
from product_module.models import Product
from jalali_date import datetime2jalali, date2jalali



# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='پرداحت شده/نشده')
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ پرداخت')

    def __str__(self):
        return str(self.user.email) + ' is paid : ' + str(self.is_paid)

    def calculate_total_price(self):
        total = 0
        if self.is_paid:
            for order_item in self.orderitems_set.all():
                total+=order_item.final_price * order_item.count
        else:
            for order_item in self.orderitems_set.all():
                total+=order_item.product.price * order_item.count
        return total

    def jalali_payment_date(self):
        return datetime2jalali(self.payment_date)


    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید کاربران'


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    count = models.IntegerField(verbose_name='تعداد')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت پرداخت شده محصول')

    def __str__(self):
        return str(self.order) + ' ' + str(self.count)

    def get_total_price(self):
        return self.count * self.product.price

    def get_total_price_after_purchased(self):
        return self.count * self.final_price

    class Meta:
        verbose_name = 'جزویات سبد خرید'
        verbose_name_plural = 'جزئیات سبد های خرید کاربران'

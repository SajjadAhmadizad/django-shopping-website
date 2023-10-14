from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from jalali_date import datetime2jalali

from account_module.models import User


# Create your models here.

class ProductCategory(models.Model):
    parent = models.ForeignKey('ProductCategory', null=True, blank=True, verbose_name='والد', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/category-image',default=None,blank=True,null=True,verbose_name='تصویر دسته بندی')
    title = models.CharField(max_length=30, verbose_name='عنوان دسته بندی')
    url_title = models.CharField(max_length=300, verbose_name='عنوان در url')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی محصول'
        verbose_name_plural = "دسته بندی های محصولات"




class ProductTags(models.Model):
    title = models.CharField(max_length=50, verbose_name='تگ')
    url_title = models.CharField(max_length=200, verbose_name='عنوان در url')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = "تگ های محصولات"


class ProductBrand(models.Model):
    title = models.CharField(max_length=50, verbose_name='برند')
    url_title = models.CharField(max_length=200, verbose_name='عنوان در url')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برند محصول'
        verbose_name_plural = "برند های محصولات"


class ProductGallery(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر محصول')


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان محصول')
    short_description = models.CharField(max_length=200, verbose_name='توضیحات کوتاه محصول')
    description = models.TextField(max_length=500, verbose_name='توضیحات اصلی محصول')
    price = models.IntegerField(verbose_name='قیمت محصول')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='دسته بندی محصول')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند محصول')
    tags = models.ManyToManyField(ProductTags, verbose_name='تگ های محصول')
    color = models.CharField(max_length=20, verbose_name='رنگ محصول')
    image = models.ImageField(upload_to='images/product-image', verbose_name='تصویر اصلی محصول')
    slug = models.CharField(max_length=300, verbose_name='اسلاگ', null=False, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال', default=True)
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده/نشده')

    def __str__(self):
        return str(self.title) + " / " + str(self.price)

    # def save(self,*args,**kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args,**kwargs)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = "محصولات"

    def get_absolute_url(self):
        return reverse('product_detail_page', args=[self.slug])


class ProductVisitModel(models.Model):
    ip = models.CharField(max_length=60,verbose_name='آی پی')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر',null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')

    class Meta:
        verbose_name = 'بازدید محصولات'
        verbose_name_plural = 'بازدید های محصولات'

    def __str__(self):
        return str(self.ip) + ' / ' + str(self.user)


class ProductCommentModel(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')
    parent = models.ForeignKey('ProductCommentModel',on_delete=models.CASCADE,null=True,blank=True,verbose_name='والد')
    comment = models.TextField(verbose_name='متن کامنت')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'کامنت محصولات'
        verbose_name_plural = 'کامنت های محصولات'

    def jalali_create_date(self):
        return datetime2jalali(self.create_date)

    def __str__(self):
        return str(self.comment) + ' / ' + str(self.user)


class ProductCommentLikeModel(models.Model):
    comment = models.ForeignKey(ProductCommentModel,on_delete=models.CASCADE,verbose_name='کامنت')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')

    class Meta:
        verbose_name = 'لایک کامنت محصول'
        verbose_name_plural = 'لایک های کامنت های محصولات'

    def __str__(self):
        return str(self.comment.comment) + ' / ' + str(self.user)
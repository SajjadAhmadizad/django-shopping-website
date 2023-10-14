from django.db import models

# Create your models here.

class SiteModel(models.Model):
    site_name = models.CharField(max_length=50,verbose_name='نام سایت')
    domain_name = models.CharField(max_length=50,verbose_name='دامنه سایت')
    copy_right = models.CharField(max_length=50, verbose_name='متن کپی رایت')
    address = models.CharField(max_length=100,verbose_name='آدرس')
    phone = models.IntegerField(verbose_name='تلفن')
    email = models.EmailField(verbose_name='ایمیل')
    telegram = models.CharField(max_length=50,verbose_name="تلگرام")
    twitter = models.CharField(max_length=50,verbose_name="توئیتر")
    instagram = models.CharField(max_length=50,verbose_name="اینستاگرام")
    facebook = models.CharField(max_length=50,verbose_name="فیسبوک")
    pinteres = models.CharField(max_length=50,verbose_name="پینترست")
    rules = models.TextField(max_length=50,verbose_name='قوانین')
    is_active=models.BooleanField(default=False,verbose_name='فعال/غیرفعال')

    class Meta:
        verbose_name='تنظیمات سایت'
        verbose_name_plural='لیست تنظیمات سایت'

    def __str__(self):
        return f'{self.site_name} {self.is_active}'
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('ایمیل باید وارد شود!')
        if not password:
            raise ValueError('پسورد باید وارد شود!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # def create_superuser(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    mobile = models.CharField(max_length=20, unique=False, verbose_name='تلفن همراه')
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی ایمیل')
    username = models.CharField(max_length=40,unique=True,verbose_name='یوزرنیم')
    about_user = models.TextField(blank=True, null=True, verbose_name='درباره کاربر')
    avatar = models.ImageField(upload_to='images/user-profiles',verbose_name='تصویر آواتار',default=None,blank=True,null=True)
    address = models.TextField(verbose_name='آدرس',default=None,null=True,blank=True)
    last_reset_password_date = models.DateTimeField(auto_now_add=False,null=True,blank=True,verbose_name='زمان دریافت آخرین ایمیل بازیابی کلمه عبور')

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        else:
            return self.email

    def save(self, *args, **kwargs):
        x=self.email.index('@')
        self.username = self.email[0:x]
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     # تنها درصورتی که شیِ ساخته شده جدید است(ویرایش شیِ قبلی نیست(تنها درصورتی آیدی ندارد که شی جدید باشد)) براش یوزرنیم برابر با آیدی اخرین کاربر+1 درنظر بگیر
    #     if not self.pk:
    #         self.username = User.objects.last().id + 1
    #     super().save(*args,**kwargs)


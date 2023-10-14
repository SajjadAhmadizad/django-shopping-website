from django.db import models

# Create your models here.


class ContactUsModel(models.Model):
    name = models.CharField(max_length=50,verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    message = models.TextField(verbose_name='متن تماس باما')
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد')
    read_by_admin = models.BooleanField(default=False,verbose_name='خوانده شده توسط ادمین')
    answer = models.TextField(verbose_name='پاسخ')

    class Meta:
        verbose_name = 'فرم تماس باما'
        verbose_name_plural = 'فرم های تماس باما'

    def __str__(self):
        return f'{self.name} {self.email}'
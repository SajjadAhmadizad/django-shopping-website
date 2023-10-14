from django.contrib import admin

from site_module.models import SiteModel
from . import models
from utils.email_service import send_email
from contact_module.models import ContactUsModel


# Register your models here.

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message', 'answer']
    list_filter = ['name', 'email', 'message', 'answer']

    def save_model(self, request, obj: models.ContactUsModel, form, change):
        site = SiteModel.objects.filter(is_active=True).first()
        if change and obj.read_by_admin == 1 and not obj.answer:
            send_email('تماس با ما', obj.email, {'address': site.address, 'phone': site.phone},
                       'emails/contact-us.html')
        elif change and obj.read_by_admin == 1 and obj.answer:
            send_email('تماس با ما', obj.email, {'answer': obj.answer, 'address': site.address, 'phone': site.phone},
                       'emails/contact-us-answer.html')

        return super().save_model(request, obj, form, change)


admin.site.register(models.ContactUsModel, ContactUsAdmin)

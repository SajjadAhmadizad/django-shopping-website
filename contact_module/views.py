from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.template.loader import render_to_string

from contact_module.forms import ContactUsModelForm
from site_module.models import SiteModel
from utils.email_service import send_email


# Create your views here.


def ContactUsView(request):
    if request.method == 'GET':
        contact_us_form = ContactUsModelForm()
        site = SiteModel.objects.filter(is_active=True).first()
        if site is not None:
            return render(request, 'contact_module/contact-us-page.html',
                          {'form': contact_us_form, 'csrf_token': get_token(request), 'address': site.address,'phone': site.phone})
        else:
            return render(request, 'contact_module/contact-us-page.html',
                          {'form': contact_us_form, 'csrf_token': get_token(request), 'address': 'مازندران بابل','phone': '09931355952'})

    if request.method == 'POST':
        contact_us_form = ContactUsModelForm(request.POST)
        if contact_us_form.is_valid():
            contact_us_form.save()
            site = SiteModel.objects.filter(is_active=True).first()
            if site is not None:
                send_email('تماس با ما', contact_us_form.cleaned_data.get('email'),{'address': site.address, 'phone': site.phone}, 'emails/contact-us-success.html')
            else:
                send_email('تماس با ما', contact_us_form.cleaned_data.get('email'),{'address': 'مازندران بابل', 'phone': '09931355952'}, 'emails/contact-us-success.html')
            
            return JsonResponse({
                'status': 'success',
                'message': 'فرم تماس باما با موفقیت ثبت شد'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'body': render_to_string('contact_module/components/contact-us-form-component.html',
                                         {'form': contact_us_form, 'csrf_token': get_token(request)})
            })

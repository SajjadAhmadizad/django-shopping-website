import datetime

from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse, Http404
from django.middleware.csrf import get_token
from django.urls import reverse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.middleware import csrf
from django.utils.html import strip_tags

from djangoProject1 import settings
from site_module.models import SiteModel
from utils.email_service import send_email
from .forms import RegisterForm, LoginForm, ResetPasswordForm, ChangePasswordForm
from .models import User


# Create your views here.
def RegisterView(request):
    if request.method == 'GET':
        return render(request, 'account_module/register_view.html',
                      {'register_form': RegisterForm(), 'login_form': LoginForm(),
                       'csrf_token': csrf.get_token(request), 'csrf_token2': csrf.get_token(request)})
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        status = 'failed'
        if register_form.is_valid():
            password = register_form.cleaned_data.get('password')
            email = register_form.cleaned_data.get('email')
            new_user = User(email=email, email_active_code=get_random_string(80), is_active=False)
            new_user.set_password(password)
            new_user.save()

            send_email(subject='فعالسازی حساب کاربری', to=email,
                       context={'domainname': SiteModel.objects.filter(is_active=True).first().domain_name,
                                'address': SiteModel.objects.filter(is_active=True).first().address,
                                'emailactivecode': new_user.email_active_code,
                                'phone': SiteModel.objects.filter(is_active=True).first().phone},
                       template_name='emails/active-email.html')
            status = 'success'
        data = render_to_string('account_module/components/sign_up_component.html',
                                {'register_form': register_form, 'login_form': LoginForm(),
                                 'csrf_token': csrf.get_token(request), 'csrf_token2': csrf.get_token(request)})
        return JsonResponse({
            'body': data,
            'status': status,
            'message': 'ایمیل فعالسازی حساب با موفقیت ارسال شد'
        })


def LoginFormSubmit(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        status = 'failed'
        redirectTo = ''
        if login_form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            if email is not None:
                user = User.objects.filter(email=email).first()
                if user is not None:
                    if user.check_password(password):
                        if user.is_active:
                            login(request, user)
                            user.email_active_code = get_random_string(80)
                            user.save()
                            status = 'success'
                            redirectTo = request.POST.get('next')
                            if redirectTo == '':
                                redirectTo = reverse('home_page')
                        else:
                            login_form.add_error('email', 'حساب کاربری مورد نظر فعال نمیباشد!')
                    else:
                        login_form.add_error('password', 'رمز عبور وارد شده صحیح نمیباشد!')
                else:
                    login_form.add_error('email', 'کاربری با این ایمیل یافت نشد!')

        data = render_to_string('account_module/components/sign_in_component.html',
                                {'register_form': RegisterForm(), 'login_form': login_form,
                                 'csrf_token': csrf.get_token(request), 'csrf_token2': csrf.get_token(request)})
        return JsonResponse({
            'body': data,
            'status': status,
            'redirectTo': redirectTo
        })


def ActiveAccount(request, email_active_code):
    user = User.objects.filter(email_active_code__iexact=email_active_code, is_active=False).first()
    if user is None:
        raise Http404()
    else:
        user.is_active = True
        user.email_active_code = get_random_string(80)
        user.save()
        return redirect('register_page')


def LogOutView(request):
    logout(request)
    return redirect('register_page')


def ForgotPasswordView(request):
    if request.method == 'GET':
        reset_pass_form = ResetPasswordForm()
        return render(request, 'account_module/forgot_password_view.html',
                      {'form': reset_pass_form})
    if request.method == 'POST':
        reset_pass_form = ResetPasswordForm(request.POST)
        status = 'error'
        if reset_pass_form.is_valid():
            user = User.objects.filter(email__iexact=request.POST.get('email')).first()
            elapsed_time = None
            if user.last_reset_password_date is not None:
                elapsed_time = timezone.now() - user.last_reset_password_date
            if elapsed_time is None or elapsed_time.total_seconds() >= 300:
                send_email(subject='بازیابی کلمه عبور', to=user.email,
                           context={'domainname': SiteModel.objects.filter(is_active=True).first().domain_name,
                                    'address': SiteModel.objects.filter(is_active=True).first().address,
                                    'emailactivecode': user.email_active_code,
                                    'phone': SiteModel.objects.filter(is_active=True).first().phone},
                           template_name='emails/reset-password.html')
                status = 'success'
                user.last_reset_password_date = timezone.now()
                user.save()
            else:
                status = 'time_error'

        return JsonResponse({
            'status': status,
            'body': render_to_string('account_module/components/forgot_password_email_component.html',
                                     {'csrf': get_token(request),
                                      'form': reset_pass_form}),
            'message': 'ایمیل بازیابی کلمه عبور با موفقیت ارسال شد'
        })


def ResetPasswordView(request, email_active_code):
    user: User = User.objects.filter(email_active_code=email_active_code).first()
    if request.method == 'GET':
        if user is not None:
            form = ChangePasswordForm()
            return render(request, 'account_module/reset_password_view.html',
                          {'form': form, 'email_active_code': user.email_active_code})
        else:
            raise Http404()
    if request.method == 'POST':
        status = 'error'
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user.set_password(request.POST.get('password'))
            user.email_active_code = get_random_string(80)
            user.save()
            status = 'success'

        return JsonResponse({
            'status': status,
            'body': render_to_string('account_module/components/reset-password-form-component.html',
                                     {'form': form, 'email_active_code': user.email_active_code,
                                      'csrf': get_token(request)}),
            'message': 'تغییر کلمه عبور با موفقیت انجام شد.'
        })


def ForgotPasswordLoggedInUserView(request):
    if request.user.is_authenticated:
        user = User.objects.filter(id=request.user.id).first()
        elapsed_time = None
        if user.last_reset_password_date is not None:
            elapsed_time = timezone.now() - user.last_reset_password_date
        if elapsed_time is None or elapsed_time.total_seconds() >= 300:
            send_email(subject='بازیابی کلمه عبور', to=user.email,
                       context={'domainname': SiteModel.objects.filter(is_active=True).first().domain_name,
                                'address': SiteModel.objects.filter(is_active=True).first().address,
                                'emailactivecode': user.email_active_code,
                                'phone': SiteModel.objects.filter(is_active=True).first().phone},
                       template_name='emails/reset-password.html')
            status = 'success'
            user.last_reset_password_date = timezone.now()
            user.save()
            status = 'success'
        else:
            status = 'time_error'
        return JsonResponse({
            'status': status
        })
    else:
        raise Http404()

from django import forms
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from account_module.models import User


class RegisterForm(forms.Form):
    #
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(RegisterForm, self).__init__(*args, **kwargs)

    email = forms.CharField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ایمیل',

        }),
        required=True,
        error_messages={
            'required': 'ایمیل حتما باید وارد شود!'
        }
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': "رمز عبور"
        }),
        required=True,
        error_messages={
            'required': 'رمز عبور حتما باید وارد شود!'
        }
    )
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'تکرار رمز عبور'
        }),
        required=True,
        error_messages={
            'required': 'تکرار رمز عبور حتما باید وارد شود!'
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is not None:
            if email[-10::] == '@gmail.com':
                user: User = User.objects.filter(email__iexact=email).first()
                if user is None:
                    return email
                else:
                    raise ValidationError('ایمیل وارد شده تکراری میباشد!')
            else:
                raise ValidationError('امکان ثبت نام با دامنه هایی به غیر از gmail.com@ وجود ندارد!')
        else:
            raise ValidationError('این فیلد نمیتواند خالی باشد!')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password == confirm_password:
            return cleaned_data
        else:
            self.add_error('password', 'رمز عبور و تکرار رمز عبور باهم مطابقت ندارند!')

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password is not None:
            if str(password).isdigit() == False:
                if len(password) >= 6:
                    return password
                else:
                    raise ValidationError('طول رمز عبور باید بیشتر از 6 کلمه باشد!')
            else:
                raise ValidationError('رمز عبور نمیتواند فقط شامل اعداد باشد!')


# def clean(self):
#     cleaned_data = super().clean()
#     email = cleaned_data.get('email')
#     password = cleaned_data.get('password')
#     confirm_password = cleaned_data.get('confirm_password')
#     if User.objects.filter(email__iexact=email).first() is None:
#         if email is not None:
#             if email[-10::].lower() == '@gmail.com':
#                 if password is not None:
#                     if len(password) >= 6:
#                         if str(password).isdigit() == False:
#                             if password == confirm_password:
#                                 password = self.cleaned_data.get('password')
#                                 new_user = User(email=email, email_active_code=get_random_string(80),
#                                                 is_active=False)
#                                 new_user.set_password(password)
#                                 new_user.save()
#                             else:
#                                 self.add_error('password', 'رمز عبور و تکرار رمز عبور باهم مطابقت ندارند!')
#                         else:
#                             self.add_error('password', 'رمز عبور نمیتواند فقط شامل اعداد باشد!')
#                     else:
#                         self.add_error('password', 'طول رمز عبور باید بیشتر از 6 کلمه باشد!')
#                 else:
#                     pass
#             else:
#                 self.add_error('email', 'امکان ثبت نام با دامنه هایی به غیر از gmail.com@ ممکن نیست!')
#         else:
#             pass
#     else:
#         self.add_error('email', 'ایمیل وارد شده تکراری میباشد!')


class LoginForm(forms.Form):
    email = forms.CharField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ایمیل',
        }),
        required=True,
        error_messages={
            'required': 'ایمیل حتما باید وارد شود!'
        }

    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': "رمز عبور"
        }),
        required=True,
        error_messages={
            'required': 'رمز عبور حتما باید وارد شود!'
        }
    )


class ResetPasswordForm(forms.Form):
    email = forms.CharField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'id': 'user_email',
            'name': 'user_email',
            'placeholder': 'ایمیل'
        }),
        required=True,
        error_messages={
            'required': 'ایمیل حتما باید وارد شود!'
        }

    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email[-10::].lower() != '@gmail.com' or User.objects.filter(email__iexact=email).first() is None:
            raise ValidationError('حساب کاربری ای با این ایمیل یافت نشد!')
        return email


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': "رمز عبور"
        }),
        required=True,
        error_messages={
            'required': 'رمز عبور حتما باید وارد شود!'
        }
    )
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'تکرار رمز عبور'
        }),
        required=True,
        error_messages={
            'required': 'تکرار رمز عبور حتما باید وارد شود!'
        }
    )

    def clean(self):
        cleaned_data = super().clean();
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password == confirm_password:
            return cleaned_data
        else:
            self.add_error('password', 'رمز عبور و تکرار رمز عبور باهم مطابقت ندارند!')

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password is not None:
            if str(password).isdigit() == False:
                if len(password) >= 6:
                    return password
                else:
                    raise ValidationError('طول رمز عبور باید بیشتر از 6 کلمه باشد!')
            else:
                raise ValidationError('رمز عبور نمیتواند فقط شامل اعداد باشد!')

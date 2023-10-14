from django import forms
from django.core.exceptions import ValidationError

from account_module.models import User


class UserProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'about_user', 'address', 'avatar']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'dir': 'rtl',
                'name': 'first_name',
                'id': 'first_name',
                'placeholder': 'نام'
            }
            ),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'dir': 'rtl',
                'name': 'first_name',
                'id': 'first_name',
                'placeholder': 'نام خانوادگی'
            }
            ),
            'username': forms.TextInput(attrs={
                'class':'form-control',
                'dir':'rtl',
                'name': 'username',
                'id': 'username',
                'placeholder': 'یوزرنیم'
            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'dir': 'rtl',
                'name': 'aboutuser',
                'id': 'aboutuser',
                'placeholder': 'درباره کاربر'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'dir': 'rtl',
                'name': 'address',
                'id': 'address',
                'placeholder': 'آدرس'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'dir': 'rtl',
                'name': 'avatar'
            })
        }
        error_messages = {
            'username':{
                'unique':'این یوزرنیم توسط شخص دیگری انتخاب شده است'
            }
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) > 20:
            raise  ValidationError('نام نمیتواند بیشتر از 20 حرف باشد!')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) > 20:
            raise  ValidationError('نام خانوادگی نمیتواند بیشتر از 20 حرف باشد!')
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        allowed = '0123456789abcdefghijklmnopqrstuvwxyz_'
        if len(username) > 20:
            raise  ValidationError('یوزرنیم نمیتواند بیشتر از 20 حرف باشد!')

        for char in username:
            if char not in allowed:
                raise ValidationError('موارد مجاز : a-z و 0-9 و _')

        return username


    def clean_about_user(self):
        about_user = self.cleaned_data.get('about_user')
        if len(about_user) > 200:
            raise ValidationError('بیوگرافی نمیتواند بیشتر از 200 حرف باشد!')
        return about_user



class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'placeholder': "رمز عبور",
            'class':'form-control',
            'dir':'rtl'
        }),
        required=True,
        error_messages={
            'required': 'رمز عبور حتما باید وارد شود!',
            'class':'form-control'
        }
    )
    new_password = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور جدید',
            'class':'form-control',
            'dir':'rtl'
        }),
        required=True,
        error_messages={
            'required': 'رمز عبور حتما باید وارد شود!'
        }
    )

    confirm_new_password = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'تکرار رمز عبور جدید',
            'class':'form-control',
            'dir':'rtl'
        }),
        required=True,
        error_messages={
            'required': ' تکرار رمز عبور حتما باید وارد شود!'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        if new_password != confirm_new_password:
            self.add_error('new_password','کلمه عبور جدید با تکرار آن مطابقت ندارد!')
        if str(new_password).isdigit() == True:
            self.add_error('new_password','رمز عبور نمیتواند فقط شامل اعداد باشد!')
        if len(str(new_password)) < 6:
            self.add_error('new_password','طول رمز عبور باید بیشتر از 6 کلمه باشد!')
        return new_password
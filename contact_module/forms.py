from django import forms

from contact_module.models import ContactUsModel


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUsModel
        fields = ['name','email','message']


        widgets={
            'name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'نام'
            }),
            'email':forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }),
            'message':forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'متن پیام',
                'rows':6
            })
        }

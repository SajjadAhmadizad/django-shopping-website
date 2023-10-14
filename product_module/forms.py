from django import forms

from product_module.models import ProductCommentModel


class ProductCommentModelForm(forms.ModelForm):
    class Meta:
        model = ProductCommentModel
        fields = ['comment']

        widgets = {
            'comment':forms.Textarea(attrs={
                'class':'form-control',
                'rows':'6',
                'id':'comment',
                'name':'comment'
            })
        }
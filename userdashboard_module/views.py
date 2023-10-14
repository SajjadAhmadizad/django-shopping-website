from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from account_module.models import User
from order_module.models import Order
from userdashboard_module.forms import UserProfileModelForm, ChangePasswordForm


# Create your views here.
@login_required
def UserDashboardView(request):
    if request.method == 'GET':
        form = UserProfileModelForm(instance=request.user)
        change_password_form = ChangePasswordForm()
        return render(request, 'userdashboard_module/userdashboared.html', {'form1': form,'change_password_form':change_password_form,'active_item':'information-form'})
    if request.method == 'POST':
        current_user:User = User.objects.filter(id=request.user.id).first()
        active_item = 'information-form'
        if request.POST.get('form') == 'password-form':
            change_password_form = ChangePasswordForm(request.POST)
            current_password = request.POST.get('current_password')
            is_password_correct = current_user.check_password(current_password)
            if is_password_correct is True:
                if change_password_form.is_valid():
                    new_password = request.POST.get('new_password')
                    current_user.set_password(new_password)
                    current_user.save()
            else:
                change_password_form.add_error('current_password', 'رمز عبور فعلی نادرست است')
            form = UserProfileModelForm(instance=request.user)
            active_item = 'password-form'
        elif request.POST.get('form') == 'user-information-form':
            form = UserProfileModelForm(request.POST,request.FILES,instance=current_user)
            if form.is_valid():
                if User.objects.filter(username=form.cleaned_data.get('username')).exclude(id=current_user.id).first() is None:
                    form.save(commit=True)
            change_password_form = ChangePasswordForm()
    return render(request, 'userdashboard_module/userdashboared.html', {'form1': form,'user':current_user,'change_password_form':change_password_form,'active_item':active_item})


@login_required
def PurchasedProducts(request):
    current_user:User = User.objects.filter(id=request.user.id).first()
    orders:Order = Order.objects.prefetch_related('orderitems_set').filter(is_paid=True,user_id=current_user.id).all()
    return render(request,'userdashboard_module/purchasedproducts.html',{'orders':orders})

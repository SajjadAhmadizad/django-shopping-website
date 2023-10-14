from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.RegisterView,name='register_page'),
    path('log-out/',views.LogOutView,name='log_out_page'),
    path('login-form-submit/',views.LoginFormSubmit,name='login_form_submit_ajax'),
    path('active-account/<str:email_active_code>',views.ActiveAccount,name='activate_account_view'),
    path('forgot-password/',views.ForgotPasswordView,name='forgot_password_view'),
    path('forgot-password-logged-in-user/',views.ForgotPasswordLoggedInUserView,name='forgot_password_logged_in_user_view'),
    path('reset-password/<str:email_active_code>',views.ResetPasswordView,name='reset_password_view'),
]
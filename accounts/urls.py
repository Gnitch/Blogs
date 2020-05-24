from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name='accounts'
urlpatterns = [
    path('',views.welcome,name='welcome'),
    path('login/',views.userLogin,name='user_login'),
    path('signup/',views.userSignUp,name='user_signup'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='accounts/pass_reset.html'),name='pass_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/pass_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/pass_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/pass_reset_complete.html'),name='password_reset_complete'),


]



# '
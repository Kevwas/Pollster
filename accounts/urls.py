from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.registerView, name='register'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutUser, name='logout'), 

    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), 
        name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="reset_password_sent"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path('reset_password_done/', 
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset_done.html"), 
        name="reset_password_done"),
]
from django.urls import path, reverse_lazy

from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.registerView, name='register'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutUser, name='logout'), 
    path('<str:username>/', views.ProfileView, name='profile'), 

    path('accounts/password_reset/', 
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            success_url=reverse_lazy('accounts:password_reset_done'),
        ), name="password_reset"),

    path('accounts/password_reset_done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_sent.html",
        ), name="password_reset_done"),

    path('accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy('accounts:password_reset_complete')
        ),  name="password_reset_confirm"),

    path('accounts/password_reset_complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_done.html"
        ), name="password_reset_complete"),
]
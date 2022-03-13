from django.urls import path
from .views import *
from django.urls import reverse_lazy
from django.contrib.auth.views import (LoginView, LogoutView, PasswordResetDoneView, PasswordResetView,
                                       PasswordResetCompleteView, PasswordResetConfirmView,
                                       PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetDoneView)

app_name = 'authapp'

urlpatterns = [
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='authapp/logged_out.html'), name='logout'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='authapp/password_change_form.html'), name='password_change'),
    path('password_change/dond/', PasswordChangeDoneView.as_view(template_name='authapp/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='authapp/password_reset_form.html',
        email_template_name='authapp/password_reset_email.html',
        success_url=reverse_lazy('authapp:password_reset_done')), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='authapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='authapp/password_reset_confirm.html',
        success_url=reverse_lazy('authapp:login')), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='authapp/password_reset_complete.html'), name='password_reset_complete'),
    path('all_users/', show_all_users, name='all_users'),
    path('all_users/<int:from_user_id>-<int:user_id>/', send_friend_request, name='friend_request_sent'),
    path('all_users/frs/', show_friend_requests, name='friend_requests'),
    path('all_users/frs/accept<int:sender_id>/', accept_friend_request, name='friend_requests'),
    path('all_users/qr/', QrFriendsList.as_view(), name="qr_friends_list"),
    path('all_users/download/', DownloadFriendsList.as_view(), name="download_friends_list"),
    path('forms/register/', Register_User.as_view(), name='register_user_from_form'),
    path('forms/', TemplateView.as_view(template_name='forms/form.html'), name='render_register_template'),
]

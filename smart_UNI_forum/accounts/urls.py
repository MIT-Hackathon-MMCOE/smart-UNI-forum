from django.conf.urls import url, include
from .views import *
from django.contrib.auth import views as auth

urlpatterns = [
	# url('', IndexPageView.as_view(), name='index'),

    url('i18n/', include('django.conf.urls.i18n')),

    url('accounts/login/', SignInView.as_view(), name='login'),
    url('accounts/logout/', auth.logout, {'next_page': '/accounts/login'}),
    url('accounts/activate/resend/', ReSendActivationCodeView.as_view(), name='resend_activation_code'),

    url('accounts/register/', SignUpView.as_view(), name='register'),
    url('accounts/activate/<code>/', ActivateView.as_view(), name='activate'),

    url('accounts/password/change/', auth.PasswordChangeView.as_view(
        template_name='password_change_form.html'), name='password_change'),
    url('accounts/password/change/done/', auth.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'), name='password_change_done'),

    url('accounts/password/reset/',
         PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    url('accounts/password/reset/done/', auth.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),

    url('accounts/reset/<uidb64>/<token>/',
         auth.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    url('accounts/reset/done/',
         auth.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

    url('accounts/change/email/', ChangeEmailView.as_view(), name='change_email'),
    url('accounts/change/email/<code>/', ChangeEmailActivateView.as_view(),
         name='change_email_activation'),
    url(r'^accounts/profile/edit/(?P<slug>[^\.]+)/$', ProfileUpdate.as_view(success_url="/accounts/profile/"), name='profile_edit'),

    url('accounts/profile', profile_display, name='profile_display'),
]


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME, get_user_model
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView as BasePasswordResetView, SuccessURLAllowedHostsMixin
from django.shortcuts import get_object_or_404, resolve_url
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from django.views.generic.edit import FormView
from django.conf import settings
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required


from .utils import (
    get_login_form, send_activation_email, get_password_reset_form, send_reset_password_email,
    send_activation_change_email, is_username_disabled, get_resend_ac_form
)

from .choices import *
from .forms import SignUpForm, ProfileEditForm, ChangeEmailForm
from .models import *

UserModel = get_user_model()

# Create your views here.

class IndexPageView(TemplateView):
    template_name = 'index.html'

def LogoutView(request):
    """docstring for LogoutView"""
    logout(request)
    return redirect('/accounts/login')

class SuccessRedirectView(SuccessURLAllowedHostsMixin, FormView):
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_form_kwargs(self):
        kwargs = super(SuccessRedirectView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class SignInView(SuccessRedirectView):
    template_name = 'login.html'
    form_class = get_login_form()
    success_url = '/'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(SignInView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        login(self.request, form.get_user())

        return super(SignInView, self).form_valid(form)


class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save(commit=False)

        if is_username_disabled():
            # Set temporary username
            user.username = get_random_string()
        else:
            user.username = form.cleaned_data.get('username')

        if settings.ENABLE_USER_ACTIVATION:
            user.is_active = False

        user.save()

        # Change the username to "user_ID" form
        if is_username_disabled():
            user.username = 'user_{}'.format(user.id)
            user.save()

        if settings.ENABLE_USER_ACTIVATION:
            send_activation_email(self.request, user)

            messages.add_message(self.request, messages.SUCCESS,
                                 _('You are registered. To activate the account, follow the link sent to the mail.'))
        else:
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=user.username, password=raw_password)
            login(self.request, user)

            messages.add_message(self.request, messages.SUCCESS, _('You are successfully registered!'))

        return super(SignUpView, self).form_valid(form)


class ActivateView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):
        assert 'code' in kwargs

        act = get_object_or_404(Activation, code=kwargs['code'])

        # Activate user's profile
        user = act.user
        user.is_active = True
        user.save()

        # Remove activation record, it is unneeded
        act.delete()

        messages.add_message(self.request, messages.SUCCESS, _('You have successfully activated your account!'))
        login(self.request, user)

        return super(ActivateView, self).get_redirect_url()


class ReSendActivationCodeView(SuccessRedirectView):
    template_name = 'resend_activation_code.html'
    form_class = get_resend_ac_form()
    success_url = '/'

    def form_valid(self, form):
        user = form.get_user()

        activation = user.activation_set.get()
        activation.delete()

        send_activation_email(self.request, user)

        messages.add_message(self.request, messages.SUCCESS, _('A new activation code has been sent to your e-mail.'))

        return super(ReSendActivationCodeView, self).form_valid(form)


class PasswordResetView(BasePasswordResetView):
    form_class = get_password_reset_form()

    def form_valid(self, form):
        send_reset_password_email(self.request, form.get_user())

        return super(PasswordResetView, self).form_valid(form)


class ProfileEditView(LoginRequiredMixin, FormView):
    template_name = 'profile/edit.html'

    form_class = ProfileEditForm
    success_url = '/profile/edit/'

    def get_initial(self):
        initial = super(ProfileEditView, self).get_initial()

        user = self.request.user

        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name

        return initial

    def form_valid(self, form):
        user = self.request.user

        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()

        messages.add_message(self.request, messages.SUCCESS, _('Profile data has been successfully updated.'))

        return super(ProfileEditView, self).form_valid(form)


class ChangeEmailView(LoginRequiredMixin, FormView):
    template_name = 'profile/change_email.html'

    form_class = ChangeEmailForm
    success_url = '/change/email/'

    def get_form_kwargs(self):
        kwargs = super(ChangeEmailView, self).get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def get_initial(self):
        initial = super(ChangeEmailView, self).get_initial()

        user = self.request.user

        initial['email'] = user.email

        return initial

    def form_valid(self, form):
        user = self.request.user

        email = form.cleaned_data.get('email')
        email = email.lower()

        if hasattr(settings, 'EMAIL_ACTIVATION_AFTER_CHANGING') and settings.EMAIL_ACTIVATION_AFTER_CHANGING:
            send_activation_change_email(self.request, user, email)

            messages.add_message(self.request, messages.SUCCESS,
                                 _('To complete the change of mail, click on the link sent to it.'))
        else:
            user.email = email
            user.save()

            messages.add_message(self.request, messages.SUCCESS, _('Email successfully changed.'))

        return super(ChangeEmailView, self).form_valid(form)


class ChangeEmailActivateView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'change_email'

    def get_redirect_url(self, *args, **kwargs):
        assert 'code' in kwargs

        act = get_object_or_404(Activation, code=kwargs['code'])

        # Change user's email
        user = act.user
        user.email = act.email
        user.save()

        # Remove activation record, it is unneeded
        act.delete()

        messages.add_message(self.request, messages.SUCCESS, _('You have successfully changed your email!'))

        return super(ChangeEmailActivateView, self).get_redirect_url()

@login_required(login_url="accounts/login/")
def profile_edit(request):
    if request.method == 'POST':
        user                        = UserModel.objects.get(pk = request.POST.get("profile", ""))
        profile                     = Profile.objects.get(user = user)
        form = ProfileForm(request.POST, request.FILES, instance = profile)
        if form.is_valid():
            form.save()
            return redirect('accounts/profile/')
        else:
            print( form.errors )
            form = ProfileForm
            context = {'form': form}
            return render(request, 'profile_edit.html', context)

    else:
        form = ProfileForm
        context = {'form': form}
        return render(request, 'profile_edit.html', context)
    


@login_required(login_url="accounts/login/")
def profile_display(request):
    profile = Profile.objects.filter(user = request.user)
    if not profile:
        profile = Profile(
                        user          = request.user,
                        first_name    = request.user.first_name,
                        last_name     = request.user.last_name,
                        level         = 0,
                        points        = 0
                     )
        profile.save()
        followers       = Follower.objects.filter(user = request.user).count()
        following       = Follower.objects.filter(following = request.user).count()
        projects        = Project.objects.filter(user = request.user)
        profile         = profile[0]
        context     = {'profile': profile, 'followers': followers, 'following' : following, 'projects': projects}
        return render(request, 'profile_display.html', context)
    else:
        followers       = Follower.objects.filter(user = request.user).count()
        following       = Follower.objects.filter(following = request.user).count()
        projects        = Project.objects.filter(user = request.user)
        profile         = profile[0]
        colleges        = dict(Colleges)
        branch          = dict(Branch)
        profile.college = colleges[profile.college]
        profile.branch  = branch[profile.branch]
        context     = {'profile': profile, 'followers': followers, 'following' : following, 'projects': projects}
        return render(request, 'profile_display.html', context)
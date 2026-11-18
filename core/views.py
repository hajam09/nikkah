from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from core.forms import (
    LoginForm,
    MatrimonialProfileForm,
    PasswordChangeForm,
    PersonalProfileForm,
    ReligiousProfileForm,
)
from core.models import MatrimonialProfile, ReligiousProfile


class UserLoginView(LoginView):
    template_name = 'core/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


def indexView(request):
    return render(request, 'core/home.html')


@login_required
def dashboardView(request):
    return render(request, 'core/dashboard.html')


@login_required
def personalSettingsView(request):
    form = PersonalProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your personal profile has been updated.')
        return redirect('core:settings-personal')

    return render(request, 'core/settings/personal_profile.html', {
        'form': form,
        'active_setting': 'personal',
    })


class UserPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'core/settings/password.html'
    success_url = reverse_lazy('core:settings-password')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed.')
        return super().form_valid(form)


@login_required
def matrimonialProfileSettingsView(request):
    profile = MatrimonialProfile.objects.filter(user=request.user).first()
    form = MatrimonialProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(request, 'Your matrimonial profile has been updated.')
        return redirect('core:settings-matrimonial')

    return render(request, 'core/settings/matrimonial_profile.html', {
        'form': form,
        'active_setting': 'matrimonial',
    })


@login_required
def religiousProfileSettingsView(request):
    profile = ReligiousProfile.objects.filter(user=request.user).first()
    form = ReligiousProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(request, 'Your religious profile has been updated.')
        return redirect('core:settings-religious')

    return render(request, 'core/settings/religious_profile.html', {
        'form': form,
        'active_setting': 'religious',
        'is_creating_profile': profile is None,
    })

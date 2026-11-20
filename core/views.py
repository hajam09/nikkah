from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from core.forms import (
    CareerProfileForm,
    EducationForm,
    FamilyProfileForm,
    LoginForm,
    MatrimonialProfileForm,
    PasswordChangeForm,
    PersonalProfileForm,
    ProfileLocationForm,
    ReligiousProfileForm,
    WaliForm,
)
from core.models import (
    CareerProfile,
    Education,
    FamilyProfile,
    MatrimonialProfile,
    ProfileLocation,
    ReligiousProfile,
    Wali,
)


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
def familyProfileSettingsView(request):
    profile = FamilyProfile.objects.filter(user=request.user).first()
    form = FamilyProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(request, 'Your family profile has been updated.')
        return redirect('core:settings-family')

    return render(request, 'core/settings/family_profile.html', {
        'form': form,
        'active_setting': 'family',
        'is_creating_profile': profile is None,
    })


@login_required
def waliSettingsView(request):
    wali = Wali.objects.filter(user=request.user).first()
    form = WaliForm(request.POST or None, instance=wali)
    if request.method == 'POST' and form.is_valid():
        wali = form.save(commit=False)
        wali.user = request.user
        wali.save()
        messages.success(request, 'Your wali details have been updated.')
        return redirect('core:settings-wali')

    return render(request, 'core/settings/wali.html', {
        'form': form,
        'active_setting': 'wali',
        'is_creating_profile': wali is None,
    })


@login_required
def religiousProfileSettingsView(request):
    profile = ReligiousProfile.objects.select_related('user__matrimonialProfile').filter(user=request.user).first()
    gender = profile.user.matrimonialProfile.gender if profile and profile.user.matrimonialProfile else None
    form = ReligiousProfileForm(request.POST or None, instance=profile, gender=gender)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        if gender == MatrimonialProfile.Gender.MALE:
            profile.wearsHijab = None
            profile.wearsNiqab = None
        profile.save()
        messages.success(request, 'Your religious profile has been updated.')
        return redirect('core:settings-religious')

    return render(request, 'core/settings/religious_profile.html', {
        'form': form,
        'active_setting': 'religious',
        'is_creating_profile': profile is None,
    })


@login_required
def educationSettingsView(request):
    profile = Education.objects.filter(user=request.user).first()
    form = EducationForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(request, 'Your education profile has been updated.')
        return redirect('core:settings-education')

    return render(request, 'core/settings/education.html', {
        'form': form,
        'active_setting': 'education',
        'is_creating_profile': profile is None,
    })


@login_required
def careerProfileSettingsView(request):
    profile = CareerProfile.objects.filter(user=request.user).first()
    form = CareerProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(request, 'Your career profile has been updated.')
        return redirect('core:settings-career')

    return render(request, 'core/settings/career_profile.html', {
        'form': form,
        'active_setting': 'career',
        'is_creating_profile': profile is None,
    })


@login_required
def profileLocationSettingsView(request):
    profile = ProfileLocation.objects.filter(user=request.user).first()
    form = ProfileLocationForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(request, 'Your location profile has been updated.')
        return redirect('core:settings-location')

    return render(request, 'core/settings/location.html', {
        'form': form,
        'active_setting': 'location',
        'is_creating_profile': profile is None,
    })

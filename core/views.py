from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db import transaction
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from core.forms import (
    CareerProfileForm,
    EducationForm,
    FamilyProfileForm,
    LoginForm,
    MatrimonialProfileForm,
    PasswordChangeForm,
    PartnerPreferenceForm,
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
    PartnerPreference,
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
        'is_creating_profile': profile is None,
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
    gender = profile.user.matrimonialProfile.gender if profile and hasattr(profile.user, 'matrimonialProfile') else None
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


def _render_partner_preference_settings(
    request,
    create_form=None,
    bound_forms=None,
    editing_preference_id=None,
):
    preferences = PartnerPreference.objects.filter(user=request.user).order_by(
        '-isDefault', 'id'
    )
    first_preference = preferences.order_by('id').first()
    if first_preference and not preferences.filter(isDefault=True).exists():
        first_preference.isDefault = True
        first_preference.save(update_fields=['isDefault'])
        preferences = PartnerPreference.objects.filter(user=request.user).order_by(
            '-isDefault', 'id'
        )
    preference_count = preferences.count()
    bound_forms = bound_forms or {}
    preference_forms = [
        {
            'number': index,
            'preference': preference,
            'form': bound_forms.get(preference.pk) or PartnerPreferenceForm(
                instance=preference,
                prefix=f'preference-{preference.pk}',
            ),
            'is_open': preference.pk == editing_preference_id,
        }
        for index, preference in enumerate(preferences, start=1)
    ]

    return render(request, 'core/settings/partner_preferences.html', {
        'active_setting': 'preferences',
        'preference_forms': preference_forms,
        'preference_count': preference_count,
        'create_form': create_form or PartnerPreferenceForm(
            prefix='create',
        ),
    })


@login_required
def partnerPreferenceSettingsView(request):
    return _render_partner_preference_settings(request)


@login_required
def createPartnerPreferenceView(request):
    if request.method != 'POST':
        return redirect('core:settings-preferences')

    form = PartnerPreferenceForm(
        request.POST,
        prefix='create',
    )
    if form.is_valid():
        with transaction.atomic():
            preference = form.save(commit=False)
            preference.user = request.user
            preference.save()
        messages.success(request, 'Partner preference created.')
        return redirect('core:settings-preferences')

    return _render_partner_preference_settings(request, create_form=form)


@login_required
def updatePartnerPreferenceView(request, pk):
    if request.method != 'POST':
        return redirect('core:settings-preferences')

    preference = get_object_or_404(PartnerPreference, pk=pk, user=request.user)
    form = PartnerPreferenceForm(
        request.POST,
        instance=preference,
        prefix=f'preference-{preference.pk}',
    )
    if form.is_valid():
        with transaction.atomic():
            preference = form.save(commit=False)
            preference.save()
        messages.success(request, 'Partner preference updated.')
        return redirect('core:settings-preferences')

    return _render_partner_preference_settings(
        request,
        bound_forms={preference.pk: form},
        editing_preference_id=preference.pk,
    )


@login_required
def deletePartnerPreferenceView(request, pk):
    if request.method != 'POST':
        return redirect('core:settings-preferences')

    preference = get_object_or_404(PartnerPreference, pk=pk, user=request.user)
    preference.delete()
    messages.success(request, 'Partner preference deleted.')
    return redirect('core:settings-preferences')


@login_required
def clonePartnerPreferenceView(request, pk):
    if request.method != 'POST':
        return redirect('core:settings-preferences')

    preference = get_object_or_404(PartnerPreference, pk=pk, user=request.user)
    copiedFields = model_to_dict(preference, exclude=('id', 'user', 'name', 'isDefault'))
    PartnerPreference.objects.create(
        user=request.user,
        name=f'Copy of {preference.name}'[:100],
        isDefault=False,
        **copiedFields,
    )
    messages.success(request, 'Partner preference cloned.')
    return redirect('core:settings-preferences')

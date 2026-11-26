from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone

from core import service
from core.choices import Gender
from core.constants import (
    USER_PROFILE_RELATIONS,
    PROFILE_SECTIONS,
    MATCHES_PANEL_SECTIONS,
    MATRIMONIAL_PROFILE_RELATIONS,
    MATRIMONIAL_PROFILE_FIELD_FILTERS,
    MATRIMONIAL_PROFILE_BOOLEAN_FIELD_FILTERS,
    FIVE_OR_MORE_CHILDREN,
)
from core.forms import (
    CareerProfileForm,
    EducationProfileForm,
    FamilyProfileForm,
    LoginForm,
    MatrimonialProfileForm,
    PasswordChangeForm,
    PartnerPreferenceForm,
    PersonalProfileForm,
    LocationProfileForm,
    ProfileSearchForm,
    ReligiousProfileForm,
    WaliProfileForm, )
from core.models import (
    CareerProfile,
    EducationProfile,
    FamilyProfile,
    MatrimonialProfile,
    PartnerPreference,
    LocationProfile,
    ReligiousProfile,
    WaliProfile,
    ProfileView,
)
from core.service import MATCHES_FILTER_FUNCTIONS


class UserLoginView(LoginView):
    template_name = 'core/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


def indexView(request):
    if not request.user.is_authenticated:
        return render(request, 'core/home.html')

    user = get_user_model().objects.select_related(*USER_PROFILE_RELATIONS).get(pk=request.user.pk)
    setupSections = [
        {
            'label': label,
            'url': url,
            'complete': hasattr(user, relation),
        }
        for label, url, relation in PROFILE_SECTIONS
    ]

    completed = sum(section['complete'] for section in setupSections)
    context = {
        'setupSections': setupSections,
        'completedSections': completed,
        'setupPercentage': round(completed / len(setupSections) * 100),
    }
    return render(request, 'core/home.html', context)


@login_required
def searchView(request):
    oppositeGender = service.getOppositeGender(request.user)
    profiles = MatrimonialProfile.objects.select_related(*MATRIMONIAL_PROFILE_RELATIONS).exclude(user=request.user).filter(gender=oppositeGender).order_by('-user__createdAt', 'pk')

    form = ProfileSearchForm(request.GET or None, includeHijabStatus=oppositeGender == Gender.FEMALE)
    if form.is_valid():
        filters = form.cleaned_data

        if filters['minAge']:
            profiles = profiles.filter(dateOfBirth__lte=service.getDateOfBirthFromAge(int(filters['minAge'])))
        if filters['maxAge']:
            profiles = profiles.filter(dateOfBirth__gt=service.getDateOfBirthFromAge(int(filters['maxAge']) + 1))

        for field, lookup in MATRIMONIAL_PROFILE_FIELD_FILTERS.items():
            value = filters.get(field)
            if value:
                profiles = profiles.filter(**{lookup: value})

        if filters['children']:
            childFilters = Q()
            for choice in filters['children']:
                if choice == FIVE_OR_MORE_CHILDREN:
                    childFilters |= Q(children__gte=5)
                else:
                    childFilters |= Q(children=int(choice))

            profiles = profiles.filter(childFilters)

        if filters['language']:
            languageFilters = Q()
            for language in filters['language']:
                languageFilters |= Q(languages__icontains=f'"{language}"')
            profiles = profiles.filter(languageFilters)

        for field, lookup in MATRIMONIAL_PROFILE_BOOLEAN_FIELD_FILTERS.items():
            if filters.get(field):
                profiles = profiles.filter(**{lookup: filters[field][0] == 'YES'})

        if filters['citizenship']:
            citizenship_filters = Q()
            for citizenship in filters['citizenship']:
                citizenship_filters |= Q(user__locationProfile__citizenShip__icontains=f'"{citizenship}"')
            profiles = profiles.filter(citizenship_filters)

        if filters['profileCreated']:
            days = int(filters['profileCreated'])
            profiles = profiles.filter(user__createdAt__date__gte=timezone.localdate() - timedelta(days=days - 1))

        if filters['verified']:
            profiles = profiles.filter(user__isVerified=True)

    elif request.GET:
        profiles = profiles.none()

    page = Paginator(profiles, 10).get_page(request.GET.get('page'))

    queryParameters = request.GET.copy()
    queryParameters.pop('page', None)

    return render(request, 'core/search.html', {
        'form': form,
        'profiles': page,
        'queryParameters': queryParameters.urlencode(),
    })


@login_required
def matchesView(request):
    query = request.GET.get('match', '')
    profiles = MatrimonialProfile.objects.exclude(user=request.user).order_by('-user__createdAt', 'pk')

    if query in MATCHES_FILTER_FUNCTIONS:
        profiles = MATCHES_FILTER_FUNCTIONS[query](request.user)

    page = Paginator(profiles, 10).get_page(request.GET.get('page'))
    matchesHeading = next(
        (
            panel.heading
            for section in MATCHES_PANEL_SECTIONS
            for panel in section['panels']
            if panel.match == query
        ),
        'Your matches'
    )

    return render(request, 'core/matches.html', {
        'profiles': page,
        'matchesHeading': matchesHeading,
        'panelSections': MATCHES_PANEL_SECTIONS,
    })


@login_required
def profileView(request, pk):
    profile = MatrimonialProfile.objects.select_related(*MATRIMONIAL_PROFILE_RELATIONS).get(id=pk)
    service.registerProfileView(request.user, profile.user)
    return render(request, 'core/profile.html', {
        'profile': profile,
        'previousProfile': None,
        'nextProfile': None,
    })


@login_required
def settingsPersonalProfileView(request):
    form = PersonalProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(
            request,
            'Your personal profile has been updated.'
        )
        return redirect('core:settings-personal')
    return render(request, 'core/settings/settings-personal-profile.html', {'form': form})


class UserPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'core/settings/password.html'
    success_url = reverse_lazy('core:settings-password')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Your password has been changed.'
        )
        return super().form_valid(form)


@login_required
def settingsMatrimonialProfileView(request):
    profile = MatrimonialProfile.objects.filter(user=request.user).first()
    form = MatrimonialProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(
            request,
            'Your matrimonial profile has been updated.'
        )
        return redirect('core:settings-matrimonial')
    return render(request, 'core/settings/settings-matrimonial-profile.html', {'form': form})


@login_required
def settingsReligiousProfileView(request):
    profile = ReligiousProfile.objects.filter(user=request.user).first()
    form = ReligiousProfileForm(request, request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(
            request,
            'Your religious profile has been updated.'
        )
        return redirect('core:settings-religious')
    return render(request, 'core/settings/settings-religious-profile.html', {'form': form})


@login_required
def settingsEducationProfileView(request):
    profile = EducationProfile.objects.filter(user=request.user).first()
    form = EducationProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(
            request,
            'Your education profile has been updated.'
        )
        return redirect('core:settings-education')
    return render(request, 'core/settings/settings-education-profile.html', {'form': form})


@login_required
def settingsCareerProfileView(request):
    profile = CareerProfile.objects.filter(user=request.user).first()
    form = CareerProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(
            request,
            'Your career profile has been updated.'
        )
        return redirect('core:settings-career')
    return render(request, 'core/settings/settings-career-profile.html', {'form': form})


@login_required
def settingsLocationProfileView(request):
    profile = LocationProfile.objects.filter(user=request.user).first()
    form = LocationProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(
            request,
            'Your location profile has been updated.'
        )
        return redirect('core:settings-location')
    return render(request, 'core/settings/settings-location-profile.html', {'form': form})


@login_required
def settingsFamilyProfileView(request):
    profile = FamilyProfile.objects.filter(user=request.user).first()
    form = FamilyProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(
            request,
            'Your family profile has been updated.'
        )
        return redirect('core:settings-family')
    return render(request, 'core/settings/settings-family-profile.html', {'form': form})


@login_required
def settingsWaliProfileView(request):
    profile = WaliProfile.objects.filter(user=request.user).first()
    form = WaliProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(
            request,
            'Your wali profile has been updated.'
        )
        return redirect('core:settings-wali')
    return render(request, 'core/settings/settings-wali-profile.html', {'form': form})


@login_required
def partnerPreferenceSettingsView(request):
    preference = PartnerPreference.objects.filter(user=request.user).first()
    form = PartnerPreferenceForm(request.POST or None, instance=preference)
    if request.method == 'POST' and form.is_valid():
        preference = form.save(commit=False)
        preference.user = request.user
        preference.save()
        messages.success(
            request,
            'Your partner preference has been updated.'
        )
        return redirect('core:settings-preferences')
    return render(request, 'core/settings/settings-partner-preference.html', {'form': form})

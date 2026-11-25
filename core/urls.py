from django.contrib.auth.views import LogoutView
from django.urls import path

from core.views import (
    indexView,
    UserLoginView,
    searchView,
    matchesView,
    profileView,
    settingsPersonalProfileView,
    UserPasswordChangeView,
    settingsMatrimonialProfileView,
    settingsReligiousProfileView,
    settingsEducationProfileView,
    settingsCareerProfileView,
    settingsLocationProfileView,
    settingsFamilyProfileView,
    settingsWaliProfileView,
    partnerPreferenceSettingsView,
)

app_name = 'core'

urlpatterns = [
    path('', indexView, name='index-view'),
    path('login/', UserLoginView.as_view(), name='login-view'),
    path('logout/', LogoutView.as_view(next_page='core:login-view'), name='logout-view'),
    path('search/', searchView, name='search-view'),
    path('matches/', matchesView, name='matches-view'),
    path('profile/<int:pk>/', profileView, name='profile-view'),
    path('settings/personal/', settingsPersonalProfileView, name='settings-personal'),
    path('settings/password/', UserPasswordChangeView.as_view(), name='settings-password'),
    path('settings/matrimonial/', settingsMatrimonialProfileView, name='settings-matrimonial'),
    path('settings/religious/', settingsReligiousProfileView, name='settings-religious'),
    path('settings/education/', settingsEducationProfileView, name='settings-education'),
    path('settings/career/', settingsCareerProfileView, name='settings-career'),
    path('settings/location/', settingsLocationProfileView, name='settings-location'),
    path('settings/family/', settingsFamilyProfileView, name='settings-family'),
    path('settings/wali/', settingsWaliProfileView, name='settings-wali'),
    path('settings/preferences/', partnerPreferenceSettingsView, name='settings-preferences'),
]

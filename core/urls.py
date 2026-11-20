from django.urls import path
from django.contrib.auth.views import LogoutView

from core.views import (
    UserLoginView,
    UserPasswordChangeView,
    careerProfileSettingsView,
    dashboardView,
    educationSettingsView,
    familyProfileSettingsView,
    indexView,
    matrimonialProfileSettingsView,
    personalSettingsView,
    profileLocationSettingsView,
    religiousProfileSettingsView,
    waliSettingsView,
    partnerPreferenceSettingsView,
    createPartnerPreferenceView,
    updatePartnerPreferenceView,
    deletePartnerPreferenceView,
    clonePartnerPreferenceView,
)

app_name = 'core'

urlpatterns = [
    path('', indexView, name='index-view'),
    path('login/', UserLoginView.as_view(), name='login-view'),
    path('dashboard/', dashboardView, name='dashboard-view'),
    path('settings/personal/', personalSettingsView, name='settings-personal'),
    path('settings/password/', UserPasswordChangeView.as_view(), name='settings-password'),
    path('settings/matrimonial/', matrimonialProfileSettingsView, name='settings-matrimonial'),
    path('settings/family/', familyProfileSettingsView, name='settings-family'),
    path('settings/wali/', waliSettingsView, name='settings-wali'),
    path('settings/religious/', religiousProfileSettingsView, name='settings-religious'),
    path('settings/education/', educationSettingsView, name='settings-education'),
    path('settings/career/', careerProfileSettingsView, name='settings-career'),
    path('settings/location/', profileLocationSettingsView, name='settings-location'),
    path('settings/preferences/', partnerPreferenceSettingsView, name='settings-preferences'),
    path('settings/preferences/create/', createPartnerPreferenceView, name='settings-preferences-create'),
    path('settings/preferences/<int:pk>/update/', updatePartnerPreferenceView, name='settings-preferences-update'),
    path('settings/preferences/<int:pk>/delete/', deletePartnerPreferenceView, name='settings-preferences-delete'),
    path('settings/preferences/<int:pk>/clone/', clonePartnerPreferenceView, name='settings-preferences-clone'),
    path('logout/', LogoutView.as_view(next_page='core:login-view'), name='logout-view'),
]

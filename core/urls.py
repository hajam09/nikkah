from django.urls import path
from django.contrib.auth.views import LogoutView

from core.views import (
    UserLoginView,
    UserPasswordChangeView,
    dashboardView,
    educationSettingsView,
    indexView,
    matrimonialProfileSettingsView,
    personalSettingsView,
    religiousProfileSettingsView,
)

app_name = 'core'

urlpatterns = [
    path('', indexView, name='index-view'),
    path('login/', UserLoginView.as_view(), name='login-view'),
    path('dashboard/', dashboardView, name='dashboard-view'),
    path('settings/personal/', personalSettingsView, name='settings-personal'),
    path('settings/password/', UserPasswordChangeView.as_view(), name='settings-password'),
    path('settings/matrimonial/', matrimonialProfileSettingsView, name='settings-matrimonial'),
    path('settings/religious/', religiousProfileSettingsView, name='settings-religious'),
    path('settings/education/', educationSettingsView, name='settings-education'),
    path('logout/', LogoutView.as_view(next_page='core:login-view'), name='logout-view'),
]

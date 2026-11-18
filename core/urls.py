from django.urls import path
from django.contrib.auth.views import LogoutView

from core.views import UserLoginView, dashboardView, indexView

app_name = 'core'

urlpatterns = [
    path('', indexView, name='index-view'),
    path('login/', UserLoginView.as_view(), name='login-view'),
    path('dashboard/', dashboardView, name='dashboard-view'),
    path('logout/', LogoutView.as_view(next_page='core:login-view'), name='logout-view'),
]

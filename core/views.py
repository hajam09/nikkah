from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render

from core.forms import LoginForm


class UserLoginView(LoginView):
    template_name = 'core/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


def indexView(request):
    return render(request, 'core/home.html')


@login_required
def dashboardView(request):
    return render(request, 'core/dashboard.html')

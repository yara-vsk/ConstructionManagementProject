from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.urls import reverse_lazy
from .custommixins import UserAuthenticatingMixin

from .form import UserRegistrationForm, CustomAuthenticationForm
from django.views import View


# Create your views here.


class RegisterUserView(UserAuthenticatingMixin, View):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    redirect_url = '/'

    def test_func(self):
        return not self.request.user.is_authenticated

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('/')
        return render(request, self.template_name, {'form': form})


class CustomLoginView(UserAuthenticatingMixin, View):
    form_class = CustomAuthenticationForm
    template_name = 'users/registration.html'
    redirect_url = '/'

    def test_func(self):
        return not self.request.user.is_authenticated

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect('/')
        return render(request, self.template_name, {'form': form})


class CustomLogoutView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .custommixins import UserAuthenticatingMixin
from .tokens import account_activation_token
from .form import UserRegistrationForm, CustomAuthenticationForm
from django.views import View


# Create your views here.

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user =None

    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('login')
    return redirect('registration')


def activate_info(request):
    return render(request, template_name='users/activate_info.html')


def activate_email(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string('users/template_activate_account.html',{
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    print("emmmmmm")
    if email.send():
        print("send_EMMMMM")



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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            return HttpResponseRedirect(reverse_lazy('activate-info'))
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



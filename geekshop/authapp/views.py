from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.views.generic import UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

# Create your views here.

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basket.models import Basket
from adminapp.mixins import BaseClassContextMixin, CustomDispatchMixin
from authapp.models import User


class Login(LoginView, BaseClassContextMixin, CustomDispatchMixin):
    form_class = UserLoginForm
    title = 'GeekShop | Авторизация'
    template_name = 'authapp/login.html'


class RegisterFormView(FormView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    title = 'GeekShop | Registration'
    form_class = UserLoginForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('authapp:login')

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            if self.send_verify_link(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(request, 'Вы успешно зарегистрировались!')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(request, form.errors)
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        return render(request, self.template_name, {'form': form})

    def send_verify_link(self, user):
        verify_link = reverse('authapp:verify', args=[
                              user.email, user.activation_key])
        subject = f'Для активации учётной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учётной записи {user.username} на портале \n {settings.DOMAIN_NAME}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silenty=False)

    def verify(self, email, activate_key):
        try:
            user = User.objects.get(email=email)
            if user and (user.is_activation_key == activate_key) and not user.is_activation_key_expired():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_activate = True
                user.save()
                auth.login(self, user)
            return render(self, 'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))


class ProfileFormView(UpdateView, BaseClassContextMixin, CustomDispatchMixin):
    model = User
    template_name = 'autapp/profile.html'
    form_class = UserProfileForm
    seccess_url = reverse_lazy('authapp:profile')
    title = 'GeekShop | Profile'

    def form_valid(self, form):
        messages.set_level(self.request, messages.SUCCESS)
        messages.success(self.request, 'Данные успешно обновились!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.pk)


class Logout(LogoutView):
    template_name = 'mainapp/index.html'

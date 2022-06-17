from django.conf import settings
from django.core.mail import send_mail
from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView, FormView
from django.views.generic import UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

# Create your views here.

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileUpdateForm
from adminapp.mixins import BaseClassContextMixin, UserDispatchMixin
from authapp.models import User
from basket.models import Basket


class Login(LoginView, BaseClassContextMixin):
    form_class = UserLoginForm
    title = 'GeekShop | Авторизация'
    template_name = 'authapp/login.html'


class RegisterFormView(FormView, BaseClassContextMixin):
    model = User
    title = 'GeekShop | Registration'
    form_class = UserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('authapp:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(request, 'Вы успешно зарегистрировались')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(request, form.errors)
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        context = {'form': form}
        return render(request, self.template_name, context)

    @staticmethod
    def send_verify_link(user):
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activate_key):
        try:
            user = User.objects.get(email=email)
            if user and (user.activation_key == activate_key and not user.is_activation_key_expired()):
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(
                    self, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(self.request, 'authapp/verification.html')
        except NameError:
            return HttpResponseRedirect(reverse('index'))


class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    model = User
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('authapp:profile')
    title = 'GeekShop | Profile'

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileUpdateForm(
            data=request.POST, files=request.FILES, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data()
        context['profile'] = UserProfileUpdateForm(instance=self.request.user.userprofile)
        return context

    def form_valid(self, form):
        messages.set_level(self.request, messages.SUCCESS)
        messages.success(self.request, 'Вы успешно сохранили профиль')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.pk)


class Logout(LogoutView):
    template_name = 'mainapp/index.html'

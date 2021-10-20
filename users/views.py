from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages, auth
from django.urls import reverse_lazy, reverse

# Create your views here.


from django.views.generic import FormView, UpdateView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin, CustomAuthMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User


class ListLoginView(LoginView, BaseClassContextMixin):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'

#
# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'GeekShop - Авторизация',
#         'form': form
#     }
#     return render(request, 'users/login.html', context)


class RegisterFormView(FormView, BaseClassContextMixin):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    cancel_url = reverse_lazy('users:register')
    title = 'GeekShop - Регистрация'

    def send_verify_link(self, request, *args, **kwargs):
        verify_link = reverse('users:verify', args=[request.email, request.activation_key])
        subject = f'Для активации учетной записи {request.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {request.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [request.email], fail_silently=False)

    def verify(request, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activation_key and not user.is_activation_key_expired():
                user.activation_key = ''
                user.activation_key_created = None
                user.is_active = True
                user.save()
                auth.login(request, user)
            return render(request, 'users/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.success(request, 'Вы успешно зарегистрировались')
            return redirect(self.success_url)
        else:
            messages.error(request, 'Ошибка регистрации')
            return redirect(self.cancel_url)


class ProfileFormView(UpdateView, BaseClassContextMixin, CustomAuthMixin):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    title = 'GeekShop - Профиль'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    # def get_context_data(self, **kwargs):
    #     context = super(ProfileFormView, self).get_context_data(**kwargs)
    #     context['baskets'] = Basket.objects.filter(user=self.request.user)
    #     return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно обновили профиль')
            return redirect(self.success_url)
        else:
            messages.error(request, 'Профиль не сохранен')
            return redirect(self.success_url)
#
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно обновили профиль')
#             return HttpResponseRedirect(reverse('users:profile'))
#         # else:
#         #     messages.error(request, 'Профиль не сохранен')
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     context = {
#         'title': 'GeekShop - Profile',
#         'form': form,
#         'baskets': Basket.objects.filter(user=request.user)
#     }
#     return render(request, 'users/profile.html', context)


class Logout(LogoutView):
    template_name = 'mainapp/index.html'

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))



# def send_verify_link(user):
#     verify_link = reverse('users:verify',args=[user.email,user.activation_key])
#     subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
#     message = f'Для подтверждения учетной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
#     return send_mail(subject,message,settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
#
#
# def verify(request, email, activation_key):
#     try:
#         user = User.objects.get(email=email)
#         if user and user.activation_key == activation_key and not user.is_activation_key_expired():
#             user.activation_key = ''
#             user.activation_key_created = None
#             user.is_active = True
#             user.save()
#             auth.login(request, user)
#         return render(request, 'users/verification.html')
#     except Exception as e:
#         return HttpResponseRedirect(reverse('index'))

class ForgotPassword(FormView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    cancel_url = reverse_lazy('users:register')
    title = 'GeekShop - Обновление пароля'

    def send_verify_password(self, request, *args, **kwargs):
        verify_link = reverse('users:verify', args=[request.email, request.activation_key])
        subject = f'Для активации учетной записи {request.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {request.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [request.email], fail_silently=False)

    def verify(self, request, email):
        try:
            user = User.objects.get(email=email)
            user.save()
            auth.login(request, user)
            return render(request, 'users/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            if self.send_verify_password():
                form.save()
                messages.success(request, 'Вы успешно зарегистрировались')
            return redirect(self.success_url)
        else:
            messages.error(request, 'Ошибка регистрации')
            return redirect(self.cancel_url)
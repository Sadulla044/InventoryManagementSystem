from django.shortcuts import (
    render,
    redirect,
    get_list_or_404
)
from django.views import View
from django.contrib.auth import (
    login,
    logout,
    authenticate
)
from django.core.mail import send_mail

from django.contrib.auth.hashers import make_password
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode
)
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from random import randint
from django.conf.global_settings import EMAIL_HOST_USER
from django.http import HttpResponse

from .models import Users
from .forms import (
    SignUpForm,
    LoginForm,
    EditForm
)
from .code import Code


class SignUp(View):
    template_name = 'signup.html'
    subject_template_name = 'verification.txt'
    from_email = EMAIL_HOST_USER
    title = 'Verification code'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            password = request.POST.get('password')
            confirm = request.POST.get('confirm')
            if password == confirm:
                user = form.save(commit=False)
                user.password = make_password(password=password)
                user.is_active = False
                user.save()
                code = randint(100000, 999999)
                session = Code(request=request)
                session.add(id=user.id, code=code)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                context = {
                    'domain': '127.0.0.1:8000',
                    'uid': uid,
                    'protocol': 'http',
                    'code': code
                }
                email = render_to_string(self.subject_template_name, context=context)
                try:
                    send_mail(self.title, email, self.from_email, [user.email], fail_silently=False)
                except Exception:
                    return HttpResponse('Email error')
                return render(request, template_name='verification.html', context={
                    'uid': uid
                })
            else:
                return HttpResponse('Didn\'t match')
        else:
            return HttpResponse('Form error')


class Login(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user=user)
            return HttpResponse('Main page')
        else:
            return redirect('auth:login')


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponse('Main Page')


class EditAccount(View):
    template_name = ''

    def get(self, request, pk, *args, **kwargs):
        user = get_list_or_404(Users, pk=pk)
        form = EditForm(instance=user)
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request, pk, *args, **kwargs):
        user = get_list_or_404(Users, pk=pk)
        form = EditForm(data=request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            login(request, user=user)
            return redirect('Main Page')
        else:
            return redirect('Edit page', 'error massage (form is invalid)')


class AccountVerification(View):
    template_name = 'verification.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        uid = request.POST.get('uid')
        code = request.POST.get('code')
        if code:
            user_id = urlsafe_base64_decode(uid).decode()
            session = Code(request=request)
            user_code = session.get(id=user_id)
            if int(code) == int(user_code):
                user = Users.objects.get(id=user_id)
                user.is_active = True
                user.save()
                login(request, user=user)
                return HttpResponse('Main page')
            else:
                return HttpResponse('Code error')
        else:
            return HttpResponse('Error')

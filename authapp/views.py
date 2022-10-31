from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Activate account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str

# Email activation
from django.core import mail
from django.core.mail import send_mail, BadHeaderError, EmailMessage, EmailMultiAlternatives
from django.conf import settings

# reset password generators
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .forms import SignUpForm, PasswordResetForm
from .utils import account_activation_token

#Email thread
import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def home(request):
    return render(request, 'authapp/home.html')

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # check if user exists
            if User.objects.filter(username=user.username).exists():
                messages.error(request, 'Username already exists')
                return redirect('signup')
            elif User.objects.filter(email=user.email).exists():
                messages.error(request, 'Email already exists')
                return redirect('signup')

            #check if passwords match
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2:
                user.set_password(password1)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('authapp/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                EmailThread(email).start()
                messages.success(request, 'Account created successfully. Please check your email to activate your account.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('signup')

    context = {'form': form}
    return render(request, 'authapp/signup.html', context)

def loginuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'authapp/login.html')

def logoutuser(request):
    logout(request)
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('home')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('home')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "[Password Reset Requested]"
                    email_template_name = "authapp/password_reset_email.html"
                    c = {
                    "email":user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'DjangoAuthentication',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': PasswordResetTokenGenerator().make_token(user),
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        email_message = EmailMessage(
                            subject, email, 'DjangoAuthentication' +'' , [user.email]
                        )
                        EmailThread(email_message).start()
                        messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                        return redirect("login")
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    context = {'password_reset_form': password_reset_form}
    return render(request=request, template_name="authapp/password_reset.html", context=context)

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successful')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('password_reset_confirm', uidb64=uidb64, token=token)
        return render(request, 'authapp/password_reset_confirm.html')
    else:
        messages.error(request, 'The reset link is no longer valid')
        return redirect('password_reset')


def profile(request):
    return render(request, 'authapp/profile.html')







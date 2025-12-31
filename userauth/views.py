from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail    
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .validator import activate_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from .models import CustomUser, VertifyUser
from .forms import UserSignUp, LoginForm, UserSignUp, passwordChangeForm 
from django.utils import timezone
from django.contrib import messages


@csrf_protect
def home(request):
    user = CustomUser.objects.all()
    return render(request, '../templates/plate/home.html',{'user': user})  


@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = UserSignUp(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            nickname = form.cleaned_data.get('nickname')
            password = form.cleaned_data.get('password')
            last_name = form.cleaned_data.get('last_name')
            first_name = form.cleaned_data.get('first_name')
            user = CustomUser(email=email, nickname=nickname, last_name=last_name, first_name=first_name)
            user.set_password(password)
            user.is_active = False 
            user.is_verified = False
            user.save()
            logout(request)
            verify_user = VertifyUser.objects.create(user=user)
            gen = verify_user.generate_code()
            verify_user.code = gen
            verify_user.save()
            current_site = get_current_site(request)
            message = render_to_string('../templates/userauth/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'gen_code': gen,
            })
            message = strip_tags(message)
            mail_subject = 'Activate your account.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            try:
                send_mail(mail_subject, message, email_from, recipient_list)
            except Exception as e:
                print(f'Email sending failed: {str(e)}')
            domain = current_site.domain
            messages.success(request, 'Please check your email to verify your account.')
            return render(request, 'userauth/checkemailmsg.html', {'domain': domain})
        else:
            return render(request, '../templates/userauth/signup.html', {'form': form})
    else:
        form = UserSignUp()
    return render(request, '../templates/userauth/signup.html', {'form': form})


@csrf_protect
def signin(request):
    form = LoginForm(data=request.POST)
    next_url = request.GET.get('next')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            print(email, password)
            if user is not None:
                login(request, user)
                return redirect('voting:x6sad_dashboard')
            else:
                return render(request, '../templates/userauth/login.html', {'form': form, 'next': next_url, 'error': 'Invalid email or password'})
    return render(request, '../templates/userauth/login.html', {'form': form, 'next': next_url})


@require_http_methods(['POST'])
def signout(request):
    logout(request)
    return redirect('/')
     

@csrf_protect
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = CustomUser.objects.get(email=email)
                current_site = get_current_site(request)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                email_body = render_to_string('authentication_app/password_reset/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                    'protocol': 'http',
                    'site_name': '',
                })
                email_subject = 'Password reset on ' + current_site.domain
                email_body = strip_tags(email_body)
                try:
                    email = send_mail(email_subject, email_body, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])
                    # email.send()
                    return render(request, 'authentication_app/password_reset/password_reset_done.html')
                except Exception as e:
                    return render(request, "{error message: address not found. " + str(e) + "}")
            except CustomUser.DoesNotExist:
                form.add_error(None, 'Email address not found, try again')
    else:
        form = PasswordResetForm()
    return render(request, 'authentication_app/password_reset/password_reset_form.html', {'form': form})


@csrf_protect
def resetPage(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        newuser = User.objects.create_user( password = password, confirmPassword = confirmPassword)
        try:
            newuser.save()
        except ValueError:
            return HttpResponse('Please go back!') 
    else:
        form = LoginForm()
    return render(request, 'authentication_app/password_reset/password_reset_form.html')


@csrf_protect
def resetPageDone(request):
     return render(request, 'authentication_app/password_reset/password_reset_done.html')


@csrf_protect
def reset_password_confirm(request, uidb64, token):
    try:
        uid =force_str(urlsafe_base64_decode(uidb64))
        user = UserSignUp.objects.get(pf=uid)
    except(UserSignUp.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = passwordChangeForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data.get('password')
                user.set_password(new_password)
                user.save()
                user =authenticate(request, email=user.email, password=new_password)
                login(request, user)
                
                return render(request, 'authentication_app/password_reset/password_reset_complete.html')
        else:
            form = passwordChangeForm()
        return render(request, 'authentication_app/password_reset/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'authentication_app/password_reset/404.html')
    

@csrf_protect
def email_verification(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        print(f"Code received: {code}")
        if not code:
            messages.error(request, 'Please enter the verification code.')
            return render(request, 'userauth/email_verification.html')
        try:
            verifyuser = VertifyUser.objects.get(code=code)
            print(f"verifyuser found: {verifyuser}")
        except VertifyUser.DoesNotExist:
            messages.error(request, 'Invalid verification code.')
            return render(request, 'userauth/email_verification.html')
        if timezone.now() > verifyuser.is_expired:
            messages.error(request, 'Verification code has expired.')
            return render(request, 'userauth/email_verification.html')
        user = verifyuser.user
        print(f"User found: {user}")
        if not user.is_active:
            user.is_active = True
            user.is_verified = True
            user.save()
            login(request, user, backend='userauth.backends.EmailBackend')
            messages.success(request, 'Your account has been successfully verified!')
            return redirect('voting:x6sad_dashboard')
        else:
            messages.info(request, 'Your account is already verified.')
            return redirect('voting:x6sad_dashboard')

    return render(request, 'userauth/email_verification.html')
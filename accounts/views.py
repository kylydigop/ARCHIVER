from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.mail import send_mail

from django.contrib.auth import get_user_model

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template

from django.utils.encoding import force_bytes, force_str

from django.http import HttpResponse


from .models import PDFBaseUser
from .form import RegisterForm,LoginForm
from .tokens import account_activation_token

# Create your views here.

class loginPage(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect('/search/home')
        else:
            context = {
                'form' : form,
            }
            return render(request, template_name='loginPage.html', context=context)

    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST)

        if form.is_valid():
            userId = form.cleaned_data['userId']
            studentNumber = form.cleaned_data['studentNumber']
            password = form.cleaned_data['password']
            user = authenticate(request, username=userId, password=password)
        else:
            userId = form.cleaned_data['userId']
            password = form.cleaned_data['password']
            user = authenticate(request, username=userId, password=password)
            

        if user is not None:
            login(request, user)
            return redirect('/search/home')
        else:
            messages.error(request, "Incorrect User ID or Password, please try again.")
            print('User is incorrect')
        context={
            'form' : form,
        }
        return render(request, template_name='loginPage.html', context=context)


class registerPage(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        
        
        context = {
            'form' : form,
        }

        return render(request, template_name='registerPage.html', context=context)
    
    def post(self, request, *args, **kwargs):
        email_from = 'faithmary.galon04@gmail.com'
        form = RegisterForm(request.POST)
        if form.is_valid():            
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            studentNumber = form.cleaned_data['studentNumber']
           
            user = form.save(commit=False)
            user.is_active = False

            if user.is_active is False:
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                message = render_to_string('email_template.html', {
                    'user' : user,
                    'domain' : current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data['email']
                send_mail(mail_subject, message, email_from, [to_email])
                messages.success(request, "Please confirm your email address to complete the registration.")
                return redirect('login')
            else:
                messages.error(request, "User already exists")
                return redirect('login')
            
        context = {
            'form' : form
        }

        return render(request, template_name='registerPage.html', context=context)

class profilePage(View):

    def get(self, request, userId, *args, **kwargs):
        User = get_user_model()

        pdfUser = User.objects.get(userId=userId)
        context = {
            'user' : pdfUser,
        }

        return render (request,template_name='profilePage.html', context=context)

class activatePage(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Thank you for your email confirmation. <br /> You can now login to your account.")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid.")
            return redirect('login')

@login_required(login_url='/')
def logoutUser(request):
    logout(request)
    return redirect('/')






from django.shortcuts import render, redirect
from .forms import RegistrationForm, Login_form, EditAccountForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import send_general_msg
from messaging.models import General_Message


# Homepage
@login_required(login_url='login_page')
def homepage(request):
    if request.POST:
        created = len(General_Message.objects.filter(content=request.POST['text']))==0
        if created:
            new_msg = General_Message.objects.create(content=request.POST['text'])
            general_msg = {'content': new_msg.content }
            group_name = 'general_message'
            send_general_msg(group_name, general_msg)


    return render(request,'Account/homepage.html')

# Registration page
def register(request):
    context= {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email,password=raw_password)
            messages.success(request,'Account created!')
            login(request,account)
            return redirect('entry')
        else:
            context['registration_form'] = form
            messages.error(request,'')
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request,'Account/register.html',context)

# Login page
def Login(request):
    context = {}

    user = request.user

    if user.is_authenticated:
        return redirect('entry')
    if request.POST:
        form = Login_form(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)

            if user:
                login(request,user)
                messages.info(request,'Logged in!')
                return redirect('entry')
    else:
        form = Login_form()

    context['login_form'] = form

    return render(request,'account/login.html',context)


# Logout
def Logout(request):
    logout(request)
    messages.info(request,'Logged out!')
    return redirect('login_page')

# Editing page
@login_required(login_url='login_page')
def EditProfile(request):
    context= {}
    user = request.user
    if request.POST:
        # print("REQUEST", request.POST)
        form = EditAccountForm(request.POST, instance=user, initial={'fname':user.first_name})
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email,password=raw_password)
            messages.success(request,'Account Updated!')
            # login(request,account)
            print("VAAALIIID")
            return redirect('profile_page')

        else:
            print("NOOOT VAAALIIID")
            context['edit_form'] = form
            messages.error(request,'')
            return redirect('homepage')
    else:
        form = EditAccountForm(instance=request.user)
        context['edit_form'] = form
    return render(request,'Account/edit_page.html',context)

# Website page
def conf_website(request):
    return render(request,'Account/Conference_site.html')


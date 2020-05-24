import secrets
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .forms import UserSignUpForm, UserAuthenticationForm
from django.contrib.auth import authenticate, login

def welcome(request) :
    return render(request,'accounts/welcome.html')

def userSignUp(request):
    if request.method == 'POST' :
        form =  UserSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')

            if(password1 == password2):
                if User.objects.filter(username=username).exists():
                    form =  UserSignUpForm(request.GET)                
                    message = 'Username already exist'
                    type_form = 'signup'
                    context = {'form':form,'message':message,'type_form':type_form}
                    return render(request,'accounts/authentication.html',context)
        
                elif User.objects.filter(email=email).exists():
                    form =  UserSignUpForm(request.GET)
                    message = 'Email already exist'
                    type_form = 'signup'
                    context = {'form':form,'message':message,'type_form':type_form}
                    return render(request,'accounts/authentication.html',context)

                else :
                    user = User.objects.create_user(username=username,password=password1,email=email)
                    user.save()
                    user = authenticate(request, username=username, password=password1)
                    if user is not None :
                        print("User registered and authenticated")
                        login(request, user)
                        return redirect('/blogs/edit_profile/')
                    
                    else :
                        form =  UserAuthenticationForm()
                        message = 'User authentcation failed'
                        type_form = 'login'
                        context = {'form':form,'message':message,'type_form':type_form}
                        return render(request,'accounts/authentication.html',context)

            else :
                form =  UserSignUpForm(request.GET)
                message = 'Passwords do not match'
                type_form = 'signup'
                context = {'form':form,'message':message,'type_form':type_form}
                return render(request,'accounts/authentication.html',context)
        
        else :
            form =  UserSignUpForm(request.GET)
            message = 'Invalid Credentials'
            type_form = 'signup'
            context = {'form':form,'message':message,'type_form':type_form}
            return render(request,'accounts/authentication.html',context)

    else :
        form = UserSignUpForm(request.GET)
        message=''
        type_form='signup'
        context = {'form':form,'message':message,'type_form':type_form}
        return render(request,'accounts/authentication.html',context)


def userLogin(request):
    if request.method == 'POST' :
        form =  UserAuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None :
                print("User Authenticated")
                login(request, user)
                return redirect('/blogs/')

            else :
                form =  UserAuthenticationForm()
                message = 'Authentication Error'
                type_form = 'signup'
                context = {'form':form,'message':message,'type_form':type_form}
                return render(request,'accounts/authentication.html',context)    

        else :
            form =  UserAuthenticationForm()
            message = 'Invalid Credentials'
            type_form = 'login'
            context = {'form':form,'message':message,'type_form':type_form}
            return render(request,'accounts/authentication.html',context)   

    else :
        form =  UserAuthenticationForm()
        message = ''
        type_form = 'login'
        context = {'form':form,'message':message,'type_form':type_form}
        return render(request,'accounts/authentication.html',context)  





from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.

from .forms import  RegistrationForm, LoginForm
from django.contrib.auth.models import User,auth

from .models import CookieConsent

import secrets
import string
import requests

def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/meme/login/')
    
    sid = request.COOKIES['sessionid']
    return render(request,'home.html',{'title':'Accept Cookies','SID':sid})

def register(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/meme/')
        
    error = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            fname = request.POST['first_name']
            lname = request.POST['last_name']
            uname = request.POST['username']
            email = request.POST['email']
            pwd = request.POST['password']
            cpwd = request.POST['confirm_password']

            if( pwd == cpwd):
                if ( User.objects.filter(username=uname).exists()):
                    error = 'Username already taken'
                    print(error)
                else:
                    user = User.objects.create_user(username = uname, password = pwd , email=email, first_name = fname, last_name = lname)
                    user.save()

                    return HttpResponseRedirect('/meme/login/')
            else:
                error = 'Password Mismatched'
    else:
        form = RegistrationForm()

    return render(request,'register.html',{'form': form,'title':'Register User','error' :error})

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/meme/')
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            uname = request.POST['username']
            pwd = request.POST['password']

            user = auth.authenticate(username=uname, password=pwd)
            if( user is not None):
                auth.login(request,user)
                return redirect('/meme/')
            else:
                error = 'Password Mismatched'
    else:
        form = LoginForm()
    return render(request,'login.html',{'form': form,'title':'Register User','error' :error})

def logout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/meme/login/')
    else:
        auth.logout(request)
        return HttpResponseRedirect('/meme/')

def acceptCookies(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/meme/login/')
    else:
        sid = request.COOKIES['sessionid']
        print(sid)
        print(request.user.username)
        cc = CookieConsent.objects.create(user = request.user.username, sessn=sid, concent=True)
        cc.save()
        response = requests.get('https://api.imgflip.com/get_memes')
        memes = response.json()
        return render(request,'index.html',{'title':'Memes', 'data':memes["data"]["memes"]}) 

def rejectCookies(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/meme/login/')
    else:
        sid = request.COOKIES['sessionid']
        print(sid)
        print(request.user.username)
        cc = CookieConsent.objects.create(user = request.user.username, sessn=sid, concent=False)
        cc.save()
        auth.logout(request)
        return render(request,'denied.html')
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.

from .forms import TextForm, RegistrationForm, LoginForm, EncKeyForm
from django.contrib.auth.models import User,auth
from .models import TextInfo



import secrets
import string

def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/textsharing/login/')
    return render(request,'home.html',{'title':'Create Text'})

def thanks(request,hash=''):
    return render(request,'thanks.html',{'hash':hash,'title':'Shared Text Created Successfully'})

def view_shared_text(request,hash=''):
    if not request.user.is_authenticated:
        print('Login first')
        return HttpResponseRedirect('/textsharing/login/')
    if hash != '':
        page = '/textsharing/view/'
        page += hash
        data = TextInfo.objects.filter(hash=hash).first()
        if (data is not None):
            if request.method == 'POST':
                form = EncKeyForm(request.POST)
                key = request.POST['enc_key']
                if (key == data.enc_key):
                    data = encrypt(data.text,key)
                    return render(request, 'viewtext.html', {'data': data, 'renderForm': False})
                else:
                    return render(request, 'viewtext.html', {'form': form,'renderForm': True, 'page':page})
            else:
                if not data.isEnc:
                    return render(request, 'viewtext.html', {'data': data.text,'renderForm': False})
                else:
                    form = EncKeyForm()
                    return render(request, 'viewtext.html', {'form': form,'renderForm': True, 'page':page})
        else:
            print('Inalid Hash Value')
            return HttpResponseRedirect('/textsharing/')
    else:
        print('No hash Value received')
        return HttpResponseRedirect('/textsharing/')

    


def create_sharable_url(request):
    if not request.user.is_authenticated:
        print('LOgin first')
        return HttpResponseRedirect('/textsharing/login/')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TextForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            text = request.POST['text_msg']
            if ('enc' in request.POST): 
                if ( request.POST['enc'] == 'on'):
                    enc = True
                else:
                    enc = False
            else:
                enc = False
            enc_key = request.POST['enc_key']
            if( not enc):
                enc_key = ''  
            else:
                text = encrypt(text,enc_key)  
            sharedText = TextInfo.objects.create(text = text, isEnc= enc, enc_key = enc_key, hash = getHash(32))
            sharedText.save()


            return HttpResponseRedirect('../thanks/'+ sharedText.hash)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TextForm()

    return render(request, 'name.html', {'form': form})

def register(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/textsharing/')
        
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

                    return HttpResponseRedirect('/textsharing/login/')
            else:
                error = 'Password Mismatched'
    else:
        form = RegistrationForm()

    return render(request,'register.html',{'form': form,'title':'Register User','error' :error})

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/textsharing/')
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
                return redirect('/textsharing/')
            else:
                error = 'Password Mismatched'
    else:
        form = LoginForm()
    return render(request,'login.html',{'form': form,'title':'Register User','error' :error})

def logout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/textsharing/login/')
    else:
        auth.logout(request)
        return HttpResponseRedirect('/textsharing/')


def getHash(length):
    return secrets.token_hex(length)


def encrypt(data,key):
    m = len(key)
    n = len(data)
    d = data.encode()
    t = key.encode()
    if (m == 0 or n == 0):
        return data
    j = 0
    tmp = ''
    for i in range(n):
        tmp = tmp + chr(d[i]^t[j])
        j = (j + 1)%m
    
    return tmp
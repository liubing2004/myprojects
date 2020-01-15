from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout,login 
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.http import HttpResponse, Http404

from django.conf import settings
from django.contrib.auth.models import User
from core.models import *
import os, zipfile, time, hashlib
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import utils, shutil
#from matplotlib.font_manager import path
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.conf import POSTBACK_ENDPOINT, SANDBOX_POSTBACK_ENDPOINT
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return myprofile(request)

def login_view(request):    
    error_messages = list()
    if request.method == 'GET':
        next = request.REQUEST.get('next', "/")
        return render_internal(request,'index/login.html',
                      {"next":next, "error_messages":error_messages})
    elif request.method == 'POST':
        email = request.POST.get("email","").strip()
        password = request.POST.get("password","").strip()
        next = request.POST.get("next", "/").strip()
        user = authenticate(username=email,password=password)
        if not user == None:
            login(request,user)                  
            return redirect(next)
        
        #redirect to login page
        error_messages.append("Email or password is wrong.")
        return render_internal(request,'index/login.html',
                      {"next":next,"error_messages":error_messages})
    
def logout_view(request):
    logout(request)
    return redirect("/")

@transaction.atomic
def register(request):
    error_messages = list();
    if request.method == 'GET':
        return render_internal(request,'index/signup.html',{'error_messages':error_messages})
    
    #email format verfication should be done in FE
    email = request.POST.get("email","").strip()
    passwd = request.POST.get("pass_confirmation", "").strip()
    passwd_confirm = request.POST.get("pass", "")
    name = request.POST.get("name", "").strip()
    
    if len(email)==0 or len(passwd)==0 or passwd != passwd_confirm:
        error_messages.append("Invalid email or password.")
        return render_internal(request,'index/signup.html',{'error_messages':error_messages})

    try:
        validate_email(email)
    except ValidationError as e:
        error_messages.append("Invalid email.")
        return render_internal(request,'index/signup.html',{'error_messages':error_messages})

    #first need to check whether email had been registered already or not
    if User.objects.filter(email=email).count() > 0:
        error_messages.append("User already exists.")
        return render_internal(request,'index/signup.html',{'error_messages':error_messages})
    
    try: 
        user = User.objects.create_user(username=email, email=email, password=passwd)
        user.save()
        profile = UserProfile(user=user, name=name)
        profile.save()
        user = authenticate(username=email,password=passwd)
        login(request,user)  
        return redirect('/')
    except Exception,e:
        raise e
        error_messages.append("Cannot create user.");
        return render_internal(request,'index/signup.html',{'error_messages':error_messages})
    

@login_required(login_url='/login')
def myprofile(request):    
    if request.method == "POST":
        user_name = request.POST.get("user_name", "")
        user_phone = request.POST.get("user_phone", "")
        uf = UserProfile.objects.get(user=request.user)
        uf.name = user_name
        uf.save()
        
    return render_internal(request,'myaccount/myprofile.html',
                           {})
    


    
def aboutus(request):
	return render_internal(request, 'index/aboutus.html', {})

    

 

"""
internal function
"""    
def render_internal(request, url, dirs):
    new_dirs = dirs
    if request.user.id != None:
        uf = UserProfile.objects.get(user=request.user)
        new_dirs["uf"] = uf
    return render(request, url, new_dirs)







    
    

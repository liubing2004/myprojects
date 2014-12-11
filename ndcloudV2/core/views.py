from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout,login 
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction

from django.conf import settings
from django.contrib.auth.models import User
from core.models import *
import os

# Create your views here.
def index(request):
    #response = render(request,'index/index.html',{})
    return render(request, 'ndmodel/project_list.html', {})

def login_view(request):    
    error_messages = list()
    print request.method
    print request
    if request.method == 'GET':
        next = request.REQUEST.get('next', "/")
        return render(request,'index/login.html',
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
        return render(request,'index/login.html',
                      {"next":next,"error_messages":error_messages})
    
def logout_view(request):
    logout(request)
    return redirect("/")

@transaction.atomic
def register(request):
    error_messages = list();
    if request.method == 'GET':
        return render(request,'index/signup.html',{'error_messages':error_messages})
    
    #email format verfication should be done in FE
    email = request.POST.get("email","").strip()
    passwd = request.POST.get("pass_confirmation", "").strip()
    passwd_confirm = request.POST.get("pass", "")
    name = request.POST.get("name", "").strip()
    
    if len(email)==0 or len(passwd)==0 or passwd != passwd_confirm:
        error_messages.append("Invalid email or password.")
        return render(request,'index/signup.html',{'error_messages':error_messages})

    try:
        validate_email(email)
    except ValidationError as e:
        error_messages.append("Invalid email.")
        return render(request,'index/signup.html',{'error_messages':error_messages})

    #first need to check whether email had been registered already or not
    if User.objects.filter(email=email).count() > 0:
        error_messages.append("User already exists.")
        return render(request,'index/signup.html',{'error_messages':error_messages})
    
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
        return render(request,'index/signup.html',{'error_messages':error_messages})
    

@login_required(login_url='/login')
def myprofile(request):
    profile = UserProfile.objects.get(user=request.user)
    print profile
    return render(request,'myaccount/myprofile.html',{"userprofile":profile})


@login_required(login_url='/login')
@transaction.atomic
def upload_project(request):
    if request.method == 'GET':
        return render(request,'myaccount/upload.html',{})
    project_name = request.POST.get("name", "").strip()
    user = request.user
    project_profile = ProjectProfile(user=user, name=project_name)
    project_profile.save()
    
    for key, file in request.FILES.items():
        directory = settings.BASE_DIR+"/medias/upload/%d/original/" %(project_profile.id)
        if not os.path.exists(directory):
            os.makedirs(directory)
        path = directory + file.name
        print path
        dest = open(path, 'w')
        if file.multiple_chunks:
            for c in file.chunks():
                dest.write(c)
        else:
            dest.write(file.read())
        dest.close()
    return render(request, 'myaccount/upload_confirm.html', {})

   

def project_detail(request, project_id):
    project = get_object_or_404(ProjectProfile, pk=project_id)
    return render(request, 'ndmodel/project_detail.html', {'project':project})

def project_list(request):
    projects = list()
    return render(request, 'ndmodel/project_list.html', {'projects':projects})
    
def aboutus(request):
	return render(request, 'index/aboutus.html', {})
    
    

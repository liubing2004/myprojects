from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout,login 
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction

from django.conf import settings
from django.contrib.auth.models import User
from core.models import *
import os, zipfile

import utils

# Create your views here.
def index(request):
    return project_list(request)

def login_view(request):    
    error_messages = list()
    print request.method
    print request
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
    profile = UserProfile.objects.get(user=request.user)
    return render_internal(request,'myaccount/myprofile.html',{"userprofile":profile})


@login_required(login_url='/login')
@transaction.atomic
def upload_project(request):
    if request.method == 'GET':
        return render_internal(request,'myaccount/upload.html',{})
    if request.FILES == None or len(request.FILES.items())==0:
        return render_internal(request,'myaccount/upload.html',{})
    
    for key, file in request.FILES.items():
        unzipped = zipfile.ZipFile(file)
        for img_name in unzipped.namelist():
            if not utils.isValidImageName(img_name):
                return render_internal(request,'myaccount/upload.html',{})
    
    
    project_name = request.POST.get("name", "").strip()
    user = request.user
    project_profile = ProjectProfile(user=user, name=project_name)
    project_profile.save()
    
    directory = settings.BASE_DIR+"/medias/upload/%d/original/" %(project_profile.id)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for key, file in request.FILES.items():
        path = directory + file.name
        print path
        dest = open(path, 'w')
        if file.multiple_chunks:
            for c in file.chunks():
                dest.write(c)
        else:
            dest.write(file.read())
        dest.close()
    
    return render_internal(request, 'myaccount/upload_confirm.html', {})

   

def project_3dview(request, project_id):
    project = get_object_or_404(ProjectProfile, pk=project_id)
    return render_internal(request, 'ndmodel/project_3dview.html', {'project':project})

def project_detail(request, project_id):
    project = get_object_or_404(ProjectProfile, pk=project_id)
    owner_uf = UserProfile.objects.get(user=project.user)
    owner_other_projects = list((ProjectProfile.objects.filter(user = project.user.id, status = utils.ProjectStatus.success).exclude(id=project_id))[:4])   
    print "owner other projects:", owner_other_projects
    print "project owner:", owner_uf
    return render_internal(request, 'ndmodel/project_detail.html', 
                           {'project':project, 'owner_uf':owner_uf,
                            'owner_other_projects':owner_other_projects})    

def project_list(request):
    projects = list(ProjectProfile.objects.filter(status = utils.ProjectStatus.success))
    print "project size:", len(projects)
    return render_internal(request, 'ndmodel/project_list.html', {'projects':projects, 'projects_size':len(projects)})
    
def aboutus(request):
	return render_internal(request, 'index/aboutus.html', {})
    

"""
internal render function
"""    
def render_internal(request, url, dirs):
    new_dirs = dirs
    if request.user.id != None:
        uf = UserProfile.objects.get(user=request.user)
        new_dirs["uf"] = uf
    return render(request, url, new_dirs)


    
    

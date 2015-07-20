from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout,login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth.models import User
from core.models import UserProfile, ShopItem, Store
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



def index(request):
    return render(request, 'index/index.html',{})

def aboutus(request):
        return render(request, 'index/aboutus.html', {})

@csrf_exempt
def mobile_login(request):
    email = request.GET.get("email", "")
    password= request.GET.get("password", "")
    print "email=",email, "password", password
    user = authenticate(username=email,password = password)
    print user
    response_data = {}
    if user!=None:
        response_data['status'] = 'true'
    else:
        response_data['status'] = 'false'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def mobile_additem(request):
    userId = request.GET.get("userId", "")
    shopListName = request.GET.get("shopListName", "")
    storeName = request.GET.get("store", "")
    itemName = request.GET.get("itemName", "")
    print "userId=", userId, "shoplist=", shopListName, storeName, itemName
    user = User.objects.get(id=userId)
    print user
    
#     shopListList = ShopList.objects.filter(owner=user)
#     print shopListList
#     shopList = None
#     if shopListList!=None:
#         for sl in shopListList:
#             if sl.name == shopListName:
#                 shopList = sl
#     
#     if shopList == None:
#         shopList = ShopList(owner=user, name=shopListName)
#         shopList.save()
#     print "shopList=", shopList
    store = Store.objects.filter(name=storeName)[0]
    print store
    shopItem = ShopItem(name=itemName, store=store, shopList = shopListName, owner=user)
    shopItem.save()
    response_data = {"status":"true"}
    return HttpResponse(json.dumps(response_data), content_type="application/json")

# @csrf_exempt
# def mobile_getshoplist(request):
#     userId = request.GET.get("userId", "")
#     user = User.objects.get(id=userId)
#     print "user=",user
#     
#     shopListList = ShopList.objects.filter(owner=user)
#     response_data = list()
#     for sl in shopListList:
#         response_data.append({"title":sl.name})
#         
#     print "shoplist=", response_data
#     return HttpResponse(json.dumps(response_data), content_type="application/json")

# @csrf_exempt
# def mobile_deleteshoplist(request):
#     userId = request.GET.get("userId", "")
#     user = User.objects.get(id=userId)
#     shoplistName = request.GET.get("shoplistName", "")
#     
#     shoplistList = ShopList.objects.filter(name=shoplistName, owner=user)
#     for sl in shoplistList:
#         ShopList.delete(sl)
#     return mobile_getshoplist(request)

@csrf_exempt
def mobile_getshopitem(request):
    userId = request.GET.get("userId", "")
    #shoplistName = request.GET.get("shoplistName", "")
    user = User.objects.get(id=userId)
    print "user=",user
    #shoplistList = ShopList.objects.filter(owner=user)
    response_data = list()
    #if len(shoplistList)>0:
    #    shoplist = shoplistList[0]
    shopitems = ShopItem.objects.filter(owner=user)
    print "shopitems:", shopitems
    for shopitem in shopitems:
        response_data.append({"name":shopitem.name, "store":shopitem.store.name, "shoplist":shopitem.shopList})
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    
@csrf_exempt
def mobile_deleteshopitem(request):
    userId = request.GET.get("userId", "")
    #shoplistName = request.GET.get("shoplistName", "")
    shopItemName = request.GET.get("shopitemName", "")
    user = User.objects.get(id=userId)
    #shoplistList = ShopList.objects.filter(name=shoplistName, owner=user)
#     if len(shoplistList)>0:
#         shoplist = shoplistList[0]
    shopitems = ShopItem.objects.filter(name = shopItemName)
    for shopitem in shopitems:
        ShopItem.delete(shopitem)
    return mobile_getshopitem(request)
    

def login_view(request):
    error_messages = list()
    if request.method == 'GET':
        nexturl = request.GET.get('next', "/")
        return render(request,'index/login.html',
                      {"next":nexturl, "error_messages":error_messages})
    elif request.method == 'POST':
        email = request.POST.get("email","").strip()
        password = request.POST.get("password","").strip()
        nexturl = request.POST.get("next", "/").strip()
        user = authenticate(username=email,password=password)
        if not user == None:
            login(request,user)
            return redirect(nexturl)

        #redirect to login page
        error_messages.append("Email or password is wrong.")
        return render(request,'index/login.html',
                      {"next":nexturl,"error_messages":error_messages})



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


"""
Shop List
"""
# @login_required(login_url='/login')
# def shoplist_create(request):
#     error_messages = list()
#     if request.method == "GET":
#         return render(request, 'shoplist/shoplist_create.html',{'error_messages':error_messages})
#     name = request.POST.get("name", "")
#     shopList = ShopList(owner=request.user, name=name)
#     shopList.save()
#     return redirect('/shopitem/')
# 
# @login_required(login_url='/login')
# def shoplist_update(request, shoplist_id):
#     error_messages = list()
#     shopList = ShopList.objects.get(id=shoplist_id)
#     if request.method == "GET":
#         return render(request, 'shoplist/shoplist_update.html',{'error_messages':error_messages, "shoplist":shopList})
#     name = request.POST.get("name", "")
#     shopList.name = name
#     shopList.owner = request.user
#     shopList.save()
#     return redirect('/shoplist/%d' % shopList.id)
# 
# 
# @login_required(login_url='/login')
# def shopitem_create(request):
#     error_messages = list()
#     shopListList = ShopList.objects.all()
#     storeList = Store.objects.all()
#     if request.method == "GET":
#         return render(request, 'shoplist/shopitem_create.html',{'error_messages':error_messages, 
#                                                                 'store_list':storeList,
#                                                                 'shoplist_list':shopListList})
#     name = request.POST.get("name", "")
#     shopListId = request.POST.get("shopListId", "0")
#     shopList = ShopList.objects.get(id = shopListId)
#     storeId = request.POST.get("storeId", "0")
#     store = Store.objects.get(id=storeId)
#     
#     shopItem = ShopItem(name=name, store=store, shopList = shopList)
#     shopItem.save()
#     return redirect('/shopitem/' )
#     
# @login_required(login_url='/login')
# def shopitem_update(request, shopitem_id):
#     error_messages = list()
#     shopListList = ShopList.objects.all()
#     storeList = Store.objects.all()
#     shopItem = ShopItem.objects.get(id=shopitem_id)
#     if request.method == "GET":
#         return render(request, 'shoplist/shopitem_update.html',{'error_messages':error_messages, 
#                                                                 'store_list':storeList,
#                                                                 'shoplist_list':shopListList,
#                                                                 'shopitem':shopItem})
#     name = request.POST.get("name", "")
#     shopListId = request.POST.get("shopListId", "0")
#     shopList = ShopList.objects.get(id = shopListId)
#     storeId = request.POST.get("storeId", "0")
#     store = Store.objects.get(id=storeId)
#     
#     shopItem.name = name
#     shopItem.shopList = shopList
#     shopItem.store = store
#     shopItem.save()
#     return redirect('/shopitem/%d' % shopItem.id)
# 
# 
# @login_required(login_url='/login')
# def shoplist_getall(request):
#     error_messages = list()
#     shopListList = ShopList.objects.all()
#     return render(request, 'shoplist/shoplist_list.html', {'error_messages':error_messages, 
#                                                            'shoplist_list':shopListList,
#                                                            })
#         
    
    


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
import os, zipfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import utils, time, hashlib
#from matplotlib.font_manager import path
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.conf import POSTBACK_ENDPOINT, SANDBOX_POSTBACK_ENDPOINT
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    return project_list(request)

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
    profile = UserProfile.objects.get(user=request.user)
    return render_internal(request,'myaccount/myprofile.html',{})


@login_required(login_url='/login')
@transaction.atomic
def upload_project(request):
    if request.method == 'GET':
        return render_internal(request,'myaccount/upload.html',{})
    if request.FILES == None or len(request.FILES.items())==0:
        return render_internal(request,'myaccount/upload.html',{})
    
    project_name = request.POST.get("project_name", "").strip()
    project_file = request.FILES.get("project")
    project_image = request.FILES.get("project_image")
    is3dmodel = (request.POST.get("is3dmodel")=="on")
    
    print is3dmodel, project_name, project_file, project_image
    
    user = request.user
    unzipped = zipfile.ZipFile(project_file)
    if (not is3dmodel):        
        for img_name in unzipped.namelist():
            if not utils.isValidImageName(img_name):
                return render_internal(request,'myaccount/upload.html',{})
        status = utils.ProjectStatus.submit
        project_profile = ProjectProfile(user=user, name=project_name, status=status, profile_image=project_image.name)
        project_profile.save()
        
    else:
        for f in unzipped.namelist():
            if f.endswith("obj"):
                threemodel = f.split("/")[-1]
            elif f.endswith("mtl"):
                texture = f.split("/")[-1]
        status = utils.ProjectStatus.success
        project_profile = ProjectProfile(user=user, name=project_name, status=status, 
                                         profile_image=project_image.name, 
                                         threedmodel = threemodel,
                                         texture = texture)
        project_profile.save()

   
    
    original_pic_directory = settings.BASE_DIR+"/medias/upload/%d/original/" %(project_profile.id)
    if not os.path.exists(original_pic_directory):
        os.makedirs(original_pic_directory)
        
    original_model_directory = settings.BASE_DIR+"/medias/upload/%d/original_models/" %(project_profile.id)
    if not os.path.exists(original_model_directory):
        os.makedirs(original_model_directory)
    
    if is3dmodel:
        path = original_model_directory + project_file.name
        outpath = original_model_directory
    else:
        path = original_pic_directory + project_file.name
        outpath = original_pic_directory
    
    print path
    dest = open(path, 'w')
    if project_file.multiple_chunks:
        for c in project_file.chunks():
                dest.write(c)
    else:
        dest.write(project_file.read())
    dest.close()
    
    utils.extractZipfile(path, outpath)
    os.remove(path)
    
    profile_image_path = settings.BASE_DIR+"/medias/upload/%d/%s" %(project_profile.id, project_profile.profile_image);
    dest = open(profile_image_path, 'w')
    if project_image.multiple_chunks:
        for c in project_image.chunks():
                dest.write(c)
    else:
        dest.write(project_image.read())
    
    #return render_internal(request, 'myaccount/upload_confirm.html', {})
    return redirect("/projectdetail/%d" %(project_profile.id))

   

def project_3dview(request, project_id):
    project = get_object_or_404(ProjectProfile, pk=project_id)
    texture_img = request.GET.get("color", "")
    if texture_img == "null":
        texture_img = ""
    try:
        background_color = int(request.GET.get("background"))
    except:
        background_color = 200;
    
    print texture_img, background_color
    background_color_hex = '0x'+''.join(map(chr, (background_color, background_color, background_color))).encode('hex')
    if texture_img == "" and project.texture != "":
        loader = "OBJMTLLoader"
    else:
        loader = "OBJLoader"
    
    return render_internal(request, 'ndmodel/project_3dview.html', 
                           {'project':project, 'texture_url':texture_img, 
                            "loader":loader, "background_color":background_color_hex})

def project_detail(request, project_id):
    project = get_object_or_404(ProjectProfile, pk=project_id)
    owner_uf = UserProfile.objects.get(user=project.user)
    owner_other_projects = list((ProjectProfile.objects.filter(user = project.user.id, status = utils.ProjectStatus.success).exclude(id=project_id))[:4])   
    default_material = "Plastic"
    default_color = "White"
    default_color_url = "white_plastic.png"
    return render_internal(request, 'ndmodel/project_detail.html', 
                           {'project':project, 'owner_uf':owner_uf,
                            'owner_other_projects':owner_other_projects,
                            'default_material':default_material,
                            'default_color':default_color,
                            'default_color_url':default_color_url,
                            })    
@transaction.atomic
def getprice(request):
   priceunit = PriceUnit.objects.all()
   color = request.GET.get("color", "").strip()
   material = request.GET.get("material", "").strip()
   x = request.GET.get("x", "").strip()
   y = request.GET.get("y", "").strip()
   z = request.GET.get("z", "").strip()
   finish = request.GET.get("finish", "").strip()
   sizeunit = request.GET.get("sizeunit", "").strip()
   projectId = request.GET.get("projectid", "0")
   print color, material, x, y, z, sizeunit, projectId
   error_response = HttpResponse("{\"price_unit\":-1, \"total_price\":-1}")
   
   try:
       x = float(x)
       y = float(y)
       z = float(z)
       projectId = int(projectId)
       project = get_object_or_404(ProjectProfile, pk=projectId)
       if project.modelx == 0 and project.modely == 0 and project.modelz==0:
           project.modelx = round(x,2)
           project.modely = round(y,2)
           project.modelz = round(z,2) 
           project.save()
   except:
       return error_response 
   
   priceUnits = list(PriceUnit.objects.filter(unit=sizeunit, material=material))
   unit_price = 0
   
   priceUnitId = 0;
   for pu in priceUnits:
       print pu.color, pu.finish
       if len(color)==0 and len(finish)==0:
           continue
       elif len(color)>0 and len(finish)==0:
            if color == pu.color:
               unit_price = pu.price
               priceUnitId = pu.id
            else:
                continue
       elif len(color)==0 and len(finish)>0:
            if finish == pu.finish:
                unit_price = pu.price
                priceUnitId = pu.id
            else:
                continue   
       else:
           return error_response            
   price = round(unit_price * x * y * z, 2)
   response = "{\"price_unit\":%d, \"total_price\":%f}" %(priceUnitId, price)
   print response
   return HttpResponse(response)

@transaction.atomic
def update_shopcart_quantity(request, shopCartId, quantity):
    shopCartId = int(shopCartId)
    quantity = int(quantity)
    shopCartItem =  get_object_or_404(ShopCartItem, pk=shopCartId)
    if quantity<=0:
        print "delete: ",shopCartItem.id
        shopCartItem.delete()
    else:
        shopCartItem.quantity = quantity
        shopCartItem.save()
    return HttpResponse(1);
    


def project_list(request):
    projects = list(ProjectProfile.objects.filter(status = utils.ProjectStatus.success))
    paginator = Paginator(projects, 20) # Show 20 contacts per page
    
    page = request.GET.get('page')
    try:
        page = int(page)
    except Exception:
        page = 1
    
    projects = paginator.page(page)
    
    start_page = ((page-1) / 5) * 5 + 1
    end_page = ((page-1) / 5 +1) * 5
    if end_page > paginator.num_pages:
        end_page = paginator.num_pages
    
    if start_page>5:
        pre_page = start_page - 1
    else:
        pre_page = None
      
    if end_page<=5 and end_page<paginator.num_pages:
        next_page = end_page + 1
    else:
        next_page = None
    
    
    return render_internal(request, 'ndmodel/project_list.html', 
                           {'projects':projects, 
                            'projects_size':len(projects),
                            'start_page':start_page,
                            'end_page':end_page,
                            'page_range':range(start_page, end_page+1),
                            'pre_page':pre_page,
                            'next_page':next_page})
    
def aboutus(request):
	return render_internal(request, 'index/aboutus.html', {})
    
@login_required(login_url='/login')
@transaction.atomic
def shopcart(request):
    profile = UserProfile.objects.get(user=request.user)
    
    if request.method == "POST":
        priceUnitId = int(request.POST.get("priceunitid_hidden")) 
        projectId = int(request.POST.get("projectid_hidden"))
        sizex = float(request.POST.get("sizex_hidden"))
        sizey = float(request.POST.get("sizey_hidden"))
        sizez = float(request.POST.get("sizez_hidden"))
        priceUnit =  get_object_or_404(PriceUnit, pk=priceUnitId)
        project = get_object_or_404(ProjectProfile, pk=projectId)
        shopcartItems = list(ShopCartItem.objects.filter(user=request.user, priceUnit=priceUnit, 
                                                         project=project, sizex=sizex, sizey=sizey, sizez=sizez))
        if shopcartItems == None or len(shopcartItems) ==0 :
            shopcartItem = ShopCartItem(user=request.user, priceUnit=priceUnit, project=project, 
                                        sizex=sizex, sizey=sizey, sizez=sizez, quantity=1)
        else:
            shopcartItem = shopcartItems[0]
            shopcartItem.quantity = shopcartItem.quantity + 1
        shopcartItem.save()
        

    shopCartItems = ShopCartItem.objects.filter(user = request.user)
    return render_internal(request,'payment/shopcart.html',{"shopCartItems":shopCartItems})
    

# @transaction.atomic 
# def shopcart_checkout(request):
#     print request
#     profile = UserProfile.objects.get(user=request.user)
#     if request.method == "GET":
#         raise Http404
#     order = Order.objects.filter(user=request.user)
#     if order == None or len(order) == 0:
#         order = Order(user = request.user)
#         order.save()
#     else:
#         order = order[0]
#     
#     shopCartItems = ShopCartItem.objects.filter(user = request.user)
#     for item in shopCartItems:
#         item.order = order
#         item.save()
#     
#     shippingAddress = getShippingAddress(request.user)
#     return render_internal(request, 'payment/shipping.html', {"userprofile":profile,
#                                                               "shipping_address":shippingAddress})
        
    
    

@login_required(login_url='/login')
@transaction.atomic        
def shipping(request):
    profile = UserProfile.objects.get(user=request.user)
    shippingAddress = getShippingAddress(request.user)
    if request.method == "GET":
        return render_internal(request, 'payment/shipping.html', 
                               { "shipping_address":shippingAddress})
    else:        
        name = request.POST.get("shipusername")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        postcode = request.POST.get("postcode")
        addressline_1 = request.POST.get("addressline_1")
        addressline_2 = request.POST.get("addressline_2", "")
        phone = request.POST.get("phone", "")
        shippingAddress.user = request.user
        shippingAddress.country = country
        shippingAddress.city = city
        shippingAddress.state = state
        shippingAddress.postcode = postcode
        shippingAddress.addressline_1 = addressline_1
        shippingAddress.addressline_2 = addressline_2
        shippingAddress.phone = phone
        shippingAddress.shipUserName = name
        shippingAddress.save()
        return redirect("/shop/review")
    
    
@login_required(login_url='/login')
def shopreview(request):
    profile = UserProfile.objects.get(user=request.user)
    shippingAddress = getShippingAddress(request.user)
    shopCartItems = ShopCartItem.objects.filter(user = request.user)
    if shopCartItems == None or len(shopCartItems)==0:
        raise Http404
    shipping_cost = 6.5 #hard code
    subtotal_price = 0
    for item in shopCartItems:
        subtotal_price = subtotal_price + item.getTotalPrice
    total_price = subtotal_price + shipping_cost
    
    #invoice = str(int(round(time.time() * 1000)))
    invoice = getInvoice(request.user, shopCartItems)
    order = Order.objects.filter(invoice=invoice)
    if order == None or len(order) == 0:
        order = Order()
    else:
        order = order[0]
        
    order.user = request.user
    order.shippingAddress = shippingAddress
    order.gross = total_price
    order.invoice = invoice
    order.save()
    
    for item in shopCartItems:
        item.order = order
        item.save()
    
    notify_url = settings.SITE_NAME+ reverse('paypal-ipn')
    return_url = settings.SITE_NAME+"payment/return/"+"?invoice="+invoice
    cancel_url = settings.SITE_NAME+"payment/cancel/"
    action = SANDBOX_POSTBACK_ENDPOINT
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": total_price,
        "item_name": "test item",
        "invoice": invoice,
        "notify_url": notify_url,
        "return_url": return_url,
        "return": return_url,
        "cancel_return": cancel_url,
        "custom":"user=%d&order=%d" %(request.user.id, order.id),

    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)        
    return render_internal(request, 'payment/order_review.html', 
                           {"shipping_address":shippingAddress,
                            "shopCartItems":shopCartItems, 
                            "shipping_cost":shipping_cost,
                            "total_price":total_price,
                            "subtotal_price":subtotal_price,
                            "form":form,
                            "action":action})    


@login_required(login_url='/login')
def payment_confirm(request):
    return render_internal(request, 'payment/payment_confirm.html',{}) 

def payment_return(request):
    return render_internal(request, 'payment/payment_confirm.html',{}) 

def payment_cancel(request):
    return render_internal(request, 'payment/payment_confirm.html',{})

"""
internal render function
"""    
def render_internal(request, url, dirs):
    new_dirs = dirs
    if request.user.id != None:
        uf = UserProfile.objects.get(user=request.user)
        shoppingCartItems = ShopCartItem.objects.filter(user=request.user)
        shoppingCartItemCount = 0
        if shoppingCartItems != None:
            shoppingCartItemCount = len(shoppingCartItems)
        new_dirs["uf"] = uf
        new_dirs["shoppingCartItemCount"] = shoppingCartItemCount
    return render(request, url, new_dirs)

def getShippingAddress(user):
    shippingAddress = ShippingAddress.objects.filter(user=user)
    if shippingAddress == None or len(shippingAddress)==0:
        shippingAddress = ShippingAddress()
    else:
        shippingAddress = shippingAddress[0]  
    return shippingAddress  

def getInvoice(user, shoppingCarts=list()):    
    s = "user="+str(user.id)
    s += "&shoppingcarts="
    for item in shoppingCarts:
        s += str(item.id) + ","

    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()
    


    
    

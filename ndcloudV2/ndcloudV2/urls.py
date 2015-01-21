from django.conf.urls import patterns, include, url
from django.contrib import admin
from core import views as core_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ndcloudV2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',core_views.index,name="index"),
    url(r'^login$', core_views.login_view, name='login'),
    url(r'^logout$', core_views.logout_view, name='logout'),
    url(r'^signup$', core_views.register, name='signup'),
    url(r'^myprofile$', core_views.myprofile, name='myprofile'),
    url(r'^uploadproject$', core_views.upload_project, name='upload_project'),
    url(r'^uploadpicture/', core_views.upload_picture, name='upload_picture'),
    url(r'^projectdetail/(?P<project_id>\d+)$',core_views.project_detail, name='project_detail' ),
    url(r'^project3dview/(?P<project_id>\d+)$',core_views.project_3dview, name='project_3dview'),
    url(r'^project/update/(?P<project_id>\d+)$',core_views.project_update, name='project_update'),
    url(r'^project/delete/(?P<project_id>\d+)$',core_views.project_delete, name='project_delete'),
    url(r'^projectlist/$',core_views.project_list, name='project_list' ),
    url(r'^aboutus/$',core_views.aboutus, name='aboutus' ),
    url(r'^getprice/', core_views.getprice, name='getprice'),
    url(r'^userimage/update/$', core_views.userimage_update, name='userimage_update'),
    url(r'^updateshopcartquantity/(?P<shopCartId>\d+)/(?P<quantity>\d+)$', core_views.update_shopcart_quantity, name='update_shopcart_quantity'),
    url(r'^shop/cart/$', core_views.shopcart, name='shopcart'),
    url(r'^shop/shipping/$', core_views.shipping, name='shipping'),
    url(r'^shop/review/$', core_views.shopreview, name='shop_review'),
    #url(r'^shop/paymentconfirm/$', core_views.payment_confirm, name='payment_confirm'),
    
    url(r'^payment/return/', core_views.payment_return, name='payment_return'),
    url(r'^payment/cancel/', core_views.payment_cancel, name='payment_cancel'),
    url(r'^payment/paypal/', include('paypal.standard.ipn.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

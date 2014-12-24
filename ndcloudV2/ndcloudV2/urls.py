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
    #url(r'^uploadconfirm$', core_views.upload_confirm, name='upload_confirm'),
    url(r'^projectdetail/(?P<project_id>\d+)$',core_views.project_detail, name='project_detail' ),
    url(r'^project3dview/(?P<project_id>\d+)$',core_views.project_3dview, name='project_3dview'),
    url(r'^projectlist/$',core_views.project_list, name='project_list' ),
    url(r'^aboutus/$',core_views.aboutus, name='aboutus' ),
    url(r'^getprice/', core_views.getprice, name='getprice'),
    url(r'^updateshopcartquantity/(?P<shopCartId>\d+)/(?P<quantity>\d+)$', core_views.update_shopcart_quantity, name='update_shopcart_quantity'),
    url(r'^shop/cart/$', core_views.shopcart, name='shopcart'),
    url(r'^shop/shipping/$', core_views.shipping, name='shipping'),
    url(r'^shop/review/$', core_views.shopreview, name='shop_review'),
    url(r'^shop/paymentconfirm/$', core_views.payment_confirm, name='payment_confirm'),
    #url(r'^shop/checkout/$', core_views.shopcart_checkout, name='shopcart_checkout'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

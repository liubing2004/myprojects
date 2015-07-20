from django.conf.urls import patterns, include, url
from django.contrib import admin
from core import views as core_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$',core_views.index,name="index"),
    url(r'^login$', core_views.login_view, name='login'),
    url(r'^logout$', core_views.logout_view, name='logout'),
    url(r'^signup$', core_views.register, name='signup'),
    url(r'^aboutus/$',core_views.aboutus, name='aboutus' ),
#     url(r'^shoplist/$',core_views.shoplist_create, name='shoplist_create' ),
#     url(r'^shoplist/getall$',core_views.shoplist_getall, name='shoplist_list' ),
#     url(r'^shoplist/(?P<shoplist_id>\d+)$',core_views.shoplist_update, name='shoplist_update' ),
#     url(r'^shopitem/$',core_views.shopitem_create, name='shopitem_create' ),
#     url(r'^shopitem/(?P<shopitem_id>\d+)$',core_views.shopitem_update, name='shopitem_update' ),
    url(r'^mobile/login$', core_views.mobile_login, name='mobile_login'),
    url(r'^mobile/additem$', core_views.mobile_additem, name='mobile_additem'),
    #url(r'^mobile/shoplist$', core_views.mobile_getshoplist, name='mobile_shoplist'),
    url(r'^mobile/shopitem$', core_views.mobile_getshopitem, name='mobile_shopitem'),
    #url(r'^mobile/shoplist/delete$', core_views.mobile_deleteshoplist, name='mobile_shoplist_delete'),
    url(r'^mobile/shopitem/delete$', core_views.mobile_deleteshopitem, name='mobile_shopitem_delete'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
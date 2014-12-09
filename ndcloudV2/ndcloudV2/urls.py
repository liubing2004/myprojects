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
    url(r'^(?P<project_id>\d+)/projectdetail/$',core_views.project_detail, name='project_detail' ),
    url(r'^projectlist/$',core_views.project_list, name='project_list' ),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

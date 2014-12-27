from django.conf.urls import patterns, include, url

from polls import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    
    # ex: /polls/5/
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
    url(r'^payment_return/', views.payment_return, name='payment_return'),
    url(r'^payment_cancel/$', views.payment_cancel, name='payment_cancel'),
    url(r'^payment/$', views.view_that_asks_for_money, name='viewpayment'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
#     url(r'^paypal/$', views.paypal, name="paypal"),
)

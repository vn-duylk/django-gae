from django.conf.urls.defaults import *
from guestbook.views import IndexView, SignView
from django.conf.urls import url

urlpatterns =[
    url(r'^$', IndexView.as_view(), name='indexview'),
    url(r'^sign/$', SignView.as_view(), name='signview'),
]
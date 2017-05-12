# -*- coding: utf-8 -*-

from django.conf.urls import url

from guestbook.views.main_page import IndexView
from guestbook.views.sign_page import SignView
from guestbook.views.update_page import UpdateView
from guestbook.views.delete_page import DeleteView
from guestbook.api.views import GreetingService, GreetingDetail


urlpatterns = [
	url(r'^$', IndexView.as_view(), name='indexview'),
	url(r'^sign/$', SignView.as_view(), name='signview'),
	url(r'^update/$', UpdateView.as_view(), name='updateview'),
	url(r'^delete/(?P<guestbook_id>\d+)/(?P<guestbook_name>\w+)$', DeleteView.as_view(),
	    name='deleteview'),
	url(r'^api/v1/(?P<guestbook_name>\w+)/greetings/$', GreetingService.as_view(),
	    name='greetingservice'),
	url(r'^api/v1/(?P<guestbook_name>\w+)/(?P<guestbook_id>\d+)$', GreetingDetail.as_view(),
	    name='greetingservice'),
]

# -*- coding: utf-8 -*-
from guestbook.views.main_page import IndexView
from guestbook.views.sign_page import SignView
from guestbook.views.update_page import UpdateView
from guestbook.views.delete_page import DeleteView
from django.conf.urls import url


urlpatterns = [
	url(r'^$', IndexView.as_view(), name='indexview'),
	url(r'^sign/$', SignView.as_view(), name='signview'),
	url(r'^update/$', UpdateView.as_view(), name='updateview'),
	url(r'^delete/(?P<guestbook_id>\d+)/(?P<guestbook_name>\w+)$', DeleteView.as_view(),
	    name='deleteview'),
]

from guestbook.views.main_page import IndexView
from guestbook.views.sign_page import SignView
from django.conf.urls import url


urlpatterns =[
    url(r'^$', IndexView.as_view(), name='indexview'),
    url(r'^sign/$', SignView.as_view(), name='signview'),
]

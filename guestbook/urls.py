from django.conf.urls.defaults import *
#from guestbook.views import main_page, sign_post
from guestbook.views import IndexView, SignView
from django.views.generic import TemplateView
from django.conf.urls import url
# urlpatterns = patterns('',
#     # (r'^sign/$', sign_post),
#     # (r'^$', main_page),
#
#     (r'^sign/$', SignView.as_view(), name = 'sign_view'),
#     (r'^$', IndexView.as_view(), name = "index_view"),
# )

urlpatterns =[
    # url(r'^sign/$', TemplateView.as_view(template_name="sign_page.html")),
    # url(r'^$', TemplateView.as_view(template_name="index_page.html")),
    url(r'^$', IndexView.as_view(), name='indexview'),
    url(r'^sign/$', SignView.as_view(), name='signview'),
    #url(r'^sign/$', sign_post),
    #url(r'^$', main_page),
]
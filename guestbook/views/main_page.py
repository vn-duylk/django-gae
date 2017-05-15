# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from google.appengine.api import users
from google.appengine.ext import ndb

from guestbook.models import Greeting, DEFAULT_GUESTBOOK_NAME


class IndexView(TemplateView):

	template_name = "guestbook/index_page.html"
	model = Greeting

	def get_context_data(self, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		try:
			cursor = ndb.Cursor(urlsafe=self.request.GET.get('cursor', ''))
			results = int(self.request.GET.get('results', 4))
			greetings, cursor, more = Greeting.get_greetings(guestbook_name, cursor, results)
			if users.get_current_user():
				url = users.create_logout_url(self.request.get_full_path())
				url_linktext = 'Logout'
			else:
				url = users.create_login_url(self.request.get_full_path())
				url_linktext = 'Login'

			context = super(IndexView, self).get_context_data(**kwargs)
			context['greetings'] = greetings
			context['cursor'] = cursor
			context['more'] = more
			context['guestbook_name'] = guestbook_name
			context['url_linktext'] = url_linktext
			context['url'] = url
		except BaseException as e:
			print e.message

		return context

from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseForbidden

from google.appengine.api import users
from google.appengine.ext import ndb

from guestbook.models import Greeting, guestbook_key
from guestbook.views import using_task_queue


class DeleteView(TemplateView):
	template_name = "guestbook/index_page.html"

	def post(self, request, *args, **kwargs):
		guestbook_name = kwargs['guestbook_name']
		guestbook_id = int(kwargs['guestbook_id'])
		self.delete_guestbook(guestbook_name, guestbook_id)
		url = reverse_lazy('indexview')
		return redirect('%s?guestbook_name=%s' % (url, guestbook_name))

	def delete_guestbook(self,  guestbook_name, guestbook_id):
		greeting = self.get_guestbook_by_id(guestbook_name, guestbook_id)
		user = users.get_current_user()

		@ndb.transactional
		def delete_greeting():
			greeting.key.delete()

		if greeting:
			if users.is_current_user_admin() or user and greeting.author == user:
				delete_greeting()
				using_task_queue.add_task_queue(greeting.author, greeting.content)
			else:
				raise HttpResponseForbidden("Method not allowed")

	def get_guestbook_by_id(self, guestbook_name, guestbook_id):
		entity = Greeting.get_by_id(guestbook_id, guestbook_key(guestbook_name))
		return entity

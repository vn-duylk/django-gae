# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from google.appengine.ext import ndb
from google.appengine.api import users
from guestbook.forms import UpdateForm
from guestbook.models import Greeting, guestbook_key
from guestbook.views import using_task_queue


class UpdateView(FormView):
	template_name = "guestbook/update_page.html"
	form_class = UpdateForm

	def get_initial(self):
		initial = super(UpdateView, self).get_initial()
		initial['name'] = self.get_guestbook_name()
		initial['guestbook_id'] = self.get_guestbook_id()
		greeting = self.get_guestbook_by_id()
		if greeting:
			initial['message'] = greeting.content
		return initial

	def get_context_data(self, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = super(UpdateView, self).get_context_data(**kwargs)
		context['guestbook_name'] = self.get_guestbook_name()
		context['guestbook_id'] = self.get_guestbook_id()
		context['form'] = form
		return context

	def get_success_url(self):
		url = reverse_lazy('indexview')
		return '%s?guestbook_name=%s' % (url, self.get_guestbook_name())

	def get_guestbook_name(self):
		guestbook_name = self.request.GET.get('guestbook_name')
		return guestbook_name

	def get_guestbook_id(self):
		guestbook_id = self.request.GET.get('guestbook_id','')
		return int(guestbook_id)

	def get_guestbook_by_id(self):
		entity = Greeting.get_by_id(self.get_guestbook_id(), guestbook_key(
			self.get_guestbook_name()))
		return entity

	def form_valid(self, form, **kwargs):
		name = form.cleaned_data['name']
		message = form.cleaned_data['message']
		greeting = self.get_guestbook_by_id()
		if greeting:
			greeting.content = message
		if users.get_current_user():
			greeting.updated_by = users.get_current_user()

		@ndb.transactional(retries=4)
		def put_greeting():
			greeting.put()

		user = users.get_current_user()
		if users.is_current_user_admin():
			put_greeting()
			using_task_queue.add_task_queue(greeting.author, greeting.content)
		elif user == greeting.author:
			put_greeting()
			using_task_queue.add_task_queue(greeting.author, greeting.content)
		return super(UpdateView, self).form_valid(form, **kwargs)

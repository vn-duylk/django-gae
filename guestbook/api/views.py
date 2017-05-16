# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, FormView
from django.http import Http404

from google.appengine.ext import ndb
from google.appengine.api import datastore_errors, users

from guestbook.models import Greeting
from guestbook.forms import GreetingForm
from guestbook.api.JsonResponse import JsonResponse
import json


class GreetingService(JsonResponse, TemplateView):

	def get_context_data(self, **kwargs):
		context = {}
		guestbook_name = kwargs['guestbook_name']
		cursor = self.request.GET.get('cursor', '')
		try:
			cur = ndb.Cursor(urlsafe=cursor)
		except datastore_errors.BadQueryError:
			raise Http404("Not Found")
		limit = int(self.request.GET.get('limit', 4))
		greetings, cursor, results = Greeting.list(guestbook_name, cur, limit)
		results = []
		context['guestbook_name'] = guestbook_name
		for greeting in greetings:
			results.append(greeting.to_resource_dict(guestbook_name))
		context['greetings'] = results
		context['next_cursor'] = cursor
		context['total_items'] = len(results)
		return context


class GreetingDetail(JsonResponse, FormView):
	form_class = GreetingForm

	def get(self, request, *args, **kwargs):
		try:
			guestbook_name = kwargs['guestbook_name']
			guestbook_id = kwargs['guestbook_id']
			entity = Greeting.get_guestbook_by_id(int(guestbook_id), guestbook_name)
			context = entity.to_resource_dict(guestbook_name)
		except BaseException:
			return self.render_to_response({'msg': 'error'}, status=404)
		return self.render_to_response(context)

	def get_form(self, form_class):
		return self.form_class(self.kwargs)

	def form_invalid(self, form):
		return self.render_to_response({'msg': 'Error'}, status=403)

	def form_valid(self, form, **kwargs):
		message = form.cleaned_data['message']
		guestbook_id = int(form.cleaned_data['guestbook_id'])
		guestbook_name = form.cleaned_data['guestbook_name']
		greeting = Greeting.get_guestbook_by_id(guestbook_id, guestbook_name)

		@ndb.transactional(retries=4)
		def put_greeting():
			greeting.content = message
			greeting.put()

		if greeting:
			user = users.get_current_user()
			if user:
				if users.is_current_user_admin() or user == greeting.author:
					greeting.updated_by = user
					put_greeting()
				return self.render_to_response({'msg': 'Success'}, status=200)
			return self.render_to_response({'msg': 'Required Login'}, status=401)
		return self.render_to_response({'msg': 'Not Found'}, status=404)

	def put(self, *args, **kwargs):
		content = self.request.body
		body = json.loads(content)
		kwargs.update(body)
		self.kwargs = kwargs
		return super(GreetingDetail, self).put(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		try:
			guestbook_name = kwargs['guestbook_name']
			guestbook_id = int(kwargs['guestbook_id'])
			greeting = Greeting.get_guestbook_by_id(guestbook_id, guestbook_name)
		except BaseException:
			return self.render_to_response({'msg': 'Error'}, status=400)

		@ndb.transactional
		def delete_greeting():
			greeting.key.delete()

		if greeting:
			user = users.get_current_user()
			if users.is_current_user_admin() or user and greeting.author == user:
				delete_greeting()
				return self.render_to_response({'msg': 'Success'}, status=200)
			return self.render_to_response({'msg': 'Required Login'}, status=401)
		return self.render_to_response({'msg': 'Not Found'}, status=404)

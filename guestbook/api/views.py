# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, FormView
from django.http import Http404

from google.appengine.ext import ndb
from google.appengine.api import datastore_errors

from guestbook.models import Greeting
from guestbook.forms import GreetingForm
from guestbook.api.JsonResponse import JsonResponse


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

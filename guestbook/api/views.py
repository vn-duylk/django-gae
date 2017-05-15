# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, FormView
from django.http import Http404

from google.appengine.ext import ndb

from guestbook.models import Greeting
from guestbook.forms import GreetingForm
from guestbook.api.JsonResponse import JsonResponse


class GreetingService(JsonResponse, TemplateView):

	def get_context_data(self, **kwargs):
		context = {}
		guestbook_name = kwargs['guestbook_name']
		try:
			cursor = self.request.GET.get('cursor', '')
			cur = ndb.Cursor(urlsafe=cursor)
			num_result = int(self.request.GET.get('num_result', 4))
			greetings, cursor, results = Greeting.get_greetings(guestbook_name, cur, num_result)
			results = []
			context['guestbook_name'] = guestbook_name
			for greeting in greetings:
				results.append(greeting.to_resource_dict(guestbook_name))
			context['greetings'] = results
			context['next_cursor'] = cursor
			context['total_items'] = len(results)
		except BaseException:
			raise Http404("Not Found")
		return context


class GreetingDetail(JsonResponse, FormView):
	form_class = GreetingForm

	def get(self, request, *args, **kwargs):
		guestbook_name = kwargs['guestbook_name']
		guestbook_id = kwargs['guestbook_id']
		entity = Greeting.get_guestbook_by_id(int(guestbook_id), guestbook_name)
		context = entity.to_resource_dict(guestbook_name)
		return self.render_to_response(context)

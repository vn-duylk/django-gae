# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, FormView

from guestbook.models import Greeting
from guestbook.forms import GreetingForm
from guestbook.api.JsonResponse import JsonResponse


class GreetingService(JsonResponse, TemplateView):

	def get_context_data(self, **kwargs):
		guestbook_name = kwargs['guestbook_name']
		greetings = Greeting.get_greetings(guestbook_name)
		context = {}
		results = []
		context['guestbook_name'] = guestbook_name
		for greeting in greetings:
			results.append(greeting.to_resource_dict(guestbook_name))

		context['greetings'] = results
		context['total_items'] = len(results)
		return context


class GreetingDetail(JsonResponse, FormView):
	form_class = GreetingForm

	def get(self, request, *args, **kwargs):
		guestbook_name = kwargs['guestbook_name']
		guestbook_id = kwargs['guestbook_id']
		entity = Greeting.get_guestbook_by_id(int(guestbook_id), guestbook_name)
		context = entity.to_resource_dict(guestbook_name)
		return self.render_to_response(context)

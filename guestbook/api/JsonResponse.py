from django.http import HttpResponse
import json
import logging


class JsonResponse(object):
	response_class = HttpResponse

	def render_to_json_response(self, context, **response_kwargs):
		logging.info(context)
		return self.response_class(self.get_data(context), **response_kwargs)

	def get_data(self, context):
		return json.dumps(context)

	def render_to_response(self, context, **response_kwargs):
		return self.render_to_json_response(context, **response_kwargs)

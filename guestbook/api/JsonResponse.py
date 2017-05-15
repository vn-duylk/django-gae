from django.http import HttpResponse
import json


class JsonResponse(object):
	response_class = HttpResponse

	def render_to_json_response(self, context, **response_kwargs):
		return self.response_class(json.dumps(context), **response_kwargs)

	def render_to_response(self, context, **response_kwargs):
		return self.render_to_json_response(context, **response_kwargs)

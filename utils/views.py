import json

import django.http
from django.views.generic import View


class BaseHttpResponse(django.http.HttpResponse):
	content_type = 'text/html'

	def __init__(self, content = '', mimetype = None, status = None, content_type = None):

		if content_type is None:
			content_type = self.content_type

		super(BaseHttpResponse, self).__init__(content = content, mimetype = mimetype, status = status, content_type = content_type)


class BaseHttpResponseRedirect(django.http.HttpResponseRedirect, BaseHttpResponse):
	content_type = 'text/plain'


class BaseHttpResponsePermanentRedirect(django.http.HttpResponsePermanentRedirect, BaseHttpResponse):
	content_type = 'text/plain'


class BaseView(View):

	HttpResponse = BaseHttpResponse
	HttpResponseRedirect = BaseHttpResponseRedirect
	HttpResponsePermanentRedirect = BaseHttpResponsePermanentRedirect

	def options(self, request, *args, **kwargs):
		allowed_methods = [m for m in self.http_method_names if hasattr(self, m)]

		response = self.HttpResponse()

		del response['Content-Type']

		response['Allow'] = ', '.join(m.upper() for m in allowed_methods)

		return response


def _json_handler(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		raise TypeError("Object {0} is not JSON serializable.".format(repr(obj)))


class JSONHttpResponse(BaseHttpResponse):

	content_type = 'application/json'

	def __init__(self, content = {}, mimetype = None, status = None, content_type = None):

		if isinstance(content, dict):
			content = json.dumps(content, default = _json_handler)

		super(JSONHttpResponse, self).__init__(content, mimetype, status, content_type)


class JSONView(BaseView):
	HttpResponse = JSONHttpResponse
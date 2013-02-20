import json
import traceback
import sys

from django.conf import settings

from utils.memoize import memoize_method
from utils.views import JSONHttpResponse, JSONView


class OkAPIResponse(JSONHttpResponse):
	status_code = 200

	def __init__(self, content = None, mimetype = None, status = None, content_type = None):

		processed_content = {
			'status': 'ok',
		}

		if content is not None:
			processed_content['content'] = content

		super(OkAPIResponse, self).__init__(processed_content, mimetype, status, content_type)


class ErrorAPIResponse(JSONHttpResponse):
	status_code = 400

	def __init__(self, content = None, mimetype = None, status = None, content_type = None):

		if content is None:
			raise ValueError("Error value must be provided.")
		else:
			error = None
			message = None
			extra_content = None
			if isinstance(content, basestring):
				error = content
				message = None
			elif isinstance(content, tuple) and len(content) in {2, 3}:
				error, message = content[:2]
				try:
					extra_content = content[2]
				except IndexError:
					pass

			if (
				not isinstance(error, basestring) or
				not isinstance(message, (type(None), basestring)) or
				not isinstance(extra_content, (type(None), dict))
			):
				# error must be a string, message must be a string or None,
				# and extra_content must be either None or a dict
				raise ValueError("Error value {0!r} is not valid.".format(content))

			content = {
				'status': 'error',
				'content': {
				'error': error,
			}
			}

			if message is not None:
				content['content']['message'] = message

			if extra_content is not None:
				content['content'].update(extra_content)

		super(ErrorAPIResponse, self).__init__(content, mimetype, status, content_type)



class APIError(Exception):
	"""An exception that will be caught and returned as standard API error response instead of a 500 Internal Server Error."""
	def __init__(self, error, message, status = None):
		self.API_error_name = error
		self.API_error_message = message
		self.API_error_status = status
		super(APIError, self).__init__('{0}: {1}'.format(error, message))


class APIView(JSONView):
	OkAPIResponse = OkAPIResponse
	ErrorAPIResponse = ErrorAPIResponse

	def dispatch(self, request, *args, **kwargs):
		# For any code to use before the super() is called.
		self.request = request
		self.args = args
		self.kwargs = kwargs

		try:
			return super(APIView, self).dispatch(request, *args, **kwargs)
		except APIError as e:
			return self.ErrorAPIResponse((e.API_error_name, e.API_error_message), status = e.API_error_status)

	@property
	@memoize_method
	def request_data(self):
		# Handles values like 'application/json' and 'application/json; charset=utf-8'
		content_type, _, _ = self.request.META.get('CONTENT_TYPE', '').lower().partition(';')

		if content_type == 'application/json':
			try:
				return json.loads(self.request.body)
			except ValueError:
				raise APIError('invalid_JSON_syntax', "The JSON received could not be parsed.")
		else:
			raise APIError('invalid_content_type', "Request content type must be application/json.", status = 415)


class NotFoundView(APIView):
	def dispatch(self, request, *args, **kwargs):
		return self.ErrorAPIResponse(
			('not_found', "The requested resource does not exist."),
			status = 404
		)


class InternalServerErrorView(APIView):
	def dispatch(self, request, *args, **kwargs):
		content = ['server_error', "An unexpected error has occurred."]
		if settings.DEBUG:
			content.append({'traceback': traceback.format_exception(*sys.exc_info())})
		return self.ErrorAPIResponse(tuple(content), status = 500)
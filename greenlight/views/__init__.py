from three import Three
from hashlib import md5

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import Http404

from .base import APIView


QC_three = Three(
	endpoint = "http://dev-api.ville.quebec.qc.ca/open311/v2/",
	format = "json",
	jurisdiction = "ville.quebec.qc.ca",
)


class ServicesView(APIView):
	def get(self, request):
		cache_key = 'services'
		services = cache.get(cache_key)
		if services is None:
			services = QC_three.services()
			cache.set(cache_key, services, 3600) # Cache for one hour.
		return self.OkAPIResponse(services)


class ServiceView(APIView):

	def get(self, request, id):
		cache_key = 'service_{}'.format(id)
		service = cache.get(cache_key)
		if service is None:
			service = QC_three.services(id)
			cache.set(cache_key, service, 3600) # Cache for one hour.
		return self.OkAPIResponse(service)


class RequestsView(APIView):
	def get(self, request):
		return self.OkAPIResponse(QC_three.requests(**request.GET))
	
	def post(self, request):
		
		open311_response = QC_three.post(**request.POST)[0]
		
		if open311_response.get('code') == 'BadRequest':
			return self.ErrorAPIResponse((open311_response['code'], open311_response['description']))
		
		if open311_response.get('service_request_id') is not None:
			location = reverse('request', args = (open311_response['service_request_id'],))
		elif open311_response.get('token') is not None:
			location = reverse('token', args = (open311_response['token'],))
		else:
			location = None
		
		open311_response.update(location = location)
		
		response = self.OkAPIResponse(open311_response, status = 201)
		
		if location is not None:
			response['Location'] = location
		
		return response


class RequestView(APIView):
	
	def get(self, request, id):
		requests = QC_three.request(id)
		if requests:
			return self.OkAPIResponse(requests[0])
		else:
			raise Http404


class TokenView(APIView):
	def get(self, request, id):
		return self.OkAPIResponse(QC_three.token(id))

class StatsView(APIView):
	
	def get(self, request, type):
		handler = getattr(self, 'compute_' + type, None)
		
		if handler is None:
			raise Http404
		
		# Include a unique but constant hash of all querystring arguments
		# to make sure we're getting the right cached data.
		cache_key = 'stats_{}_{}'.format(
			type,
			md5(','.join(
				k + '=' + v for k, v in
				sorted(request.GET.items())
			)).hexdigest()
		)
		
		result = cache.get(cache_key)
		if result is None:
			result = handler()
			cache.set(cache_key, result, 86400)
		
		return self.OkAPIResponse(result)
	
	def compute_states(self):
		requests = QC_three.requests(**self.request.GET)
		statuses = [r['status'] for r in QC_three.requests()]
		closed_count = statuses.count('closed')
		open_count = len(statuses) - closed_count
		return {
			'total': len(requests),
			'closed_count': closed_count,
			'open_count': open_count,
		}
	
	def compute_count(self):
		return len(QC_three.requests(**self.request.GET))
		
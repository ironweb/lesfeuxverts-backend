from three import Three

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
		return self.OkAPIResponse(QC_three.services())


class ServiceView(APIView):

	def get(self, request, id):
		return self.OkAPIResponse(QC_three.services(id))


class RequestsView(APIView):
	def get(self, request):
		return self.OkAPIResponse(QC_three.requests())


	def post(self, request):
		
		open311_response = QC_three.post(**request.POST)[0]
		
		if open311_response.get('code') == 'BadRequest':
			return self.ErrorAPIResponse((open311_response['code'], open311_response['description']))
		
		if 'service_request_id' in open311_response:
			location = reverse('request', args = (open311_response['service_request_id'],))
		elif 'token' in open311_response:
			location = reverse('token', args = (open311_response['service_request_id'],))
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
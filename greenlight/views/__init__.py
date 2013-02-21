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
		
		request_id = open311_response['service_request_id']
		
		location = reverse('request', args = (request_id,))
		
		response = self.OkAPIResponse({
			'id': request_id,
			'location': location
		})
		response['Location'] = location
		return response


class RequestView(APIView):
	
	def get(self, request, id):
		requests = QC_three.request(id)
		if requests:
			return self.OkAPIResponse(requests[0])
		else:
			raise Http404
		
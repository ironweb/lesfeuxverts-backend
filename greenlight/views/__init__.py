from three import Three
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

class RequestsView(APIView):
	def get(self, request):
		return self.OkAPIResponse(QC_three.requests())
	
class RequestView(APIView):
	
	def get(self, request, id):
		requests = QC_three.request(id)
		if requests:
			return self.OkAPIResponse(requests[0])
		else:
			raise Http404
		
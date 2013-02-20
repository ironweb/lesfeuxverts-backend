from .base import APIView
from django.http import Http404

from three import Three

class QCThree(Three):
	def __init__(self):
		self.endpoint = "http://dev-api.ville.quebec.qc.ca/open311/v2/"
		self.format = "json"
		self.jurisdiction = "ville.quebec.qc.ca"

QC_three = QCThree()

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
		
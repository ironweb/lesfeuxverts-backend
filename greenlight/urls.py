from django.conf import settings
from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
	url(r'^services/$', views.ServicesView.as_view(), name='services'),
	url(r'^services/([\w-]+)$', views.ServiceView.as_view(), name='service'),
	url(r'^requests/$', views.RequestsView.as_view(), name='requests'),
	url(r'^requests/([\d\s]+)$', views.RequestView.as_view(), name='request'),
	url(r'^token/([\w-]+)$', views.TokenView.as_view(), name='token'),
)

handler404 = views.base.NotFoundView.as_view()
handler500 = views.base.InternalServerErrorView.as_view()

if settings.DEBUG:
	# Monkey patch these handlers, it's the only way we can use our own when DEBUG = True
	# (The default debug handlers aren't very nice from the http-console.)

	from django.views import debug

	debug.technical_404_response = handler404
	debug.technical_500_response = handler500

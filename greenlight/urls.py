from django.conf import settings
from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'greenlight.views.home', name='home'),
    # url(r'^greenlight/', include('greenlight.foo.urls')),
)

handler404 = views.NotFoundView.as_view()
handler500 = views.InternalServerErrorView.as_view()

if settings.DEBUG:
	# Monkey patch these handlers, it's the only way we can use our own when DEBUG = True
	# (The default debug handlers aren't very nice from the http-console.)

	from django.views import debug

	debug.technical_404_response = handler404
	debug.technical_500_response = handler500
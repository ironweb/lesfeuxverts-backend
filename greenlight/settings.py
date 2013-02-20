# Django settings for greenlight project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Montreal'

USE_I18N = False

SECRET_KEY = '9&amp;@r*3hth4m=ml5t5tme0*(9^x@2xqo-ua^s+wg_ws(-^4-7@v'

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'greenlight.urls'

WSGI_APPLICATION = 'greenlight.wsgi.application'

INSTALLED_APPS = (
	'django_extensions'
)

CORS_ORIGIN_WHITELIST = {
	'greenlight.s3-website-us-east-1.amazonaws.com',
}

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}

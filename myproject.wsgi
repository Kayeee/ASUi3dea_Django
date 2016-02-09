import os
import sys

sys.path.append('/Users/kevin/Documents/i3dea/Django/myproject')

from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
application = WSGIHandler()

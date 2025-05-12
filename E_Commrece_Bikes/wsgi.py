import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'E_Commrece_Bikes.settings')

application = get_wsgi_application()

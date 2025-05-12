
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'E_Commrece_Bikes.settings')

application = get_asgi_application()

"""
WSGI config for eventex project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from dj_static import Cling
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventex.settings")

# o Cling é uma aplicação wsgi, que vai processar as requisições web antes do
# get_wsgi_application, que é a aplicação wsgi do django
# isso para poder servir os arquivos estáticos

application = Cling(get_wsgi_application())
#application = get_wsgi_application()  ---> se for buscar de um servidor http local, funciona direto do django

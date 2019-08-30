from django.conf.urls import url
from .views import base_view, scrape


urlpatterns = [
    url(r'^$', base_view, name='finder'),
    url(r'^scape/', scrape, name='scape'),
]
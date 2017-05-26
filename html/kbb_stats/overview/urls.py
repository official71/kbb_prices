from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='kbb data query'),
    url(r'^(?P<make>[^/]*)/$', views.make, name='make'),
    url(r'^(?P<make>[^/]*)/(?P<model>[^/]*)/$', views.model, name='model')
]
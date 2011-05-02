from django.conf.urls.defaults import *

from views import login

urlpatterns = patterns('',
    (r'^$', login),
)

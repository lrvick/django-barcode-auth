from django.conf.urls.defaults import *

from views import barlogin

urlpatterns = patterns('',
    (r'^$', barlogin),
)

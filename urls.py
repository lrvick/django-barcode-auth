from django.conf.urls.defaults import *

from views import login, logout

urlpatterns = patterns('',
    (r'^$', login),
    (r'^login/', login),
    (r'^logout', logout),
)

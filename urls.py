from django.conf.urls.defaults import *

from views import login, logout, register

urlpatterns = patterns('',
    (r'^$', login),
    (r'^login', login),
    (r'^logout', logout),
    (r'^register', register),
)

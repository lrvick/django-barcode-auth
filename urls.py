from django.conf.urls.defaults import *

from views import login, logout, register, reprint, profile

urlpatterns = patterns('',
    (r'^$', login),
    (r'^login', login),
    (r'^logout', logout),
    (r'^register', register),
    (r'^profile/(?P<userprofile>.*)$', profile),
    (r'^reprint/(?P<username>.*)$', reprint),
)

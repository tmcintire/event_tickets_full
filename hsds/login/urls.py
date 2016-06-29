from django.conf.urls import url, patterns, include
from django.contrib.auth.views import password_change
from views import login, auth_view, invalid_login, logout, loggedin, account

urlpatterns = [
    url(r'^login/$', login, name="login"),
    url(r'^auth/$', auth_view, name="auth_view"),
    url(r'^logout/$', logout, name="logout"),
    url(r'^invalid/$', invalid_login, name="invalid_login"),
    url(r'^loggedin/$', loggedin, name="loggedin"),
    url(r'^user/$', account, name="account"),
    url(r'^password_change/$', password_change, name="change_password")

]
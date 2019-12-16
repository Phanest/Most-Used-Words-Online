
from django.conf.urls import url
from . import views

app_name='main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^more/sites$', views.moresites, name='sites'),
    url(r'^more/sites/Add/$', views.addSite, name='add'),
    url(r'^more/results$', views.more, name='more'),
]

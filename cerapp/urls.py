from django.conf.urls import url, include
from django.urls import path

from .views import home, pdf,MyModelView,MyModelDownloadView,WriteView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    url(r'^$', WriteView.as_view(), name='home'),
    url('m/1', MyModelView.as_view),
    url(r'^posts/(?P<pk>[0-9]+)/$', MyModelView.as_view(), name='posts'),
    url(r'^post/(?P<pk>[0-9]+)/$', MyModelDownloadView.as_view(), name='post'),
    url(r'^write/$', WriteView.as_view(success_url="/posts/"), name='write')

]

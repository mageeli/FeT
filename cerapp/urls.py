from django.conf.urls import url, include
from django.urls import path

from .views import home, pdf,MyModelView,MyModelDownloadView,WriteView

urlpatterns = [
    url(r'^$', WriteView.as_view(), name='home'),
    url('m/1', MyModelView.as_view),
    url(r'^post/(?P<pk>[0-9]+)/$', MyModelDownloadView.as_view(), name='post'),
    url(r'^write/$', WriteView.as_view(success_url="/posts/"), name='write')

]
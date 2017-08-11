from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^morphs/$', views.MorphListView.as_view(), name='morph_list'),
]

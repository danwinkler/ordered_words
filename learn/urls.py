from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^morphs/$', views.MorphListView.as_view(), name='morph_list'),
    url(r'^morphs/(?P<pk>\w+)/$', views.MorphDetailView.as_view(), name='morph_detail'),
    url(r'^sentences/$', views.SentenceListView.as_view(), name='sentence_list'),
    url(r'^sentences/(?P<pk>\w+)/$', views.SentenceDetailView.as_view(), name='sentence_detail'),

]

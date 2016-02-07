from django.conf.urls import url
from game_api import views

urlpatterns = [
    url(r'^players/$', views.player_list),
    url(r'^players/(?P<pk>[0-9]+)/$', views.player_detail),
]
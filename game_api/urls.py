from django.conf.urls import url
from game_api import views

urlpatterns = [
    url(r'^players/$', views.player_list),
    url(r'^players/(?P<pk>[0-9]+)/$', views.player_detail),
    url(r'^games/$', views.game_list),
    url(r'^games/(?P<pk>[0-9]+)/$', views.game_detail),
    url(r'^games/(?P<pk>[0-9]+)/start_space/$', views.game_start_space),
    url(r'^settings/$', views.settings_list),
    url(r'^settings/(?P<pk>[0-9]+)/$', views.settings_detail),
    url(r'^snapshots/$', views.snapshot_list),
    url(r'^snapshots/(?P<pk>[0-9]+)/$', views.snapshot_detail),
    url(r'^spaces/$', views.space_list),
    url(r'^spaces/(?P<pk>[0-9]+)/$', views.space_detail),
    url(r'^spaces/(?P<pk>[0-9]+)/start/$', views.space_start),
]
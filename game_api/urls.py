from django.conf.urls import url
from game_api import views

urlpatterns = [
    url(r'^players/$', views.PlayerListView.as_view()),
    url(r'^players/(?P<pk>[0-9]+)/$', views.PlayerDetailView.as_view()),
    url(r'^games/$', views.GameListView.as_view()),
    url(r'^games/(?P<pk>[0-9]+)/$', views.GameDetailView.as_view()),
    url(r'^games/(?P<pk>[0-9]+)/start_space/$', views.game_start_space),
    url(r'^games/(?P<pk>[0-9]+)/snapshots/$', views.game_snapshot_list),
    url(r'^settings/$', views.SettingsListView.as_view()),
    url(r'^settings/(?P<pk>[0-9]+)/$', views.SettingsDetailView.as_view()),
    url(r'^snapshots/$', views.SnapshotListView.as_view()),
    url(r'^snapshots/(?P<pk>[0-9]+)/$', views.SnapshotDetailView.as_view()),
    url(r'^spaces/$', views.SpaceListView.as_view()),
    url(r'^spaces/(?P<pk>[0-9]+)/$', views.SpaceDetailView.as_view()),
    url(r'^spaces/(?P<pk>[0-9]+)/start/$', views.space_start),
]
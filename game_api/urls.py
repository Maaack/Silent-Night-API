from django.conf.urls import url, include
from game_api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'games', views.GameViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^players/$', views.PlayerListView.as_view()),
    url(r'^players/(?P<pk>[0-9]+)/$', views.PlayerDetailView.as_view()),
    url(r'^settings/$', views.SettingsListView.as_view(), name='settings-detail'),
    url(r'^settings/(?P<pk>[0-9]+)/$', views.SettingsDetailView.as_view(), name='settings-detail'),
    url(r'^snapshots/$', views.SnapshotListView.as_view(), name='snapshot-detail'),
    url(r'^snapshots/(?P<pk>[0-9]+)/$', views.SnapshotDetailView.as_view(), name='snapshot-detail'),
    url(r'^spaces/$', views.SpaceListView.as_view(), name='space-detail'),
    url(r'^spaces/(?P<pk>[0-9]+)/$', views.SpaceDetailView.as_view(), name='space-detail'),
    url(r'^spaces/(?P<pk>[0-9]+)/start/$', views.space_start),
]
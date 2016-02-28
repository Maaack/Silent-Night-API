from django.conf.urls import url, include
from game_api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'games', views.GameViewSet)
router.register(r'players', views.PlayerViewSet)
router.register(r'space_settings', views.SpaceSettingsViewSet)
router.register(r'snapshots', views.SnapshotViewSet)
router.register(r'spaces', views.SpaceViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
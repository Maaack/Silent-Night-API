from django.conf.urls import url
from player_api import views

urlpatterns = [
    url(r'^profiles/$', views.profile_list),
]
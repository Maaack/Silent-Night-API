from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import (Player,
                     Game,
                     Snapshot,
                     Settings,
                     GameSettings,
                     SpaceSettings,
                     Space)
from .models.serializers import (PlayerSerializer,
                                 GameSerializer,
                                 GameSettingsSerializer,
                                 SpaceSettingsSerializer,
                                 SnapshotSerializer,
                                 SpaceSerializer)
from silent_night.mixins.views import BaseViewSet
from rest_framework.response import Response
from rest_framework.decorators import detail_route


# Create your views here.
class GameViewSet(BaseViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @detail_route()
    def snapshots(self, request, *args, **kwargs):
        game = self.get_object()
        serializer = SnapshotSerializer(game.snapshot_set, context={'request': request}, many=True)
        return Response(serializer.data)

    @detail_route()
    def start_space(self, request, *args, **kwargs):
        game = self.get_object()
        space = game.create_space()
        serializer = SpaceSerializer(space, context={'request': request})
        return Response(serializer.data)


class SpaceViewSet(BaseViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer

    @detail_route()
    def start(self, request, *args, **kwargs):
        space = self.get_object()
        space.start_space()
        serializer = SpaceSerializer(space, context={'request': request})
        return Response(serializer.data)


class PlayerViewSet(BaseViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class GameSettingsViewSet(BaseViewSet):
    queryset = GameSettings.objects.all()
    serializer_class = GameSettingsSerializer


class SpaceSettingsViewSet(BaseViewSet):
    queryset = SpaceSettings.objects.all()
    serializer_class = SpaceSettingsSerializer


class SnapshotViewSet(BaseViewSet):
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer

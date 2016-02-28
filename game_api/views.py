from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import (Player,
                     Game,
                     Snapshot,
                     Settings,
                     Space)
from .models.serializers import (PlayerSerializer,
                                 GameSerializer,
                                 SettingsSerializer,
                                 SnapshotSerializer,
                                 SpaceSerializer)
from silent_night.mixins.views import (default_process_detail_request,
                                       default_process_list_request,
                                       BaseListView,
                                       BaseDetailView)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


# Create your views here.
@csrf_exempt
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def game_snapshot_list(request, pk):
    """
    List all snapshots in the game, or create a new snapshot.
    """
    if request.method == 'GET':
        snapshots = Snapshot.objects.filter(game_id=pk)
        serializer = SnapshotSerializer(snapshots, many=True)
        return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def game_start_space(request, pk):
    """
    Make a game start a new Space
    """
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return HttpResponse(status=404)
    serializer_class = GameSerializer
    object_class = Game

    if request.method == 'POST':
        game.create_space()
        serializer = serializer_class(game)
        return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def space_start(request, pk):
    """
    Make a Space start itself up
    """
    try:
        space = Space.objects.get(pk=pk)
    except Space.DoesNotExist:
        return HttpResponse(status=404)
    serializer_class = SpaceSerializer
    object_class = Space

    if request.method == 'POST':
        space.start_space()
        serializer = serializer_class(space)
        return Response(serializer.data)


class GameListView(BaseListView):
    object_class = Game
    serializer_class = GameSerializer


class GameDetailView(BaseDetailView):
    object_class = Game
    serializer_class = GameSerializer


class PlayerListView(BaseListView):
    object_class = Player
    serializer_class = PlayerSerializer


class PlayerDetailView(BaseDetailView):
    object_class = Player
    serializer_class = PlayerSerializer


class SettingsListView(BaseListView):
    object_class = Settings
    serializer_class = SettingsSerializer


class SettingsDetailView(BaseDetailView):
    object_class = Settings
    serializer_class = SettingsSerializer


class SnapshotListView(BaseListView):
    object_class = Snapshot
    serializer_class = SnapshotSerializer


class SnapshotDetailView(BaseDetailView):
    object_class = Snapshot
    serializer_class = SnapshotSerializer


class SpaceListView(BaseListView):
    object_class = Snapshot
    serializer_class = SnapshotSerializer


class SpaceDetailView(BaseDetailView):
    object_class = Snapshot
    serializer_class = SnapshotSerializer
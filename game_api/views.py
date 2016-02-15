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
                                       default_process_list_request)
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def player_list(request):
    """
    List all players, or create a new player.
    """
    serializer_class = PlayerSerializer
    object_class = Player
    return default_process_list_request(request, serializer_class, object_class)

    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def player_detail(request, pk):
    """
    Retrieve, update or delete a Player.
    """
    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        return HttpResponse(status=404)
    serializer_class = PlayerSerializer
    object_class = Player

    return default_process_detail_request(request, serializer_class, player)

# Giving way too many permissions for now
# I want to get to a point of being able to interact by any means
# and will restrict permissions once everything is working
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def game_list(request):
    """
    List all players, or create a new game.
    """
    serializer_class = GameSerializer
    object_class = Game
    return default_process_list_request(request, serializer_class, object_class)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def game_detail(request, pk):
    """
    Retrieve, update or delete a game.
    """
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return HttpResponse(status=404)
    serializer_class = GameSerializer
    object_class = Game

    return default_process_detail_request(request, serializer_class, game)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def settings_list(request):
    """
    List all players, or create a new snapshot.
    """
    serializer_class = SettingsSerializer
    object_class = Settings
    return default_process_list_request(request, serializer_class, object_class)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def settings_detail(request, pk):
    """
    Retrieve, update or delete a snapshot.
    """
    try:
        settings = Settings.objects.get(pk=pk)
    except Settings.DoesNotExist:
        return HttpResponse(status=404)
    serializer_class = SettingsSerializer
    object_class = Settings

    return default_process_detail_request(request, serializer_class, settings)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def snapshot_list(request):
    """
    List all players, or create a new snapshot.
    """
    serializer_class = SnapshotSerializer
    object_class = Snapshot
    return default_process_list_request(request, serializer_class, object_class)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def snapshot_detail(request, pk):
    """
    Retrieve, update or delete a snapshot.
    """
    try:
        snapshot = Snapshot.objects.get(pk=pk)
    except Snapshot.DoesNotExist:
        return HttpResponse(status=404)
    serializer_class = SnapshotSerializer
    object_class = Snapshot

    return default_process_detail_request(request, serializer_class, snapshot)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def space_list(request):
    """
    List all players, or create a new space.
    """
    serializer_class = SpaceSerializer
    object_class = Space
    return default_process_list_request(request, serializer_class, object_class)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def space_detail(request, pk):
    """
    Retrieve, update or delete a space.
    """
    try:
        space = Space.objects.get(pk=pk)
    except Space.DoesNotExist:
        return HttpResponse(status=404)
    serializer_class = SpaceSerializer
    object_class = Space

    return default_process_detail_request(request, serializer_class, space)


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


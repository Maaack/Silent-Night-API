from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import (Player,
                     Game,
                     Snapshot,
                     Settings,
                     SpaceSettings,
                     Space)
from .models.serializers import (PlayerSerializer,
                                 GameSerializer,
                                 SpaceSettingsSerializer,
                                 SnapshotSerializer,
                                 SpaceSerializer)
from silent_night.mixins.views import (BaseListView,
                                       BaseDetailView,
                                       BaseViewSet)
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, detail_route
from rest_framework import permissions


# Create your views here.
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


class SpaceSettingsViewSet(BaseViewSet):
    queryset = SpaceSettings.objects.all()
    serializer_class = SpaceSettingsSerializer


class SnapshotViewSet(BaseViewSet):
    queryset = Snapshot.objects.all()
    serializer_class = SnapshotSerializer

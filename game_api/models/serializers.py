from rest_framework import serializers
from .models import Player, Game, GameSettings, SpaceSettings, Snapshot, Space


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        fields = ('id', 'name', 'data')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
            model = Player
            fields = ('id',)


class GameSerializer(serializers.HyperlinkedModelSerializer):
    settings = serializers.ReadOnlyField(source='settings.data')

    class Meta:
        model = Game
        fields = ('id', 'code', 'name', 'settings', 'space_set', 'snapshot_set')


class GameSettingsSerializer(SettingsSerializer):
    class Meta:
        model = GameSettings


class SpaceSettingsSerializer(SettingsSerializer):
    class Meta:
        model = SpaceSettings


class SnapshotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Snapshot
        fields = ('id', 'state', 'game_time', 'game', 'space')


class SpaceSerializer(serializers.HyperlinkedModelSerializer):
    settings = serializers.ReadOnlyField(source='settings.data')

    class Meta:
        model = Space
        fields = ('id', 'settings', 'game', 'seed', 'snapshot_set', 'initial_snapshot')
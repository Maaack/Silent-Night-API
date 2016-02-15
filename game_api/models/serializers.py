from rest_framework import serializers
from .models import Player, Game, Settings, Snapshot, Space


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
            model = Player
            fields = ('id',)


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'code', 'name', 'settings')


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ('id', 'name', 'data')


class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fields = ('id', 'state', 'game_time', 'game', 'space')


class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ('id', 'settings', 'game', 'seed')
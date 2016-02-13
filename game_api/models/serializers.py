from rest_framework import serializers
from .models import Player, Game, Settings, Snapshot


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
        fields = ('name', 'data')


class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fields = ('state', 'game_time', 'game', 'space')


class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fields = ('settings', 'seed', )
from django.db.models import fields
from events.models import Events, Rooms, Users
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username')

class EventSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Events
        fields = ('summary', 'start_time', 'end_time', 'users')

class RoomSerializer(serializers.ModelSerializer):
    evnets = EventSerializer(many=True, read_only=True)
    class Meta:
        model = Rooms
        fields = ('name', 'evnets')

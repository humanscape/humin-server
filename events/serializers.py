from events.models import Event, Room, Users
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    class Meta:
        model = Event
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)
    class Meta:
        model = Room
        fields = '__all__'

    def update(self, instance, validated_data):
        for event_data in validated_data.pop("events"):
            users = event_data.pop("users")
            event = Event.objects.create(room=instance, **event_data)
            for user_data in users:
                Users.objects.create(event=event, **user_data)
        return instance

class RoomNameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Room
        fields = ('name',)
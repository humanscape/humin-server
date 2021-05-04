from events.models import Events, Rooms, Users
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    users = UserSerializer(required=True, many=True)
    class Meta:
        model = Events
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    events = EventSerializer(required=True, many=True)
    class Meta:
        model = Rooms
        fields = '__all__'

    def update(self, instance, validated_data):
        for event_data in validated_data.pop("events"):
            event_data["room"] = instance
            event = Events.objects.create(**event_data)
            for user_data in event_data.pop("users"):
                user_data["event"] = event
                Users.objects.create(**user_data)
        return instance
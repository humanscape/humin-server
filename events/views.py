from django.http.response import JsonResponse
from events import serializers
from events.serializers import EventSerializer, RoomSerializer
from events.models import Rooms
import time

curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
serializer = RoomSerializer
query_set = Rooms.objects.all().filter(events__end_time__gte=curtime)

def list(request):
    room_serializer = serializer(instance=query_set, many=True)
    return JsonResponse(room_serializer.data, safe=False)

def retrieve(request, room_name):
    global query_set
    print(room_name)
    query_set = query_set.filter(name=room_name)
    room_serializer = serializer(instance=query_set, many=True)
    return JsonResponse(room_serializer.data, safe=False)

def retrieve_first(request, room_name):
    global query_set
    query_set = query_set.filter(name=room_name).first()
    room_serializer = serializer(instance=query_set)
    return JsonResponse(room_serializer.data, safe=False)
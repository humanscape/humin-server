from django.http.response import JsonResponse
from events.serializers import RoomNameSerializer, Roomerializer
from events.models import Room

def get_query_set():
    query_set = Room.objects.all()
    return query_set
    
def get_full_roomnames(request):
    roomname_serializer = RoomNameSerializer(get_query_set(), many=True)
    return JsonResponse(roomname_serializer.data, safe=False)

def list(request):
    room_serializer = Roomerializer(instance=get_query_set(), many=True)
    return JsonResponse(room_serializer.data, safe=False)

def retrieve(request, room_name):
    query_set = get_query_set().filter(name=room_name).first()
    room_serializer = Roomerializer(instance=query_set)
    return JsonResponse(room_serializer.data, safe=False)
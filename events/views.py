from django.http.response import JsonResponse
from events.serializers import RoomSerializer
from events.models import Rooms

def get_query_set():
    query_set = Rooms.objects.all()
    return query_set
    
def list(request):
    room_serializer = RoomSerializer(instance=get_query_set(), many=True)
    return JsonResponse(room_serializer.data, safe=False)

def retrieve(request, room_name):
    query_set = get_query_set().filter(name=room_name).first()
    room_serializer = RoomSerializer(instance=query_set)
    return JsonResponse(room_serializer.data, safe=False)
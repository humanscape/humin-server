from django.http.response import JsonResponse
from events.serializers import RoomSerializer
from events.models import Events, Rooms
from django.utils import timezone
from django.db.models import OuterRef, Subquery

def get_query_set():
    # filtered_events = Events.objects.filter(start_time__gte=timezone.now(), room=OuterRef("id"))
    # query_set = Rooms.objects.all().annotate(filtered_events=Subquery(filtered_events))
    query_set = Rooms.objects.all()
    return query_set
    
def list(request):
    room_serializer = RoomSerializer(instance=get_query_set(), many=True)
    return JsonResponse(room_serializer.data, safe=False)

def retrieve(request, room_name):
    query_set = get_query_set().filter(name=room_name).first()
    room_serializer = RoomSerializer(instance=query_set)
    return JsonResponse(room_serializer.data, safe=False)
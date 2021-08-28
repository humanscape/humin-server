from django.http.response import JsonResponse
from events.serializers import RoomNameSerializer, RoomSerializer
from events.models import Room
from rest_framework import viewsets, mixins


class EventViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Room.objects

    def get_queryset(self):
        query_set = super().get_queryset()
        if self.mode == "list" or self.mode == "retrieve":
            query_set = query_set.prefetch_related("events").prefetch_related(
                "events__users"
            )
        return query_set

    def get_full_roomnames(self, request):
        self.mode = "get_full_roomnames"
        roomname_serializer = RoomNameSerializer(get_queryset(), many=True)
        return JsonResponse(roomname_serializer.data, safe=False)

    def list(self, request, *args, **kwargs):
        self.mode = "list"
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.mode = "retrieve"
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        return RoomSerializer

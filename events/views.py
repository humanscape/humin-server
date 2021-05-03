from events.serializers import EventSerializer, RoomSerializer
from events.models import Rooms
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins

class EventViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Rooms.objects
    serializer_class = RoomSerializer
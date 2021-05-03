from events import serializers
from events.serializers import EventSerializer, RoomSerializer
from events.models import Rooms
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins

serializer = RoomSerializer
query_set = Rooms.objects

def list(request):
    pass

def retrieve(request, room_name):
    pass

def retrieve_first(request, room_name):
    pass
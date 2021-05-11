from events.models import Users
from django.shortcuts import render
from users.models import Users

def get_query_set():
    query_set = Users.objects.all()

def list(request):
    pass

def retrieve(request, email):
    pass

def search(request, keyword):
    pass
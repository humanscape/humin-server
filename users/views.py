from users.serializers import UserSerializer
from django.http.response import JsonResponse
from events.models import Users
from django.shortcuts import render
from users.models import Users

def get_query_set():
    query_set = Users.objects.all()
    return query_set

def list(request):
    user_serializer = UserSerializer(instance=get_query_set(), many=True)
    return JsonResponse(user_serializer.data, safe=False)

def retrieve(request, email):
    query_set = get_query_set().filter(email=email)
    user_serializer = UserSerializer(instance=query_set)
    return JsonResponse(user_serializer.data, safe=False)

def search(request, keyword):
    query_set = get_query_set().filter(email__contains=keyword)
    user_serializer = UserSerializer(instance=query_set, many=True)
    return JsonResponse(user_serializer.data, safe=False)
    

def list_by_organization(request, organization):
    if organization=='humanscape.io':
        query_set = get_query_set().filter(organization=1)
    elif organization=='mmtalk.kr':
        query_set = get_query_set().filter(organization=2)
    else:
        query_set = get_query_set().none()
    user_serializer = UserSerializer(instance=query_set, many=True)
    return JsonResponse(user_serializer.data, safe=False)
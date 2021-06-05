from events.serializers import Roomerializer
from events.models import Events, Room
from django.http.response import HttpResponse
import time
import jwt
import json
import requests
from django.utils import timezone
from dateutil.parser import parse

def get_signed_jwt(token_json):
    private_key_id = token_json.get("private_key_id")
    private_key = token_json.get("private_key")

    iat = time.time()
    exp = iat + 3600
    payload = {
        'iss': token_json.get("client_email"),
        'scope': 'https://www.googleapis.com/auth/calendar.readonly',
        'aud': token_json.get("token_uri"),
        'iat': iat,
        'exp': exp
    }
    additional_headers = {'kid': private_key_id} 
    signed_jwt = jwt.encode(payload, private_key, headers=additional_headers,algorithm='RS256') 
    return signed_jwt

def get_access_token():
    token_json = json.load(open("env/token.json"))
    jwt = get_signed_jwt(token_json)
    response = requests.post(
        token_json.get("token_uri"),
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': jwt
        }
    )
    response.raise_for_status()
    return response.json()['access_token']

def get_event_list(calendar_id):
    access_token = get_access_token()
    curtime = time.strftime('%Y-%m-%dT00:00:00z', time.localtime(time.time()))
    URL = 'https://www.googleapis.com/calendar/v3/calendars/'+calendar_id +'/events'+'?timeMin='+curtime
    request_header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
        "X-GFE-SSL": "yes"
    }
    response = requests.get(URL, headers=request_header)
    
    if response.json().get("items"):
        result = list()
        if response.json().get("items") is not None:
            for event in response.json().get("items"):
                users = list()
                if event.get("summary"):
                    summary = event.get("summary")
                else:
                    summary = "제목없음"
                if event.get("status")!="cancelled" and parse(event.get("end").get("dateTime"))>=timezone.now():
                    for user in event.get("attendees"):
                        users.append({"username": user.get("email")})
                    result.append({
                        "summary": summary,
                        "start_time": event.get("start").get("dateTime"),
                        "end_time": event.get("end").get("dateTime"),
                        "users": users
                    })
            return result

# 일단 업데이트 시마다 event table 초기화 후 insert 하는 방식으로 진행
# 이후 핸들링 코드 추가 시 etag로 event판별해서 update하는 방식으로 진행
def get(request):
    Events.objects.all().delete()
    for room in Room.objects.all():
        event_list = get_event_list(room.calendar_id)
        if event_list:
            event_list.sort(key=lambda event: event["end_time"])
            room_serializer = Roomerializer(instance=room, data={"events": event_list}, partial=True)
            try:
                if room_serializer.is_valid(raise_exception=True):
                    room_serializer.save()
            except Exception as e:
                print("데이터 저장 중 오류 발생")
                print(e)
                print(event_list)
    return HttpResponse("Success")

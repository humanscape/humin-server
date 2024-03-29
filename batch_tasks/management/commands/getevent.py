from os import stat
from events.serializers import RoomSerializer
from events.models import Event, Room
import time
import jwt
import json
import requests
from urllib import parse
from django.core.management.base import BaseCommand
from django.db import transaction
import datetime


class Command(BaseCommand):
    @staticmethod
    def get_signed_jwt(token_json):
        private_key_id = token_json.get("private_key_id")
        private_key = token_json.get("private_key")

        iat = time.time()
        exp = iat + 3600
        payload = {
            "iss": token_json.get("client_email"),
            "scope": "https://www.googleapis.com/auth/calendar.readonly",
            "aud": token_json.get("token_uri"),
            "iat": iat,
            "exp": exp,
        }
        additional_headers = {"kid": private_key_id}
        signed_jwt = jwt.encode(
            payload, private_key, headers=additional_headers, algorithm="RS256"
        )
        return signed_jwt

    @staticmethod
    def get_access_token():
        token_json = json.load(open("env/token.json"))
        jwt = Command.get_signed_jwt(token_json)
        response = requests.post(
            token_json.get("token_uri"),
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": jwt,
            },
        )
        response.raise_for_status()
        return response.json()["access_token"]

    @staticmethod
    def get_event_list(calendar_id):
        access_token = Command.get_access_token()
        now = datetime.datetime.now()
        timeMin = now.strftime("%Y-%m-%dT%H:%M:%S+09:00")
        timeMax = (now + datetime.timedelta(30)).strftime("%Y-%m-%dT%H:%M:%S+09:00")

        URL = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events?orderBy=startTime&singleEvents=True&timeMin={parse.quote(timeMin)}&timeMax={parse.quote(timeMax)}"
        request_header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
            "X-GFE-SSL": "yes",
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
                    if event.get("status") != "cancelled":
                        for user in event.get("attendees"):
                            users.append({"username": user.get("email")})
                        result.append(
                            {
                                "summary": summary,
                                "start_time": event.get("start").get("dateTime"),
                                "end_time": event.get("end").get("dateTime"),
                                "users": users,
                            }
                        )
                return result

    @transaction.atomic
    def handle(self, *args, **options):
        help = "get google calendar events"
        Event.objects.all().delete()
        for room in Room.objects.all():
            event_list = Command.get_event_list(room.calendar_id)
            if event_list:
                event_list.sort(key=lambda event: event["end_time"])
                room_serializer = RoomSerializer(
                    instance=room, data={"events": event_list}, partial=True
                )
                try:
                    if room_serializer.is_valid(raise_exception=True):
                        room_serializer.save()
                except Exception as e:
                    print("데이터 저장 중 오류 발생")
                    print(e)
                    print(event_list)
        self.stdout.write(self.style.SUCCESS("success"))

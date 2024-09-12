from rest_framework import viewsets
from rest_framework.response import Response
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os

from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        task = serializer.save()
        self.add_to_calendar(task)

    def perform_destroy(self, instance):
        if instance.google_calendar_id:
            self.delete_from_google_calendar(instance.google_calendar_id)
        instance.delete()

    def add_to_calendar(self, task):
        service = self.authenticate_google_calendar()
        event = {
            'summary': task.title,
            'description': task.description,
            'start': {
                'date': task.date.isoformat(),
            },
            'end': {
                'date': task.date.isoformat(),
            }
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()
        task.google_calendar_id = created_event.get('id')
        task.save()

    def delete_from_google_calendar(self, google_calendar_id):
        service = self.authenticate_google_calendar()
        try:
            service.events().delete(calendarId='primary', eventId=google_calendar_id).execute()
        except Exception as e:
            print(f"Error deleting event: {e}")

    def authenticate_google_calendar(self):
        SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return build("calendar", "v3", credentials=creds)

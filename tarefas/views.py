from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os

from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = TaskFilter

    search_fields = ['title'] 
    ordering_fields = ['date'] 
    
    def perform_create(self, serializer):
        task = serializer.save()
        self.add_to_calendar(task)

    def perform_destroy(self, instance):
        if instance.google_calendar_id:
            self.delete_from_google_calendar(instance.google_calendar_id)
        instance.delete()
        
    def perform_update(self, serializer):
      task = serializer.save()
      if task.google_calendar_id:
          self.update_google_calendar_event(task)

    def add_to_calendar(self, task):
        service = self.authenticate_google_calendar()
        if task.time:
            event = {
                'summary': task.title,
                'description': task.description,
                'start': {
                    'dateTime': f"{task.date}T{task.time}",
                    'timeZone': 'America/Sao_Paulo',
                },
                'end': {
                    'dateTime': f"{task.date}T{task.time}",
                    'timeZone': 'America/Sao_Paulo',
                }
            }
        else:
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
        
    def update_google_calendar_event(self, task):
        service = self.authenticate_google_calendar()
        try:
            event = service.events().get(calendarId='primary', eventId=task.google_calendar_id).execute()
        except Exception as e:
            print(f"Error fetching event: {e}")
            return
        event = {
            'summary': task.title,
            'description': task.description,
            'start': {
                'dateTime': f"{task.date}T{task.time}",
                'timeZone': 'America/Sao_Paulo', 
            },
            'end': {
                'dateTime': f"{task.date}T{task.time}",
                'timeZone': 'America/Sao_Paulo',
            }
        }
        try:
            updated_event = service.events().update(calendarId='primary', eventId=task.google_calendar_id, body=event).execute()
            print(f"Event updated: {updated_event.get('id')}")
        except Exception as e:
            print(f"Error updating event: {e}")
    
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

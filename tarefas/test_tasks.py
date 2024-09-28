from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken

class TaskTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(title='Test Task', description='Test Description', date='2024-09-20')
        self.client.login(username='testuser', password='testpassword')
        
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def test_create_task(self):
        url = reverse('tasks-list')
        data = {'title': 'New Task', 'description': 'New Description', 'date': '2024-09-22'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_tasks(self):
        url = reverse('tasks-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 

    def test_update_task(self):
        url = reverse('tasks-detail', args=[self.task.id])
        data = {'title': 'Updated Task', 'description': 'Updated Description', 'date': '2024-09-21'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task(self):
        url = reverse('tasks-detail', args=[self.task.id]) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

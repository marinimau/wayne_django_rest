from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from user.models import Profile


class UserTestAcceptance(TestCase):

    factory = APIRequestFactory()

    def test_registration_correct(self):
        users_count = User.objects.count()
        profile_count = Profile.objects.count()
        url = reverse('users-list')
        data = {
            'email': 'test@test.com',
            'username': 'test',
            'password': 'Prova123.',
            'password2': 'Prova123.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), users_count+1)
        self.assertEqual(Profile.objects.count(), profile_count+1)
        self.assertEqual(User.objects.get(username=data['username']).username, data['username'])
        self.assertEqual(User.objects.get(username=data['username']).email, data['email'])
        self.assertEqual(User.objects.get(username=data['username']).is_superuser, False)
        self.assertEqual(User.objects.get(username=data['username']).is_active, False)




from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, URLPatternsTestCase, force_authenticate

from user.models import Profile


class UserTestAcceptance(TestCase, URLPatternsTestCase):

    factory = APIRequestFactory()
    client = APIClient()

    urlpatterns = [
        path('', include('user.urls')),
    ]

    def setUp(self):
        # User setup
        self.user = User.objects.create_user(username='admin', password='Prova123.', is_superuser=True, email='admin@test.com')
        self.user.save()
        self.user = User.objects.create_user(username='utente1', password='Prova123.', email='utente1@test.com')
        self.user.save()
        self.user2 = User.objects.create_user(username='utente2', password='Prova123.', email='utente2@test.com')
        self.user2.save()

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   User list view
    #
    # ------------------------------------------------------------------------------------------------------------------

    def test_view_user_list_default(self):
        url = reverse('users-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_view_user_list_default_as_superuser(self):
        self.client.login(username='admin', password='Prova123.')
        url = reverse('users-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   User detail view
    #
    # ------------------------------------------------------------------------------------------------------------------

    def test_view_user_detail_default(self):
        factory = APIRequestFactory()
        user = User.objects.get(username='utente1')
        # Make an authenticated request to the view...
        request = factory.get('/users/1')
        force_authenticate(request, user=user)
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_view_user_list_detail_as_superuser(self):
        self.client.login(username='admin', password='Prova123.')
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   User Registration Testing
    #
    # ------------------------------------------------------------------------------------------------------------------

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
        user = User.objects.get(username=data['username'])
        self.assertEqual(Profile.objects.filter(user=user.pk).count(), 1)
        self.assertEqual(User.objects.get(username=data['username']).username, data['username'])
        self.assertEqual(User.objects.get(username=data['username']).email, data['email'])
        self.assertFalse(User.objects.get(username=data['username']).is_superuser)
        self.assertFalse(User.objects.get(username=data['username']).is_active)
        self.assertTrue(User.is_authenticated)

    def test_registration_email_already_exists(self):
        users_count = User.objects.count()
        profile_count = Profile.objects.count()
        url = reverse('users-list')
        data = {
            'email': 'utente1@test.com',
            'username': 'test',
            'password': 'Prova123.',
            'password2': 'Prova123.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'email already used')
        self.assertEqual(User.objects.count(), users_count)
        self.assertEqual(Profile.objects.count(), profile_count)

    def test_registration_username_already_exists(self):
        users_count = User.objects.count()
        profile_count = Profile.objects.count()
        url = reverse('users-list')
        data = {
            'email': 'test@test.com',
            'username': 'utente1',
            'password': 'Prova123.',
            'password2': 'Prova123.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(User.objects.count(), users_count)
        self.assertEqual(Profile.objects.count(), profile_count)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'username already used')

    def test_registration_password_unsecure(self):
        users_count = User.objects.count()
        profile_count = Profile.objects.count()
        url = reverse('users-list')
        data = {
            'email': 'test@test.com',
            'username': 'test',
            'password': 'Prova123',
            'password2': 'Prova123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'password insecure')
        self.assertEqual(User.objects.count(), users_count)
        self.assertEqual(Profile.objects.count(), profile_count)

    def test_registration_password_mismatch(self):
        users_count = User.objects.count()
        profile_count = Profile.objects.count()
        url = reverse('users-list')
        data = {
            'email': 'test@test.com',
            'username': 'test',
            'password': 'Prova123.',
            'password2': 'Prova123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'password mismatch')
        self.assertEqual(User.objects.count(), users_count)
        self.assertEqual(Profile.objects.count(), profile_count)

    def test_registration_input_error_1(self):
        users_count = User.objects.count()
        profile_count = Profile.objects.count()
        url = reverse('users-list')
        data = {
            # no email
            'username': 'test',
            'password': 'Prova123',
            'password2': 'Prova123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'input error')
        self.assertEqual(User.objects.count(), users_count)
        self.assertEqual(Profile.objects.count(), profile_count)

    def test_registration_input_error_2(self):
        users_count = User.objects.count()
        profile_count = Profile.objects.count()
        url = reverse('users-list')
        data = {
            'email': 'test@test.com',
            # non username
            'password': 'Prova123',
            'password2': 'Prova123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'input error')
        self.assertEqual(User.objects.count(), users_count)
        self.assertEqual(Profile.objects.count(), profile_count)

    def test_registration_input_error_3(self):
        users_count = User.objects.count()
        profile_count = Profile.objects.count()
        url = reverse('users-list')
        data = {
            'email': 'test@test.com',
            'username': 'test',
            # no password
            'password2': 'Prova123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'input error')
        self.assertEqual(User.objects.count(), users_count)
        self.assertEqual(Profile.objects.count(), profile_count)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   User update testing
    #
    # ------------------------------------------------------------------------------------------------------------------

    # Email

    def test_update_email_correct(self):
        self.client.login(username='utente1', password='Prova123.')
        url = '/users/2/'
        data = {
            'email': 'update@test.com',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_email_unauthorized(self):
        url = '/users/1/'
        data = {
            'email': 'update2@test.com',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Username

    # Password

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Deactivate account
    #
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Profile update testing
    #
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   User activation testing
    #
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   Forgot password testing
    #
    # ------------------------------------------------------------------------------------------------------------------








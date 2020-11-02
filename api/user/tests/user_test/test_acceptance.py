#
#   wayne_django_rest copyright © 2020 - all diricts reserved
#   Created at: 26/10/2020
#   By: mauromarini
#   License: MIT
#   Repository: https://github.com/marinimau/wayne_django_rest
#   Credits: @marinimau (https://github.com/marinimau)
#

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, URLPatternsTestCase

from api.user.models import Profile


class UserTestAcceptance(TestCase, URLPatternsTestCase):

    factory = APIRequestFactory()
    client = APIClient()

    urlpatterns = [
        path('', include('api.user.urls')),
    ]

    def setUp(self):
        # User setup
        self.user = User.objects.create_user(pk=4, username='admin', password='Prova123.', is_superuser=True, email='admin@test.com')
        self.user.save()
        self.user = User.objects.create_user(pk=5, username='utente1', password='Prova123.', email='utente1@test.com')
        self.user.save()
        self.user2 = User.objects.create_user(pk=6, username='utente2', password='Prova123.', email='utente2@test.com')
        self.user2.save()
        self.client = Client()

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   User list view
    #
    # ------------------------------------------------------------------------------------------------------------------

    '''
    test user list visualization without authentication
    '''
    def test_view_user_list_no_auth(self):
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    '''
    test user list visualization with standard authentication
    '''
    def test_view_user_list_default_auth(self):
        self.client.login(username='utente1', password='Prova123.')
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    '''
    test user list visualization as superuser
    '''
    def test_view_user_list_default_as_superuser(self):
        self.client.login(username='admin', password='Prova123.')
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   User detail view
    #
    # ------------------------------------------------------------------------------------------------------------------

    '''
    test user detail visualization no auth - 200_OK
    '''

    def test_view_user_detail_no_auth(self):
        response = self.client.get('/' + str(User.objects.get(username='utente1').id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    '''
    test user detail visualization standard auth - 200_OK
    '''
    def test_view_user_detail_default_auth(self):
        self.client.login(username='admin', password='Prova123.')
        response = self.client.get('/' + str(User.objects.get(username='utente1').id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    '''
    test user detail visualization superuser auth - 200_OK
    '''
    def test_view_user_list_detail_superuser_auth(self):
        self.client.login(username='utente1', password='Prova123.')
        response = self.client.get('/'+str(User.objects.get(username='utente1').id)+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #   User Registration Testing
    #
    # ------------------------------------------------------------------------------------------------------------------

    '''
    test user registration correct
    '''
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

    '''
    test user registration email already exists
    '''
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

    '''
    test user registration username already exists
    '''
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

    '''
    test user registration password unsecure
    '''
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

    '''
    test user registration password mismatch
    '''
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
        response = self.client.post(url, data, content_type='application/json', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'password mismatch')
        self.assertEqual(User.objects.count(), users_count)
        self.assertEqual(Profile.objects.count(), profile_count)

    '''
    test user registration input error 1
    '''
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
        response = self.client.post(url, data, content_type='application/json', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'input error')
        self.assertEqual(User.objects.count(), users_count)
        self.assertEqual(Profile.objects.count(), profile_count)

    '''
    test user registration input error 2
    '''
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
        response = self.client.post(url, data, content_type='application/json', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'input error')
        self.assertEqual(User.objects.count(), users_count)
        self.assertEqual(Profile.objects.count(), profile_count)

    '''
    test user registration input error 3
    '''
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

    '''
    exec the request to update the email
    '''
    def get_update_email_response(self, existent=False):
        url = '/' + str(User.objects.get(username='utente1').id) + '/'
        data = {
            'email': 'update@test.com',
        }
        if existent:
            data = {
                'email': 'utente2@test.com'
            }
        return self.client.put(url, data, content_type='application/json', format='json')

    '''
    test user update email correct
    '''
    def test_update_email_correct(self):
        old_email = User.objects.get(username='utente1').email
        self.client.login(username='utente1', password='Prova123.')
        self.assertEqual(self.get_update_email_response().status_code, status.HTTP_200_OK)
        self.assertNotEqual(old_email, User.objects.get(username='utente1').email)

    '''
    test user update email - existent email
    '''
    def test_update_email_existent_email(self):
        old_email = User.objects.get(username='utente1').email
        self.client.login(username='utente1', password='Prova123.')
        self.assertEqual(self.get_update_email_response(True).status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(old_email, User.objects.get(username='utente1').email)

    '''
    test user update email no auth provided
    '''
    def test_update_email_unauthorized(self):
        old_email = User.objects.get(username='utente1').email
        self.assertEqual(self.get_update_email_response().status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(old_email, User.objects.get(username='utente1').email)

    '''
    test user update email with other user auth
    '''
    def test_update_email_other_user_auth(self):
        old_email = User.objects.get(username='utente1').email
        self.client.login(username='utente2', password='Prova123.')
        self.assertEqual(self.get_update_email_response().status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(old_email, User.objects.get(username='utente1').email)

    '''
    exec the request to update the username
    '''
    def get_update_username_response(self, existent=False):
        url = '/' + str(User.objects.get(username='utente1').id) + '/'
        data = {
            'username': 'new_username',
        }
        if existent:
            data = {
                'username': 'utente2',
            }
        return self.client.put(url, data, content_type='application/json', format='json')

    '''
    test user update username correct
    '''
    def test_update_username_correct(self):
        old_username = User.objects.get(email='utente1@test.com').username
        self.client.login(username='utente1', password='Prova123.')
        self.assertEqual(self.get_update_username_response().status_code, status.HTTP_200_OK)
        self.assertNotEqual(old_username, User.objects.get(email='utente1@test.com').username)

    '''
    test user update username existent username
    '''
    def test_update_username_existent_username(self):
        old_username = User.objects.get(email='utente1@test.com').username
        self.client.login(username='utente1', password='Prova123.')
        self.assertEqual(self.get_update_username_response(True).status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(old_username, User.objects.get(email='utente1@test.com').username)

    '''
    test user update username no auth provided
    '''
    def test_update_username_unauthorized(self):
        old_username = User.objects.get(email='utente1@test.com').username
        self.assertEqual(self.get_update_username_response().status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(old_username, User.objects.get(email='utente1@test.com').username)

    '''
    test user update username with other user auth
    '''
    def test_update_username_other_user_auth(self):
        old_username = User.objects.get(email='utente1@test.com').username
        self.client.login(username='utente2', password='Prova123.')
        self.assertEqual(self.get_update_username_response().status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(old_username, User.objects.get(email='utente1@test.com').username)

    # Password

'''
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


'''





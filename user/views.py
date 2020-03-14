from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


# ----------------------------------------------------------------------------------------------------------------------
#   Generic User views
#   -   user_list
#       - if GET:   list all user object
#       - if POST:  add new user
#   -   user_detail:
#       - if GET:   show user detail
#       - if PUT:   update user detail
# ----------------------------------------------------------------------------------------------------------------------

@csrf_exempt
@api_view(['GET', 'POST'])
def user_list(request, format=None):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def user_detail(request, pk, format=None):
    """
    Retrieve, update or delete a user.
    """
    # check if user exists
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    # if get return user instance
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)
    # if put update user instance
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    # if delete delete user instance
    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)


# ----------------------------------------------------------------------------------------------------------------------
#   User Profile views
#   -   profile_list
#       - if GET:   list all profile object
#       - if POST:  add new profile
#   -   user_detail:
#       - if GET:   show profile detail
#       - if PUT:   update profile detail
# ----------------------------------------------------------------------------------------------------------------------

@csrf_exempt
@api_view(['GET', 'POST'])
def profile_list(request, format=None):
    """
    List all profiles, or create a new user.
    """
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def profile_detail(request, pk, format=None):
    """
    Retrieve, update or delete a profile.
    """
    # check if profile exists
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # if get return profile instance
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    # if put update profali instance
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(profile, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # if delete delete profile instance
    elif request.method == 'DELETE':
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

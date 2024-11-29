from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from authentication.serializers import UserSerializer
from authentication.decorators import role_required

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key}, status=201)
    return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': token.key}, status=200)
    return JsonResponse({'message': 'Invalid credentials'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return JsonResponse({'message': 'Successfully logged out'}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@role_required('Admin')
def admin_only_view(request):
    return JsonResponse({'message': 'Welcome, Admin!'})

from functools import cache
from django.forms import ValidationError
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken

from social_network.settings import CACHE_TTL
from .models import CustomUser, FriendRequest, Friendship
from .serializers import FriendRequestSerializer, FriendshipSerializer, UserSerializer
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, FriendRequest, Friendship
from .serializers import UserSerializer, FriendRequestSerializer, FriendshipSerializer
from rest_framework.views import APIView
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

import logging
logger = logging.getLogger(__name__)

def check_friend_request_limit(user_id):
    # Generate a unique cache key for the user's friend request count
    cache_key = f"friend_requests_{user_id}"
    
    # Get the current count from the cache or initialize to 0
    request_count = cache.get(cache_key, default=0)
    
    # Increment the count and set it back to cache
    request_count += 1
    cache.set(cache_key, request_count, timeout=60)  # Timeout set to 60 seconds (1 minute)
    
    # Check if the user has exceeded the limit
    if request_count > 3:
        raise ValidationError("You cannot send more than 3 friend requests per minute.")

    return request_count

class UserSignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)  # Changed to email if using email as username
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_users(request):
    try:
        query = request.GET.get('query', '')
        if not query:
            return Response({'error': 'Query parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Assuming CustomUser model has 'email' and 'username' fields
        users = CustomUser.objects.filter(Q(email__iexact=query) | Q(username__icontains=query))[:10]
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({'error': 'No users found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f'Error during user search: {e}')
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_friend_request(request):
    data = request.data
    from_user = request.user
    try:
        to_user = CustomUser.objects.get(id=data['to_user_id'])
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    if from_user == to_user:
        return JsonResponse({'error': 'Cannot send request to yourself'}, status=status.HTTP_400_BAD_REQUEST)
    
    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        return JsonResponse({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the request is cached
    cache_key = f"friend_request_limit_{from_user.id}"
    request_count = cache.get(cache_key)

    if request_count is None:
        request_count = 1
    else:
        request_count += 1

    if request_count > 3:
        return JsonResponse({'error': 'You cannot send more than 3 friend requests per minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    cache.set(cache_key, request_count, timeout=CACHE_TTL)

    FriendRequest.objects.create(from_user=from_user, to_user=to_user)
    return JsonResponse({'success': 'Friend request sent'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def respond_friend_request(request):
    data = request.data
    try:
        friend_request = FriendRequest.objects.get(id=data['request_id'])
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    if request.user != friend_request.to_user:
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    if data['response'] == 'accept':
        Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
        friend_request.delete()
        return Response({'success': 'Friend request accepted'}, status=status.HTTP_200_OK)
    
    friend_request.delete()
    return Response({'success': 'Friend request rejected'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_friends(request):
    user = request.user
    friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
    friends = [fs.user1 if fs.user2 == user else fs.user2 for fs in friendships]
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_pending_requests(request):
    user = request.user
    requests = FriendRequest.objects.filter(to_user=user)
    serializer = FriendRequestSerializer(requests, many=True)
    return Response(serializer.data)

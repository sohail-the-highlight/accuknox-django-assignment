from django.urls import path
from .views import search_users, send_friend_request, respond_friend_request, list_friends, list_pending_requests, UserSignupView, UserLoginView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', search_users, name='search'),
    path('friend-request/send/', send_friend_request, name='send_friend_request'),
    path('friend-request/respond/', respond_friend_request, name='respond_friend_request'),
    path('friends/', list_friends, name='friends_list'),
    path('friend-requests/pending/', list_pending_requests, name='pending_friend_requests'),
]

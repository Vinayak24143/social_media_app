from django.urls import include, path
from .views import UserViewSet,UserDetailAPI,RegisterUserAPIView,UserFriendAPIView, FriendRequestAPIView,acceptFriendRequest

urlpatterns = [
    path('users', view=UserViewSet.as_view({'get':'list'}),name='users'),
    path("get-details",UserDetailAPI.as_view()),
    path('register',RegisterUserAPIView.as_view()),
    path('friends',UserFriendAPIView.as_view(),),
    path('friend-requests',FriendRequestAPIView.as_view()),
    path('friend-request/<id>/accept',acceptFriendRequest)
]

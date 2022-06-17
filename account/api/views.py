from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import FriendRequestSerializer, UserSerializer,RegisterSerializer
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from ..models import FriendRequest

User=get_user_model()

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.exclude(is_staff=True,is_superuser=True).order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailAPI(APIView):
  permission_classes = (permissions.IsAuthenticated,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

class UserFriendAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        self.queryset=request.user.friends.all()
        return super().get(request, *args, **kwargs)

class FriendRequestAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self,request,*args,**kwargs):
       
       serializer = FriendRequestSerializer(FriendRequest.objects.filter(to_user=request.user),many=True)
       return Response(serializer.data)
    def post(self,request,*args,**kwargs):
        data=request.data
        data['from_user']=request.user.id
        serializer = FriendRequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated,])
def acceptFriendRequest(request,id):
    user=request.user
    try:
        fr = FriendRequest.objects.get(id=id, to_user=user)
    except FriendRequest.DoesNotExist:
        return Response({"error":"invalid friend request"},status=status.HTTP_404_NOT_FOUND)
    user.friends.add(fr.from_user)
    fr.from_user.friends.add(user)
    fr.delete()
    return Response({"message":"Friend request accept successfully"}, status=status.HTTP_200_OK)
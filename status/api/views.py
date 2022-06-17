from .serializers import StatusSerializer
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..models import Status

class StatusListView(generics.ListAPIView):
    queryset = Status.objects.all().order_by('-created_at')
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_status(request):
    data=request.data
    data['user']=request.user.id
    serializer=StatusSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.create(serializer.validated_data)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

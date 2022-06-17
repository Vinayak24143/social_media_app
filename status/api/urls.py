from django.urls import include, path
from .views import StatusListView,   create_status

urlpatterns = [
    path("create",create_status),
    path("",StatusListView.as_view()),
]

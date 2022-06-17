from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()
class Status(models.Model):
    content = models.CharField(max_length=255)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
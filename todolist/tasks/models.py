from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class tasks(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="todos")
    title=models.CharField(max_length=50)
    description=models.TextField()
    completed=models.BooleanField(default=False)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + "\n" + self.description

class CapturedPicture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='.')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Picture for {self.user.username} at {self.timestamp}"

class WeightHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    #timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weight for {self.user.username}"      

class WeightPicture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imageId = models.ForeignKey(CapturedPicture, on_delete=models.CASCADE)
    weightId = models.ForeignKey(WeightHistory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Detail for image {self.imageId}  {self.weightId}"          
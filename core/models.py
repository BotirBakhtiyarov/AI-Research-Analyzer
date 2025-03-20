from django.db import models
from django.contrib.auth.models import User

class Research(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='core/')
    title = models.CharField(max_length=255, blank=True)
    date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    keywords = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    ai_probability = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
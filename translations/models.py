from django.db import models
from django.contrib.auth.models import User

class Translation(models.Model):
    msgid = models.TextField()
    language = models.CharField(max_length=10, default='it')
    msgstr = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_translations')
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='approved_translations')

    class Meta:
        unique_together = ('msgid', 'language')

class Vote(models.Model):
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=[(1, 'Up'), (-1, 'Down')])

    class Meta:
        unique_together = ('translation', 'user')

class Comment(models.Model):
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    VIDEO_TYPE_CHOICES = (
        ('video', 'Video'),
        ('shorts', 'Shorts'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    task_id = models.CharField(max_length=100, unique=True)
    video_type = models.CharField(max_length=10, choices=VIDEO_TYPE_CHOICES)
    video_link = models.URLField()
    title = models.CharField(max_length=255)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    fail_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_id

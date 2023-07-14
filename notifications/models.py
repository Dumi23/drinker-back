from django.db import models

# Create your models here.
class Notification(models.Model):
    sender = models.CharField(max_length=55)
    text = models.TextField(max_length=200)
    url = models.URLField()
    recieved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.text)
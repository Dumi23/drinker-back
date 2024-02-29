import threading 
from django.db import transaction
from ..club.models import Place, Event
from .models import Notification
from datetime import datetime


class NotificationThread(threading.Thread):
    obj: Place
    event: Event
    text: str
    url: str

    def run(self, obj, event, text, url):
        batch_send_club_notifications_for_event_creation(self.obj, self.event, self.text, self.url)
                
    


def batch_send_club_notifications_for_event_creation(obj: Place, event: Event, text, url):
    followers = obj.followers
    with transaction.atomic():
        for follower in followers:
            notification = Notification.objects.create(sender=obj.name, text=f"Created a new Event: {event.name}", url="https://google.com", recieved_at=datetime.now())
            follower.notifications.add(notification)
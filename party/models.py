from django.db import models
from drinker.utils import get_hashid

# Create your models here.
class HouseParty(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey("user.User", related_name="created_by", null=True, blank=True, on_delete=models.CASCADE)
    invites = models.ManyToManyField("user.User", blank=True)
    start_time_and_date = models.DateTimeField(null=True)
    slug = models.CharField(max_length=255, unique=True, null=True, blank=True, editable=False)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.name + self.created_by.email
    
    def save(self, *args, **kwargs):
        get_hashid(self, Type=HouseParty, *args, **kwargs)
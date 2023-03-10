from django.db import models
from club.models import club
# Create your models here.


class event(models.Model):

    # class Meta:
    #     app_label = 'events'

    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    registration_link = models.URLField(max_length=200, null=True)
    type = models.CharField(max_length=20, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    max_attendance = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    club = models.ForeignKey(to=club, on_delete=models.DO_NOTHING)
    poster_path = models.URLField(max_length=500)


class event_attendance(models.Model):

    # class Meta:
    #     app_label = 'events'

    registered_at = models.DateTimeField()
    student_id = models.IntegerField()
    event = models.ForeignKey(to=event, on_delete=models.DO_NOTHING)

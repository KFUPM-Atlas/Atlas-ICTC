from django.db import models

# Create your models here.


class event(models.Model):
    event_id = models.AutoField(max_length=10, primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    registration_link = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    start_datetime = models.DateTimeField()
    end_datatime = models.DateTimeField()
    max_attendance = models.IntegerField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    # club_id = models.ForeignKey(to='backend.club', on_delete=models.DO_NOTHING)
    poster_path = models.CharField(max_length=500)


class event_attendance(models.Model):
    registered_at = models.DateTimeField()
    student_id = models.IntegerField(max_length=10)
    event_id = models.ForeignKey(to='event', on_delete=models.DO_NOTHING)

from django.db import models

# Create your models here.
class club_officer(models.Model):

    class Meta:
        app_label = 'auth'

    club_officer_id = models.IntegerField(primary_key=True)
    president_id = models.IntegerField()


class supervisor(models.Model):

    class Meta:
        app_label = 'auth'
    supervisor_id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=100)
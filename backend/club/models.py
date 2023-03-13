from django.db import models
from auth_users.models import supervisor,club_officer


# Create your models here.
class club_management(models.Model):

    class Meta:
        app_label = 'club'

    assignment_date = models.DateField()
    club_officer = models.ForeignKey(to=club_officer, on_delete=models.DO_NOTHING)
    club = models.ForeignKey(to='club', on_delete=models.DO_NOTHING)


class club(models.Model):

    class Meta:
        app_label = 'club'

    club_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    headquarter = models.CharField(max_length=50)
    supervisor = models.ForeignKey(supervisor, on_delete=models.DO_NOTHING, primary_key=False)
    logo_path = models.CharField(max_length=500)
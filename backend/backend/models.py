from django.db import models
from auth_users.models import supervisor, club_officer
from club.models import club

"""
This file will contain all the data models which will be used in this application

Models:
1- Event            -> events app
2- Request          -> requests app
3- Club Management  -> club app 
4- Club Officer     -> auth_users app
5- Club             -> club app
6- Event Attendance -> events app

"""

class request(models.Model):
    # Request Status Possible Values
    NEW = 'new'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    status_choices = [(NEW, 'new'),
        (APPROVED, 'approved'),
        (REJECTED, 'rejected')]

    # Request Type Possible Values
    CUSTODY = 'custody'
    SETTLEMENT = 'settlement'
    BUDGET = 'budget'
    EVENT = 'event'

    type_choices = [(CUSTODY, 'custody'),
        (SETTLEMENT, 'settlement'),
        (BUDGET, 'budget'),
        (EVENT, 'event')]

    request_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    type = models.CharField(choices=type_choices,max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=status_choices, default=NEW,max_length=10)
    updated_at = models.DateTimeField()
    club = models.ForeignKey(to=club, on_delete=models.DO_NOTHING, primary_key=False)
    supervisor = models.ForeignKey(to=supervisor, on_delete=models.DO_NOTHING, primary_key=False)
    club_officer = models.ForeignKey(to=club_officer, on_delete=models.DO_NOTHING, primary_key=False)
    attachment_path = models.CharField(max_length=500)











from django.db import models

"""
This file will contain all the data models which will be used in this application

Models:
1- Event
2- Request
3- Club Management
4- Club Officer
5- Club
6- Event Attendance

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

    request_id = models.AutoField(max_length=10)
    title = models.CharField(max_length=50)
    type = models.CharField(choices=type_choices,max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=status_choices, default=NEW,max_length=10)
    updated_at = models.DateTimeField()
    club_id = models.ForeignKey(to='club')
    supervisor_id = models.IntegerField(max_length=10)
    club_officer_id = models.ForeignKey(to='club_officer')
    attachment_path = models.CharField(max_length=500)


class club_management(models.Model):
    assignment_date = models.DateField()
    club_officer_id = models.ForeignKey(to='club_officer')
    club_id = models.ForeignKey(to='club')


class club_officer(models.Model):
    club_officer_id = models.IntegerField(max_length=10, primary_key=True)
    president_id = models.IntegerField(max_length=10)


class club(models.Model):
    club_id = models.AutoField(max_length=10)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    headquarter = models.CharField(max_length=50)
    supervisor_id = models.IntegerField(max_length=10)
    logo_path = models.CharField(max_length=500)





from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re, datetime


class UsersManager(models.Manager):
    def login(self, **kwargs):
        print "Calling login function"

        error_list = []

        if len(kwargs['post']['username']) == 0:
            error_list.append('username_blank')
            return (True, error_list)

        try:
            user = User.objects.get(username=kwargs['post']['username'])
            print "Try successful"
        except:
            error_list.append('exist')
            print "Excepted"
            return (True, error_list)

        if user.password == kwargs['post']['password']:
            print "passwords match"
            user = {
                'name':user.name,
                'username':user.username,
                'email':user.email,
                'id':user.id
                }

            return(False, user)
        else:
            if len(kwargs['post']['password']) == 0:
                error_list.append('password_blank')
                print "Password blank"
                return (True, error_list)
            else:
                print "Password contains characters"
                error_list.append('mismatch')
                print "REturning True, error_list"
                return(True, error_list)


    def register(self, **kwargs):

        user = {
            'name':kwargs['post']['name'],
            'username':kwargs['post']['username'],
            'email':kwargs['post']['email'],
            'password':kwargs['post']['password'],
            'confirm_pw':kwargs['post']['confirm_pw']
        }

        error_list = []

        if len(user['password']) > 7:
            print "Password length: check"
        else:
            error_list.append('password_length')

        if len(user['name']) > 2:
            print "Username length satisfied"
        else:
            error_list.append('name_short')

        if len(user['username']) > 2:
            print "Username length satisfied"
        else:
            error_list.append('username_short')

        if user['password'] == user['confirm_pw']:
            print "Passwords match"
        else:
            error_list.append('mismatch')

        EMAIL_REGEX = re.compile(r'^[\w\.+_-]+@[\w\._-]+\.[\w]*$')
        if EMAIL_REGEX.match(user['email']):
            EMAIL_REGEX.match(user['email'])
            print "Email successfully validated"

        else:
            error_list.append("email_invalid")

        try:
            user = User.objects.get(email=user['email'])
            error_list.append("exists")
            print "exists already"
        except:
            new_user = User(name=user['name'], username=user['username'], email=user['email'], password=user['password'])

            if error_list:
                print "Returned errors"
                return (True, error_list)
            else:
                print "No errors!"
                new_user.save()
                return (False, "No errors! Continuing on")

    def create(self, **kwargs):
        print "Reached create function in User manager"
        print kwargs
        error_list = []
        travel_plan = Travel(destination=kwargs['post']['destination'], description=kwargs['post']['description'], start_date=kwargs['post']['start_date'], end_date=kwargs['post']['end_date'])
        if travel_plan.start_date < travel_plan.created_at:
            error_list.append('start_before_today')
            return (False, error_list)
        if travel_plan.start_date > travel_plan.end_date:
            error_list.append("start_after_end")
            return (False, error_list)
        else:
            travel_plan.save()
            return (True, "No errors")





def validate_date_after_today(start_date, created_at):
    if start_date < created_at:
        raise ValidationError(
            _('%(start_date)s is not a future date'),
            params = {
            'start_date': start_date
            })

def validate_date_after_start(start_date, end_date):
    if start_date >= end_date:
        raise ValidationError(
            _('%(start_date)s is after end date'),
            params = {
            'start_date':start_date,
            'end_date':end_date
            }
        )

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class Travel(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateTimeField(validators=[validate_date_after_today])
    description = models.TextField()
    end_date = models.DateTimeField(validators=[validate_date_after_start])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User)
    objects = UsersManager()

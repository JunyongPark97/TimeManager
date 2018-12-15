from datetime import timezone

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from django.db.models.signals import post_save

import user


class User(AbstractUser):
    grade= models.IntegerField(null=True, blank=True)
    writter_id=models.CharField(null=True,max_length=100)



class Timelog(models.Model):# 얘를 상속받을 것
    token=models.CharField(null=True,max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    text = models.CharField(max_length=100)

    class Meta:
        abstract = True # migrate 안하게


class EnterTimelog(Timelog):
    pass


class OutTimelog(Timelog):
    half_day_off = models.CharField(blank=True, null=True, max_length=100)#반차 기록
    breaktime = models.IntegerField(default=0)


class EnterAtHomeTimelog(Timelog):
    pass


class OutAtHomeTimelog(Timelog):
    breaktime = models.IntegerField(default=0)


class UpdateRequest(models.Model):
    sender = models.ForeignKey(User, related_name='senderRequestinfo', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiverRequestinfo', on_delete=models.CASCADE)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # time_log = GenericForeignKey('content_type', 'object_id')
    update = models.DateTimeField()
    # status = models.IntegerField(default=0, choices=((0,'대기중'),(1,'수락'),(2,'거절')))
    reason = models.TextField(null=True)
    breaktime = models.IntegerField()
    # pub_date = models.DateTimeField()
    #
    # class Meta:
    #     ordering = ['-pub_date']


# def create_entry(sender, **kwargs):
#     if 'created' in kwargs:
#         if kwargs['created']:
#             instance = kwargs['instance']
#             ctype = ContentType.objects.get_for_model(instance)
#             entry = Entry.objects.get_or_create(content_type=ctype,
#                                                 object_id=instance.id,
#                                                 pub_date=instance.pub_date)
#
#
# post_save.connect(create_entry, sender=Post)
# post_save.connect(create_entry, sender=Url)
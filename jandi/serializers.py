import re

from django.http import HttpResponse
from rest_framework import serializers, status
from rest_framework.response import Response

from user.models import EnterTimelog, User, OutTimelog, EnterAtHomeTimelog, OutAtHomeTimelog


class JandiSerializer(serializers.Serializer):
    token=serializers.CharField()
    teamName=serializers.CharField()
    roomName=serializers.CharField()
    writerName=serializers.CharField()
    text=serializers.CharField()
    keyword=serializers.CharField()
    createdAt=serializers.DateTimeField()


class JandiEnterSerializer(JandiSerializer):

    def create(self, validated_data):
        user = User.objects.get(writter_id=validated_data['writerName'])
        print(validated_data)
        return EnterTimelog.objects.create(
            user=user,
            text=validated_data['text'],
            created_at=validated_data['createdAt']
        )


class JandiOutSerializer(JandiSerializer):

    def create(self, validated_data):
        user = User.objects.get(writter_id=validated_data['writerName'])
        print(validated_data)
        text = validated_data['text']
        num = re.findall("\d+", text)

        if len(num) == 1 and '오후반차' in text:

            return OutTimelog.objects.create(
                user=user,
                created_at=validated_data['createdAt'],
                text=text,
                breaktime=int(num[0]),
                half_day_off='오후반차'
            )

        elif len(num) == 1 and not '오후반차' in text:
            return OutTimelog.objects.create(
                user=user,
                created_at=validated_data['createdAt'],
                text=text,
                breaktime=int(num[0])
            )

        elif not len(num) == 1 and '오후반차' in text:
            return OutTimelog.objects.create(
                user=user,
                created_at=validated_data['createdAt'],
                text=text,
                half_day_off='오후반차'
            )

        else:
            return HttpResponse('Wrong input')


class JandiEnterHomeSerializer(JandiSerializer):

    def create(self, validated_data):
        user = User.objects.get(writter_id=validated_data['writerName'])
        print(validated_data)
        return EnterAtHomeTimelog.objects.create(
            user=user,
            text=validated_data['text'],
            created_at=validated_data['createdAt']
        )


class JandiOutHomeSerializer(JandiSerializer):

    def create(self, validated_data):
        user = User.objects.get(writter_id=validated_data['writerName'])
        print(validated_data)
        text = validated_data['text']
        num = re.findall("\d+", text)

        if num:
            return OutAtHomeTimelog.objects.create(
                user=user,
                created_at=validated_data['createdAt'],
                text=text,
                breaktime=int(num[0])
            )

        else:
            return OutAtHomeTimelog.objects.create(
                user=user,
                created_at=validated_data['createdAt'],
                text=text,
            )
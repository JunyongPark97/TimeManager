from rest_framework import serializers

from user.models import EnterTimelog, User


class JandiSerializer(serializers.Serializer):
    token=serializers.CharField()
    teamName=serializers.CharField()
    roomName=serializers.CharField()
    writerName=serializers.CharField()
    text=serializers.CharField()
    keyword=serializers.CharField()
    createdAt=serializers.DateTimeField()

    def create(self, validated_data):
        user = User.objects.get(writter_id=validated_data['writerName'])
        return EnterTimelog.objects.create(
            user=user,
            text=validated_data['text'],
            created_at=validated_data['createdAt']
        )


    # body = serializers.CharField()
    # connectColor = serializers.CharField(required=False)
    # title = serializers.CharField(required=False)
    # connectInfo = serializers.JSONField(required=False)

# class Jandi
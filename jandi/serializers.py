from rest_framework import serializers


class JandiSerializer(serializers.Serializer):
    token=serializers.CharField()
    teamName=serializers.CharField()
    roomName=serializers.CharField()
    writerName=serializers.CharField()
    text=serializers.CharField()
    keyword=serializers.CharField()
    createdAt=serializers.DateTimeField()
    #
    # body = serializers.CharField()
    # connectColor = serializers.CharField(required=False)
    # title = serializers.CharField(required=False)
    # connectInfo = serializers.JSONField(required=False)

# class Jandi
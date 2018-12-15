import re

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from jandi.serializers import JandiEnterSerializer, JandiOutSerializer, JandiEnterHomeSerializer, JandiOutHomeSerializer
from user.models import EnterTimelog, OutTimelog, EnterAtHomeTimelog, OutAtHomeTimelog


class JandiInputAPIView(APIView):
    serializer_class = None

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})


class JandiEnterAPIView(JandiInputAPIView):
    serializer_class = JandiEnterSerializer


class JandiOutAPIView(JandiInputAPIView):
    serializer_class = JandiOutSerializer


class JandiEnterHomeAPIView(JandiInputAPIView):
    serializer_class = JandiEnterHomeSerializer


class JandiOutHomeAPIView(JandiInputAPIView):
    serializer_class = JandiOutHomeSerializer


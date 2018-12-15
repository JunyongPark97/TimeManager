import re

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from jandi.serializers import JandiEnterSerializer, JandiOutSerializer, JandiEnterHomeSerializer
from user.models import EnterTimelog, OutTimelog, EnterAtHomeTimelog, OutAtHomeTimelog


class JandiInputAPIView(APIView):
    serializer_class = None

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})


class JandiEnterAPIView(JandiInputAPIView):
    super().serializer_class = JandiEnterSerializer


class JandiOutAPIView(APIView):
    serializer_class = JandiOutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})


class JandiEnterHomeAPIView(APIView):
    serializer_class = JandiEnterHomeSerializer

    def post(self, request):
        try:
            data=request.data
            text = data['text']
            if '정정' in text:
                raise Exception('Wrong input')
            else:
                EnterAtHomeTimelog.objects.create(user=data['writerName'],
                                                  created_at=data['createdAt'],
                                                  text=data['text'])
                print('inelse')
                return HttpResponse(status=201)

        except Exception:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)


class JandiOutHomeAPIView(APIView):
    # serializer_class = JandiSerializer

    def post(self, request):
        try:
            data=request.data
            text=data['text']
            num=re.findall("\d+", text)
            if len(num)==1:
                OutAtHomeTimelog.objects.create(
                    user=data['writerName'],
                    created_at=data['createdAt'],
                    text=data['text'],
                    breaktime=num)
                print(data)
                return HttpResponse(status=201)

            elif '정정' in text:
                raise Exception('Wrong input')

        except Exception:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

import re

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from jandi.serializers import JandiSerializer
from user.models import EnterTimelog, OutTimelog, EnterAtHomeTimelog, OutAtHomeTimelog


class JandiEnterAPIView(APIView):
    # serializer_class = JandiSerializer

    def post(self, request):
        try:
            data = request.data
            print(data)
            # text = data['text']
            # if '정정' in text:
            #     raise Exception('Wrong input')
            # else:
            #     EnterTimelog.objects.create(user=data['writerName'],
            #                                 created_at=data['createdAt'],
            #                                 text=data['text'])
            #     return HttpResponse(status=201)
            #
            #     print('intty')

        except Exception:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)


class JandiOutAPIView(APIView):
    # serializer_class = JandiSerializer

    def post(self, request):
        try:
            data = request.data
            text=data['text']
            num = re.findall("\d+",text)

            if len(num)==1 and '오후반차' in text:
                OutTimelog.objects.create(
                    user=data['writerName'],
                    created_at=data['createdAt'],
                    text=data['text'],
                    breaktime=num,
                    half_day_off='오후반차')
                print('00')
                return HttpResponse(status=201)

            elif len(num)==1 and not '오후반차' in text:
                OutTimelog.objects.create(
                    user=data['writerName'],
                    created_at=data['createdAt'],
                    text=data['text'],
                    breaktime=num)
                print('--')
                return HttpResponse(status=201)

            elif '정정' in text:
                raise Exception('Wrong input')

        except Exception:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

class JandiEnterHomeAPIView(APIView):
    # serializer_class = JandiSerializer

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

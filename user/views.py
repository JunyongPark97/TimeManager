from itertools import tee, chain
from operator import attrgetter
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from collections import Counter
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from user.models import *
from user.permissions import GradePermission
from user.serializers import UserSerializer, EnterTimelogSerializer, OutTimelogSerializer, \
    EnterAtHomeTimelogSerializer, OutAtHomeTimelogSerializer, \
    EnterUpdateRequestSerializer, EnterUpdateRequestEditSerializer, UserTimeSerializer


class TimelogReadOnlyViewSet(mixins.CreateModelMixin,# 모델 뷰셋 인데 따로 기능 수정해야 해서 선언
                             mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             GenericViewSet):

    def get_queryset(self): #원래 있는 함수인데 덮어쓰기함
        if self.action == 'list':# 시리얼라이저에서 지원해주는 거 : action이 list 조회일때
            user = self.request.user
            return self.queryset.filter(Q(user__grade__gt=user.grade)|Q(user=user))# or 쓰려면 Q써야함
        return self.queryset


class EnterTimelogViewSet(TimelogReadOnlyViewSet):
    queryset = EnterTimelog.objects.all()
    permission_classes = (IsAuthenticated, GradePermission)
    serializer_class = EnterTimelogSerializer

class OutTimelogViewSet(TimelogReadOnlyViewSet):
    queryset = OutTimelog.objects.all()
    permission_classes = (IsAuthenticated, GradePermission)
    serializer_class = OutTimelogSerializer

class EnterAtHomeTimelogViewSet(TimelogReadOnlyViewSet):
    queryset = EnterAtHomeTimelog.objects.all()
    permission_classes = (IsAuthenticated, GradePermission)
    serializer_class = EnterAtHomeTimelogSerializer

class OutAtHomeTimelogViewSet(TimelogReadOnlyViewSet):
    queryset = OutAtHomeTimelog.objects.all()
    permission_classes = (IsAuthenticated, GradePermission)
    serializer_class = OutAtHomeTimelogSerializer


class TimelogList(APIView):
    """
    본인의 Timelog list를 보여주는 클래스입니다.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home/timelog_list.html'
    permission_classes = (IsAuthenticated, GradePermission)

    def get(self, request):
        user=request.user
        queryset = EnterTimelog.objects.filter(user=user)#쿼리셋합쳐서 순서대로 나열하기
        queryset2 = OutTimelog.objects.filter(user=user)
        queryset3 = EnterAtHomeTimelog.objects.filter(user=user)
        queryset4 = OutAtHomeTimelog.objects.filter(user=user)
        query=sorted(
            chain(queryset, queryset2, queryset3, queryset4),
            key=attrgetter('created_at'),
            reverse=True)
        return Response({'timelogs': query})


class TimelogEditRequest(APIView):
    """
    수정사항 입력시 사용합니다.
    요청이 post로 들어올 시, UpdateRequest라는 임시 모델에 시간을 저장합니다.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home/timelog_edit.html'

    def get(self, request, pk):
        serializer = EnterUpdateRequestSerializer()
        return Response({'serializer': serializer})

    def post(self, request, pk):
        serializer = EnterUpdateRequestSerializer(data = request.data, context={'origin': pk, 'request': request})
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('user:timelog_list')


class EditTimelog(APIView):
    # serializer_class = EnterUpdateRequestEditSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home/request_list_to_edit.html'

    def get(self, request):
        user=request.user
        update_request = UpdateRequest.objects.filter(receiver=user)
        return Response({'update_request': update_request})

    # 초이스 할 수 있는 폼 & 수락, 거절에 따른 DB업데이트
def edittimelogconfirm(request, pk1, pk2):
        update_request = get_object_or_404(UpdateRequest, pk=pk1)
        if update_request.receiver == request.user:
            if pk2 == 1:  # 수락
                enter_timelog = update_request.origin
                enter_timelog.created_at = update_request.update
                enter_timelog.save()
                update_request.status=1
                update_request.save()
            else:
                update_request.status = 2
                update_request.save()
        return redirect(reverse('user:edit_timelog'))


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'registration/logged_out.html')
    return HttpResponse('ssewf')


class MakeGraph(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home/timedata.html'

    def get(self, request):
        user=request.user
        a=latestTimelogs(user)
        return Response({'a':a})

def latestTimelogs(user):
    entertimelog=EnterTimelog.objects.filter(user=user).latest('created_at').created_at
    outtimelog=OutTimelog.objects.filter(user=user).latest('created_at').created_at
    enterhometimelog=EnterAtHomeTimelog.objects.filter(user=user).latest('created_at').created_at
    outhometimelog=OutAtHomeTimelog.objects.filter(user=user).latest('created_at').created_at
    normaltime=calculateTime(entertimelog,outtimelog)
    hometime=calculateTime(enterhometimelog,outhometimelog)
    weektime=Counter(normaltime)+Counter(hometime)
    return weektime


def calculateTime(timeA,timeB):#출근,퇴근 순서대로 입력받아 시간 계산
    week={}
    if timeA < timeB:
        week[timeA.weekday()]=convertTimetoNum(timeB-timeA)
        return week
    week[timeA.timeA.weekday()]=0
    return week

def convertTimetoNum(time):
    roughtime=str(time).split(':')
    hour=roughtime[0]
    minute=roughtime[1]
    totaltime=round(float(hour)+float(int(minute)/60),2)
    return totaltime


def change_password(request):
    if request.method =='POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
            return redirect('user:gotohome')
        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html',{'form':form})
import copy
import io
from itertools import tee

from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
import datetime
import  time
from datetime import timedelta
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

# from user.forms import RequestForm1, RequestForm2, RequestForm3
from user.models import *
from user.permissions import GradePermission
from user.serializers import UserSerializer, EnterTimelogSerializer, OutTimelogSerializer, \
    EnterAtHomeTimelogSerializer, OutAtHomeTimelogSerializer, UpdateRequestSerializer


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


# class UpdateRequestEnterViewSet(ModelViewSet):
#     queryset = UpdateRequest.objects.all()## 나중에 client에서 url호출시 pk받기
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UpdateRequestEnterSerializer

class UpdateRequestOutViewSet(ModelViewSet):
    queryset = UpdateRequest.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateRequestSerializer


class TimelogList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home/timelog_list.html'
    permission_classes = (IsAuthenticated, GradePermission)

    def get(self, request):
        user=request.user
        queryset = EnterTimelog.objects.filter(user=user)#쿼리셋합쳐서 순서대로 나열하기
        return Response({'timelogs': queryset})

class TimelogEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'timelog_edit.html'

    def get(self, request, pk):
        # timelog = EnterTimelog.objects
        serializer = EnterTimelogSerializer
        return Response({'serializer': serializer})

    def post(self, request, pk):
        user=request.user
        timelog = EnterTimelog.objects.get(pk=pk)
        serializer = UpdateRequestSerializer(timelog, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'timelogs': timelog})
        serializer.save()
        return redirect('user:timelog_list')





def update_request(request):
    if request.user.is_authenticated:
        user = request.user  # user는 에초에 init에 정의되어있음, User모델 추가함으로써 자동으로 해당 모델 참조.
        last_week = datetime.datetime.now() - datetime.timedelta(days=7)
        timelogs = EnterTimelog.objects.filter(user=user,
                                          created_at__gt=last_week)  # 자기자신의 정보 앞의 user는 foreignkey로 user_id와 같음

    return render(request, 'home/update_req.html',context={'timelogs':timelogs})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'registration/logged_out.html')
    return HttpResponse('ssewf')




# #각 유저별로 출퇴근 데이터를 얻어옵니다.
# class ImportCSVView(APIView):
#     # serializer_class = CSVSerializer # 받아온 값 저장
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = serializer.validated_data
#         csv_file = data['csv']
#         import csv
#         decoded_file = csv_file.read().decode('utf-8')
#         io_string = io.StringIO(decoded_file)
#         reader = csv.reader(io_string, delimiter=',')
#         next(reader)#첫줄 띄기
#         for line in reader:
#             user = User.objects.get(pk=line[0])
#             text=line[1].strip()
#             recent_timelog = user.timelog_set.all().order_by('-created_at').first()
#             print(line[3])
#             try:
#                 if text == '/출근':
#                     temptime = datetime.datetime.strptime(line[3], "%Y-%m-%d %H:%M")  # 서버 연동시 형식 맞춰야함
#
#                     if not recent_timelog:#이전 자료가 아무것도 없거나
#                         Timelog.objects.create(user=user, text=text, keyword=1, created_at=temptime,
#                         half_day_off='오전 반차'if temptime.time()>datetime.time(12) else None)# 퇴근-출근 쌍 맞추기
#                     elif recent_timelog.keyword in [2,4]:#2 : 퇴근
#                         Timelog.objects.create(user=user, text=text, keyword=1, created_at=temptime,
#                         half_day_off='오전 반차'if temptime.time()>datetime.time(12) else None)
#                     elif recent_timelog.keyword == 1:# 이 전 기록이 출근일 때 퇴근 만들기
#                         Timelog.objects.create(user=user, text='/퇴근', keyword=2, created_at=temptime-timedelta(minutes=5),half_day_off='자동생성')#1분 빼주기
#                         Timelog.objects.create(user=user, text=text, keyword=1, created_at=temptime,
#                         half_day_off='오전 반차'if temptime.time()>datetime.time(12) else None)# 퇴근-출근 쌍 맞추기
#                     elif recent_timelog.keyword == 3:# == 3 이 전 기록이 출근 (재택)
#                         Timelog.objects.create(user=user, text='/퇴근 (재택)', keyword=4, created_at=temptime-timedelta(minutes=5),half_day_off='자동생성')# 얘도
#                         Timelog.objects.create(user=user, text=text, keyword=1, created_at=temptime,
#                         half_day_off='오전 반차'if temptime.time()>datetime.time(12) else None)# 퇴근-출근 쌍 맞추기
#                         # else:
#                         #     Timelog.objects.create(user=user, text=text, keyword=1, created_at=temptime,
#                         #                            half_day_off='오전반차'if temptime.time()>datetime.time(12) else None)
#
#                 elif text == '/출근 (재택)':
#                     temptime = datetime.datetime.strptime(line[3], "%Y-%m-%d %H:%M")  # 서버 연동시 형식 맞춰야함
#
#                     if not recent_timelog or recent_timelog.keyword in [2, 4]:
#                         Timelog.objects.create(user=user, text=text, keyword=3, created_at=temptime)# 퇴근-출근 쌍 맞추기
#                     elif recent_timelog.keyword == 1:
#                         Timelog.objects.create(user=user, text='/퇴근', keyword=2, created_at=temptime-timedelta(minutes=5),half_day_off='자동생성')  # 1분 빼주기
#                         Timelog.objects.create(user=user, text=text, keyword=3, created_at=temptime)
#                     else:
#                         Timelog.objects.create(user=user, text='/퇴근 (재택)', keyword=4, created_at=temptime-timedelta(minutes=5),half_day_off='자동생성')  # 얘도
#                         Timelog.objects.create(user=user, text=text, keyword=3, created_at=temptime)
#
#                 elif text == '/퇴근 (재택)':
#                     temptime = datetime.datetime.strptime(line[3], "%Y-%m-%d %H:%M")  # 서버 연동시 형식 맞춰야함
#                     if not recent_timelog:
#                         Timelog.objects.create(user=user, text=text, keyword=4, created_at=temptime)
#                     elif recent_timelog.keyword == 3:
#                         Timelog.objects.create(user=user, text=text, keyword=4, created_at=temptime)
#
#                 elif text[:3] == '/퇴근' and len(text.split()) == 3: # /퇴근 -2 오후반차
#                     temptime = datetime.datetime.strptime(line[3], "%Y-%m-%d %H:%M")  # 서버 연동시 형식 맞춰야함
#                     if not recent_timelog or recent_timelog.keyword == 1:
#                         breaks=abs(int(text.split()[1]))
#                         Timelog.objects.create(user=user, text=text, keyword=2, breaktime=breaks,created_at=temptime-timedelta(hours=breaks), half_day_off='오후 반차')#휴게시간 빼줌
#                     elif recent_timelog.keyword in [2,4]:# 이전 기록이 /퇴근 또는 /퇴근 (재택) 인 경우 휴게시간+한시간 전 출근 하나 만들고 퇴근 찍음
#                         breaks=abs(int(text.split()[1]))
#                         Timelog.objects.create(user=user, text='/출근', keyword=1,created_at=temptime - timedelta(hours=breaks+1),half_day_off='자동생성')
#                         Timelog.objects.create(user=user, text=text, keyword=2, breaktime=breaks,
#                                                created_at=temptime - timedelta(hours=breaks),
#                                                half_day_off='오후 반차')  # 휴게시간 빼줌
#
#                 elif text[:3] == '/퇴근' and len(text.split()) == 2:
#                     temptime = datetime.datetime.strptime(line[3], "%Y-%m-%d %H:%M")  # 서버 연동시 형식 맞춰야함
#                     if not recent_timelog:
#                         if text.split()[1]=='오후반차':
#                             Timelog.objects.create(user=user, text='/출근', keyword=1, created_at=temptime-timedelta(hours=1))#
#                             Timelog.objects.create(user=user, text=text, keyword=2,
#                                                    created_at=temptime, half_day_off='오후 반차')
#                         else:
#                             breaks = abs(int(text.split()[1]))
#                             Timelog.objects.create(user=user, text='/출근', keyword=1, breaktime=breaks,created_at=temptime-timedelta(hours=(breaks+1)))#
#                             Timelog.objects.create(user=user, text=text, keyword=2, breaktime=breaks,created_at=temptime-timedelta(hours=breaks))# 휴게시간 뺴줌
#                     elif recent_timelog.keyword == 1:# 정상적인 작동
#                         if text.split()[1] == '오후반차':
#                             Timelog.objects.create(user=user, text=text, keyword=2,
#                                                    created_at=temptime, half_day_off='오후 반차')
#                         else:
#                             breaks = abs(int(text.split()[1]))
#                             Timelog.objects.create(user=user, text=text, keyword=2, breaktime=breaks,
#                                                    created_at=temptime - timedelta(hours=breaks))  # 휴게시간 뺴줌
#                     elif recent_timelog.keyword in [2,4]: # 이전 기록이 /퇴근 또는 /퇴근 (재택)
#                         breaks = abs(int(text.split()[1]))
#                         Timelog.objects.create(user=user, text='/출근', keyword=1,
#                                                created_at=temptime - timedelta(hours=breaks + 1), half_day_off='자동생성')
#                         Timelog.objects.create(user=user, text=text, keyword=2, breaktime=breaks,
#                                                created_at=temptime - timedelta(hours=breaks))  # 휴게시간 빼줌
#             except:
#                 pass
#         return Response({})


# grade 정보에 따라 timelog 정보를 보냅니다.
def list(request):
    if request.user.is_authenticated:
        user = request.user # user는 에초에 init에 정의되어있음, User모델 추가함으로써 자동으로 해당 모델 참조.
        last_week = datetime.datetime.now() - datetime.timedelta(days=7)
        timelogs = Timelog.objects.filter(user=user, created_at__gt=last_week)# 자기자신의 정보 앞의 user는 foreignkey로 user_id와 같음
        if user.grade == 1: #Clevel  2,3
            timelogs_3 = Timelog.objects.filter(user__grade=3, created_at__gt=last_week) #grade3인 유저의 정보
            timelogs_2 = Timelog.objects.filter(user__grade=2, created_at__gt=last_week) #grade2인 유저의 정보
            return render(request, 'home/home.html', context={'timelogs': timelogs,
                                                              'timelogs_2':timelogs_2,
                                                              'timelogs_3': timelogs_3})
        elif user.grade == 2: #leader 2
            timelogs_3 = Timelog.objects.filter(user__grade=3, created_at__gt=last_week) #grade3인 유저의 정보
            return render(request, 'home/home.html', context={'timelogs': timelogs,
                                                              'timelogs_2': None,
                                                              'timelogs_3': timelogs_3})
        else:
            return render(request, 'home/home.html', context={'timelogs': timelogs,
                                                              'timelogs_2':None,
                                                              'timelogs_3':None})
    else:
        return render (request, 'home/home.html')

# @login_required()
# # 변경사항 입력하는 뷰
# def request_view(request,pk):#여기서 pk는 수정 누를때(timelog.pk) pk(수정 누르는 해당 time table의 id) 아 그리고 헷갈리는데
#     #request에는 userid(user), breaktime, update, receiver가 들어있음( 우리가 입력해서 보냈던 정보가 이미 들어있음)
#
#     if request.method == "GET": # request가 GET이면 RequestForm을 실행 및 보여주고,
#         if request.user.grade == 1:
#             forsdiv = RequestForm1
#         elif request.user.grade == 2:
#             forsdiv = RequestForm2
#         else:
#             forsdiv = RequestForm3
#         form = forsdiv()
#         return render(request, 'home/request.html', context={'form': form})
#
#     elif request.method == "POST":
#         if request.user.grade == 1:
#             form = RequestForm1(request.POST)
#         elif request.user.grade == 2:
#             form = RequestForm2(request.POST)
#         else:
#             form = RequestForm3(request.POST)
#
#         if form.is_valid():
#             request_info = form.save(commit=False)
#             request_info.sender = request.user
#             request_info.timelog = Timelog.objects.get(pk=pk)
#             request_info.save()# 이제 이 값은 db에 저장되고, 나중에 grade 별로 RequestInfo.objects.get() 다르게 해서 보여주면 됨.
#             context = {'time_before':request_info.timelog.created_at,'time_edit':request_info.update}
#             return render(request, 'home/request_done.html', context)
#     return render(request, 'home/home.html')

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


def gotohome(request):
    return render(request, 'registration/change_password_done1.html')

@login_required()
def requestlist(request): # url 줄 때 로그인 한 User id 정보를 id에 담아서 보낼 예정
    if request.user.is_authenticated:
        request_list = UpdateRequest.objects.filter(receiver=request.user)#filter는 쿼리셋 반환 for문 돌려서 인스턴스 받을 수 있음
        #get()의 경우 인스턴스 (객체) 반환해서 get().name 이렇게 바로 참조할 수 있음
        #여기서 나오는 sender는 RequestInfo의 sender인자이 인자는 User모델 외래키. 즉 sender_id= User 테이블의 고유 id가 저장되어있음.
        # 이 값이 인자로 받은 로그인한 유저의 id인 경우
        context = {
            'request_list':request_list
        }
        return render(request, 'home/edit_request.html', context)
    # elif request.method == 'GET':
    #     return  HttpResponse('get')##수정 필요!! try


# 초이스 할 수 있는 폼 & 수락, 거절에 따른 DB업데이트
def editrequest(request,pk1,pk2):
    info = UpdateRequest.objects.get(pk=pk1)
    if info.receiver == request.user:
        if pk2==1:#수락
            info.status = 1  # status에 1 값 넣어두고 저장 -> 템플릿에서 해당 목록 보일 때에는 status=0일때만 보이게 함.
            info.save()
            timelog = info.timelog ## RequestInfo 의 timelog에 접근
            timelog.created_at = info.update # 해당 timelogdml created_at 을 update값으로 바꿈
            if timelog.created_at.time() < datetime.time(12):
                timelog.half_day_off=None
            timelog.save()
        else:
            info.status = 2
            info.save()
    return redirect(reverse('user:requestlist'))

# @login_required()
def graph(request): # 그래프를 그리기 위한 데이터를 뽑습니다.
    if request.method=="GET":
        if request.user.is_authenticated:
            user = request.user
            users2=User.objects.filter(grade=2)
            users3=User.objects.filter(grade=3)
            grade2data={}
            grade3data={}
            owndata = Timelog.objects.filter(#created_at__week_day__lte=datetime.datetime.now().weekday(),
                                             created_at__gt=datetime.datetime.now()-datetime.timedelta(days=8),
                                              user=user).order_by('created_at')
            own = get_graph(owndata)

            if user.grade==1:
                for user2 in users2:
                    queryset2 = Timelog.objects.filter(#created_at__week_day__lte=datetime.datetime.now().weekday(),
                                                       created_at__gt=datetime.datetime.now() - datetime.timedelta(days=8),
                                                       user=user2).order_by('created_at')
                    grade2data[user2] = get_graph(queryset2)
                for user3 in users3:
                    queryset3 = Timelog.objects.filter(#created_at__week_day__lte=datetime.datetime.now().weekday(),
                                                       created_at__gt=datetime.datetime.now() - datetime.timedelta(days=8),
                                                       user=user3).order_by('created_at')
                    grade3data[user3] = get_graph(queryset3)
                return render(request, 'home/graph.html', context={'own':own,'grade2data':grade2data,'grade3data':grade3data})

            elif user.grade==2:
                for user3 in users3:
                    queryset3 = Timelog.objects.filter(#created_at__week_day__lte=datetime.datetime.now().weekday(), -> 일주일 데이터만 보여줌.
                                                       created_at__gt=datetime.datetime.now() - datetime.timedelta(days=8),
                                                       user=user3).order_by('created_at')
                    grade3data[user3] = get_graph(queryset3)
                return render(request,'home/graph.html',context={'own':own,'grade2data':None,'grade3data':grade3data})

            else:
                return render(request,'home/graph.html',context={'own':own,'grade2data':None,'grade3data':grade3data})
        else:
            return render(request,'registration/base.html')
    else:
        return render(request, 'registration/base.html')


def get_graph(queryset):  # 그래프를 그리기 위한 함수.
        work_times = {}
        iterator = queryset.iterator()
        for timelog in iterator:
            if timelog.keyword in [2, 4]: # 월요일 처음 받은 timelog가 퇴근 또는 퇴근 (재택) 일 경우 해결하기 위해
                week_day = timelog.created_at.weekday()# 생성된 날의 날짜 정보 얻어옴
                monday = timelog.created_at - datetime.timedelta(week_day)# 그 주의 월요일 정보를 얻어옴 (날짜만 월요일)
                time1 = monday.time()# 시간까지 00:00:00 으로 맞추기 위해 월요일의 시간을 얻어옴
                monday = monday - datetime.timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second,
                                                         microseconds=time1.microsecond)# 월요일 자정으로 맞춤
                work_time = timelog.created_at - monday
                work_times[0] = work_time
            else:# 월요일 처음 받은 timelog가 출근 또는 출근 (재택)일 경우
                try:
                    start = timelog # start 에 timelog 복제해놓음
                    iterator, iterator2 = tee(iterator)
                    week_day = start.created_at.weekday()
                    if next(iterator2):# 다음 timelog가 있을 경우
                        end = next(iterator)
                        if week_day in work_times:
                            work_times[week_day] += (end.created_at - start.created_at)# 같은날 데이터가 있을 경우 더함
                        else:
                            work_times[week_day] = (end.created_at - start.created_at)
                    else:
                        if week_day in work_times:
                            work_times[week_day] += (datetime.datetime.now() - start.created_at)
                        else:
                            work_times[week_day] = (datetime.datetime.now() - start.created_at)
                except StopIteration:
                    break
        for d in work_times:
            work_times[d] = str(work_times[d])
            print(work_times[d])
            try:
                work_times[d] = round((float(work_times[d].split(':')[0]) + float(work_times[d].split(':')[1]) / 60),2)  # hours:momutes to hours
            except:# 첫날 정보가 24시간 이상이면 23시간 30분으로 저장
                hrs = time.strftime('%H:%M:%S', time.gmtime(86300))
                work_times[d] = hrs
                work_times[d] = round((float(work_times[d].split(':')[0]) + float(work_times[d].split(':')[1]) / 60),2)  # hours:momutes to hours
            print(work_times[d])

        week_hours = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        total = 0
        for i in week_hours:
            if i in work_times.keys(): week_hours[i] = work_times[i]
            total += week_hours[i]
            total = round(total, 2)
        week_hours['total']=total

        return (week_hours)

def makeEach(request):
    users3=User.objects.filter(grade=3)
    grade3data={}
    for user in users3:
        queryset3 = Timelog.objects.filter(created_at__week_day__lte=datetime.datetime.now().weekday(),
                                          created_at__gt=datetime.datetime.now()-datetime.timedelta(days=8),
                                          user=user).order_by('created_at')
        grade3data[user]=get_graph(queryset3)
        # grade3data_e=enumerate(grade3data)
        count=Timelog.objects.filter(created_at__week_day__lte=datetime.datetime.now().weekday(),
                                          created_at__gt=datetime.datetime.now()-datetime.timedelta(days=8),
                                          user=user,half_day_off='오전 반차').order_by('created_at')
        lcount={}
        lcount[user]=len(count)
    print(grade3data)

    return  render(request,'home/ex.html',{'grade3data':grade3data,'count':lcount})
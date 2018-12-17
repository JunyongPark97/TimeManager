
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from user import views
from user.views import EnterTimelogViewSet, OutTimelogViewSet, EnterAtHomeTimelogViewSet, \
    OutAtHomeTimelogViewSet, TimelogList, TimelogEditRequest, EditTimelog, MakeGraph

router = SimpleRouter()
router.register('enter', EnterTimelogViewSet)
router.register('out', OutTimelogViewSet)
router.register('enter-at-home', EnterAtHomeTimelogViewSet)
router.register('out-at-home', OutAtHomeTimelogViewSet)

app_name='user'
urlpatterns = [
    path('', TimelogList.as_view(), name='timelog_list'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout1/',LogoutView.as_view(),name='logout1'),
    path('password/',views.change_password, name='change_password'),
    path('api/timelog/', include(router.urls)),
    path('timelog_edit/<int:pk>/',TimelogEditRequest.as_view(), name='timelog_edit'),
    path('edit/',EditTimelog.as_view(),name='edit_timelog'),
    path('edit/<int:pk1>/<int:pk2>/',views.edittimelogconfirm,name='edit_timelog_confirm'),
    path('timedata/',MakeGraph.as_view(),name='timedata')

]

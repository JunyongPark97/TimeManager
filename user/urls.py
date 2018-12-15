
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from user import views
from user.views import EnterTimelogViewSet, OutTimelogViewSet, EnterAtHomeTimelogViewSet, \
    OutAtHomeTimelogViewSet, UpdateRequestEnterViewSet, TimelogList

router = SimpleRouter()
router.register('enter', EnterTimelogViewSet)
router.register('out', OutTimelogViewSet)
router.register('enter-at-home', EnterAtHomeTimelogViewSet)
router.register('out-at-home', OutAtHomeTimelogViewSet)
router.register('update-request/enter', UpdateRequestEnterViewSet)

app_name='user'
urlpatterns = [
    path('', views.graph, name='graph'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout1/',LogoutView.as_view(),{'next_page':'/'},name='logout1'),
    # path('request/<int:pk>', views.request_view, name='request'),
    path('password/',views.change_password, name='change_password'),
    path('gotohome/',views.gotohome, name='gotohome' ),
    path('request-list/',views.requestlist, name='requestlist'),
    path('request-list/<int:pk1>/<int:pk2>/',views.editrequest, name='editrequest'),
    path('list/', views.list, name='list'),
    # path('api/import/', ImportCSVView.as_view(), name='import_csv'),
    # path('api/import/user', ImportUserView.as_view(), name='import_Usercsv'),
    path('ex/', views.makeEach, name='ex'),
    path('api/timelog/', include(router.urls)),
    path('update-request/',views.update_request ,name='update_request'),
    path('timelogs/',TimelogList.as_view(), name='timelog_list')
]

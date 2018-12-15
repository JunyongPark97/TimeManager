from django.contrib import admin
from django.urls import path, include

from jandi.views import JandiEnterAPIView, JandiOutAPIView, JandiEnterHomeAPIView, JandiOutHomeAPIView

urlpatterns = [
    path('api/jandi/enter/', JandiEnterAPIView.as_view()),
    path('api/jandi/out/', JandiOutAPIView.as_view()),
    path('api/jandi/enter-home/', JandiEnterHomeAPIView.as_view()),
    path('api/jandi/out-home/', JandiOutHomeAPIView.as_view()),
]

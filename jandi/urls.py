from django.contrib import admin
from django.urls import path, include

from jandi.views import JandiEnterAPIView, JandiOutAPIView

urlpatterns = [
    path('api/jandi/enter/', JandiEnterAPIView.as_view()),
    path('api/jandi/out/', JandiOutAPIView.as_view()),
    path('api/jandi/enter-home/', JandiEnterAPIView.as_view()),
    path('api/jandi/out-home/', JandiEnterAPIView.as_view()),
]

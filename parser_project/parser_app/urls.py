from django.urls import path
from .views import GoogleRankAPIView

urlpatterns = [
    path("google-rank/", GoogleRankAPIView.as_view(), name="google-rank"),  # не добавляй api/ тут
]

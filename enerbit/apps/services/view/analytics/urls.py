from django.urls import path
from .view import Analytics

urlpatterns = [
    path("analytics/",Analytics.as_view())
]

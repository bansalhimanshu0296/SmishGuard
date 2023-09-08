from django.urls import path

from backend.views import *

app_name = "backend"

urlpatterns = [
    path('Test_Api', Test_Api.as_view()),
    path('Analyze_Text', Analyze_Text.as_view()),
]
from django.urls import path

from myapp.views import Master, template

urlpatterns = [
    path('', Master.as_view()),
]
from django.urls import path

from . import views
urlpatterns = [
    path('', views.subscribe, name='send_mail'),
]
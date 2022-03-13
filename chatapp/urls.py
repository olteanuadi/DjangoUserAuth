from django.urls import path
from chatapp.views import app_index, room_name

app_name = 'chatapp'
urlpatterns = [
    path('', app_index, name="index"),
    path('<str:name>/', room_name, name="room"),
]
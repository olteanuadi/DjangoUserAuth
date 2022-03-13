from django.shortcuts import render

# Create your views here.

def app_index(request):
    return render(request, 'chatapp/index.html')

def room_name(request, name):
    return render(request, 'chatapp/chatroom.html', {'room_name':name})
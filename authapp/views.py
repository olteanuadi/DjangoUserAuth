import time
from django.db.models.query_utils import Q
from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic.base import  TemplateView, View
from django.template.response import TemplateResponse

from authapp.models import FriendRequest, FriendStatus, UserRegistrationModel
from .forms import  UserRegistration, UserEditForm
import pyqrcode
from django.utils.decorators import method_decorator
import cv2
import pandas as pd

from authapp import forms


# Create your views here.

@login_required
def dashboard(request):
    context = {
        "welcome": "Welcome to your dashboard"
    }
    return render(request, 'authapp/dashboard.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            return render(request, 'authapp/register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'authapp/register.html', context=context)


class Register_User(View):

    template_name = "forms/success.html"

    # def start_timer(self, response):
    #     index = 0
    #     while True:
    #         print(index)
    #         index += 1
    #         time.sleep(1)
    #         if (index == 10):
    #             break

    def post(self, request):

        if request.method == 'POST':
            print(True)

        form = forms.TestUserForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            try:
                code = form.cleaned_data['code']
            except:
                pass

            print(user_name, password, confirm_password)

            if password == confirm_password:
                user = TestUser(user_name=user_name, code=code)
                user.set_password(password)
                user.save()
            
        response = TemplateResponse(request, self.template_name, {})
        # response.add_post_render_callback(self.start_timer)
        return response
    
    # def get(self, request):

    #     response = TemplateResponse(request, 'forms/form.html', {})



@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'authapp/edit.html', context=context)


@login_required
def show_all_users(request):
    users = UserRegistrationModel.objects.all()
    return render(request, 'friends/index.html', {'userregistrationmodels' : users})



# Method for sending a friend request, using UserRegitrationModel.User.id index
@login_required
def send_friend_request(request, from_user_id, user_id):
    friend_request = FriendRequest(from_user_id = from_user_id, user_target_id = user_id)
    print("{} sent to {}".format(from_user_id, user_id))
    # # fr = friend_request.save(commit=False)
    # friend_request.user_target_id = user_id
    # friend_request.from_user_id = from_user_id
    friend_request.save()
    return redirect('/dashboard/')



# Displaying all the friend requests a user has
@login_required
def show_friend_requests(request):
    users = UserRegistrationModel.objects.all()
    print(request.user.id)

    # Getting all the FriendRequests that contain logged user's index
    # and itertaing through all users to get User objects 
    friend_requests_list = []
    friend_requests = FriendRequest.objects.filter(user_target_id = request.user.id)
    for f_r in friend_requests:
        id = f_r.from_user_id
        print(id)
        for user in users:
            if user.user.id == id:
                user_object = user.user
                friend_requests_list.append(user_object)
    print(friend_requests_list)

    friends = FriendStatus.objects.filter(Q(user_id = request.user.id) | Q(friend_id = request.user.id))
    # Iterating through all the FriendStatus objects ('friends') that contain the logged user's id
    # and storing friends ids in 'friend_indexes'
    friends_indexes = []
    friends_list = []
    for friend in friends:
        if(friend.user_id == request.user.id):
            friends_indexes.append(friend.friend_id)
        else:
            friends_indexes.append(friend.user_id)
    print(friends_indexes)

    # Storing all friends as User Objects in 'friends_list'
    for user in users:
        for id in friends_indexes:
            if user.user.id == id:
                friends_list.append(user.user)
    return render(request, 'friends/requests.html', {"friend_requests_list": friend_requests_list, 'friends_list': friends_list})



# Accepting friend requests by sender index
@login_required
def accept_friend_request(request, sender_id):
    try:
        friend_relation = FriendStatus(user_id = request.user.id, friend_id = sender_id)
        print("{} is now friends with {}".format(request.user.id, sender_id))
        friend_relation.save()
        FriendRequest.objects.get(from_user_id = sender_id, user_target_id = request.user.id).delete()
    except:
        pass
    return redirect('/all_users/frs/')


# Creating a QR Code to redirect user to his/her friend list
@method_decorator(login_required, name='dispatch')
class QrFriendsList(TemplateView):
    template_name = "friends/qr_friends.html"

    def get_context_data(self, *args, **kwargs):
        # Getting the url to redirect to
        url = "localhost:8000/all_users/frs/"
        # Generating the qr for the link
        qr = pyqrcode.create(url)
        qr.png("qr.png", scale=8)
        img = cv2.imread("static/myqr.png")
        return {'qr': img}
        

def get_friend_list(user_id):
    # Getting all the users
    users = UserRegistrationModel.objects.all()
    # Getting all "FriendStatus" objects where 'user_id' or 'friend_id' is equals to the logged user id
    friends = FriendStatus.objects.filter(Q(user_id = user_id) | Q(friend_id = user_id))
    # Storing the indexes in 'friends_indexes'
    friends_indexes = []
    friends_list = []
    for friend in friends:
        if(friend.user_id == user_id):
            friends_indexes.append(friend.friend_id)
        else:
            friends_indexes.append(friend.user_id)

    # Storing all friends as User Objects in 'friends_list'
    for user in users:
        for id in friends_indexes:
            if user.user.id == id:
                friends_list.append(user.user.username)

    return friends_list


# Downloading user's friend list to an csv
@method_decorator(login_required, name='dispatch')
class DownloadFriendsList(TemplateView):

    template_name = "friends/download_friends.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Getting all friends for logged user
        firends_list = get_friend_list(self.request.user.id)
        # print(firends_list)

        # Creating a DataFrame object for user's friends list
        data = {
            "friends" : firends_list
        }

        df = pd.DataFrame(data)
        df.to_csv(f'static/friends{self.request.user.id}.csv')
        context['friends_csv'] = f'friends{self.request.user.id}.csv'
        return context
        # print(df.loc[0])



    



# @login_required
# def create_post(request):
#     if request.method == 'POST':
#         post_form = CreatePostForm(instance=request.user,
#                                  data=request.POST)
#         if post_form.is_valid():
#             new_post = post_form.save(commit=False)
#             new_post.set_post_text(
#                 post_form.get('post_text')
#             )
#             new_post.save()
#             return redirect('/')
#     else:
#         post_form = CreatePostForm(instance=request.user)
#     context = {
#         'form': post_form,
#     }
#     return render(request, 'user_posts/create_post_form.html', context=context)
    


# @login_required
# def posts_index(request):
#     latest_posts = UserPost.objects.order_by('-pk')
#     context = {'latest_posts' : latest_posts}
#     return render(request, 'user_posts/posts_home.html', context)


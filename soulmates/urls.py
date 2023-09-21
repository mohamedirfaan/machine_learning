from django.contrib import admin
from django.urls import include
from soulmates import routing
from django.urls import path

from . import views

urlpatterns=[
    path('index',views.home,name="home"),
    path('login',views.login_user,name="login"),
    path('register',views.register,name="register"),
    path('logout',views.logout_user,name="logout"),
    path('profile/logout',views.logout_user,name="logout"),
    #path('<int:id>',views.pprofile,name="profile"),
    path('profile/<int:id>',views.pprofile,name="profile"),
    path('profile/profile/<int:id>',views.pprofile,name="profile"),
    path("message/room/<int:id>",views.message,name="message"),
    path("message/chat/<int:id>",views.message1,name="message"),
    path("chat/<int:id>",views.message1,name="message"),
    path("message/",views.message,name="message"),
    path('searchresult',views.searchresult,name="searchresult"),
    path('profile/send-request',views.send_friend_request,name="send-request"),
    path("accept-friend-request",views.acceptfriendrequest,name="accept-friend-request"),
    path("select-friends",views.select_friends,name="select-friends"),
    path('create-room',views.create_room,name="create-room"),
    path("send-message",views.send_message,name="send-message"),
    path("send-comment",views.send_comment,name="send-comment"),
    path("get_messages/",views.get_message,name="get_messages"),
    path('ws/', include(routing.websocket_urlpatterns)),
    path('initiatemessage',views.initiatemessage,name="initiatemessage"),
    #path("click-friend",views.click_friend,name="click-friend"),
]
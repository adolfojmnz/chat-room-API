from django.urls import path

from api import views


app_name = 'api'
urlpatterns = [
    path('users', views.UserListView.as_view(), name='users'),
    path('chatrooms', views.ChatListView.as_view(), name='chatrooms'),
    path('chats', views.ChatListView.as_view(), name='chats'),
    path('topics', views.TopicListView.as_view(), name='topics'),
    path('chatroom-messages', views.ChatroomMessageListView.as_view(), name='chatroom-messages'),
    path('chat-messages', views.ChatMessageListView.as_view(), name='chat-messages'),
]

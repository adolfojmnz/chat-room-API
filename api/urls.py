from django.urls import path

from api import views


app_name = 'api'
urlpatterns = [
    path('users', views.UserListView.as_view(), name='users'),
    path('chatrooms', views.ChatListView.as_view(), name='chatrooms'),
    path('chats', views.ChatListView.as_view(), name='chats'),
    path('topics', views.TopicListView.as_view(), name='topics'),
    path('messages', views.MessageListView.as_view(), name='messages'),
    path('files', views.FileListView.as_view(), name='files'),
]
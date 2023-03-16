from django.urls import path

from api import views


app_name = 'api'
urlpatterns = [
    path('users', views.UserListView.as_view(), name='users'),
    path('users/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('chatrooms', views.ChatroomListView.as_view(), name='chatrooms'),
    path('chatrooms/<int:pk>', views.ChatroomDetailView.as_view(), name='chatroom-detail'),
    path('chats', views.ChatListView.as_view(), name='chats'),
    path('chats/<int:pk>', views.ChatDetailView.as_view(), name='chat-detail'),
    path('topics', views.TopicListView.as_view(), name='topics'),
    path('topics/<int:pk>', views.TopicDetailView.as_view(), name='topic-detail'),
    path('chatroom-messages', views.ChatroomMessageListView.as_view(), name='chatroom-messages'),
    path('chatroom-messages/<int:pk>', views.ChatroomMessageDetailView.as_view(), name='chatroom-message-detail'),
    path('chat-messages', views.ChatMessageListView.as_view(), name='chat-messages'),
    path('chat-messages/<int:pk>', views.ChatMessageDetailView.as_view(), name='chat-message-detail'),
]

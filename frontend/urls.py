from django.urls import path

from frontend import views


app_name ='frontend'
urlpatterns = [
    path('chatrooms', views.ChatroomListView.as_view(), name='chatrooms')
]
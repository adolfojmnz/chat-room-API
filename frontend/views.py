from django.views.generic import TemplateView


class ChatroomListView(TemplateView):
    template_name = 'chatroom_list.html'
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .models import Message
from tasks.models import Teacher
from .forms import CreateMessageForm

from itertools import chain

# Create your views here.
class Main(LoginRequiredMixin, TemplateView):
    template_name = 'messages/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if hasattr(user, 'teacher'):
            teachers = []
            groups = {}

            for teacher in Teacher.objects.all().exclude(user=self.request.user):
                resipient = {}
                resipient['user'] = teacher.user
                story = teacher.user.sender.filter(read=False).filter(resipient=user)
                resipient['story'] = len(story[:10])
                teachers.append(resipient)

            for group in user.teacher.num_groups.all():
                students = []
                name_group = f'{group.group.name}:{group.name}'
                
                for student in group.student_set.all():
                    resipient = {}
                    resipient['user'] = student.user
                    story = student.user.sender.filter(read=False).filter(resipient=user)
                    resipient['story'] = len(story[:10])
                    students.append(resipient)
                
                groups[name_group] = students

            context['groups'] = groups
            context['teachers'] = teachers
        elif hasattr(user, 'student'):
            teachers = []
            allies = []
            
            for teacher in Teacher.objects.all():
                resipient = {}
                resipient['user'] = teacher.user
                story = teacher.user.sender.filter(read=False).filter(resipient=user)
                for message in story:
                    print(message.sender)
                resipient['story'] = len(story[:10])
                teachers.append(resipient)
            
            for student in self.request.user.student.num_group.student_set.all().exclude(user=self.request.user):
                resipient = {}
                resipient['user'] = student.user
                story = student.user.sender.filter(read=False).filter(resipient=user)
                resipient['story'] = len(story[:10])
                allies.append(resipient)

            context['teachers'] = teachers
            context['allies'] = allies

        return context

class CreateMessageView(LoginRequiredMixin, CreateView):
    template_name = 'messages/create.html'
    form_class = CreateMessageForm

    def get_initial(self):
        initial = super().get_initial()
        initial['sender'] = self.request.user
        initial['resipient'] = User.objects.get(id=self.kwargs['pk'])
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resipient = User.objects.get(id=self.kwargs['pk'])
        context['resipient'] = resipient
        message_resipient = list(Message.objects.filter(resipient=resipient).filter(sender=self.request.user))
        message_sender = list(Message.objects.filter(sender=resipient).filter(resipient=self.request.user))
        result_list = sorted(
            chain(message_sender, message_resipient),
            key=lambda data: data.time, reverse=False
        )

        for message in result_list:
            if message.resipient == self.request.user:
                message.read = True
                message.save()

        context['story'] = result_list[-10:]
        return context

    def get_success_url(self):
        return self.request.path
from django.shortcuts import render
from django.views.generic import TemplateView

from tasks.models import Task, TaskStudent

# Create your views here.
class HomePage(TemplateView):
    template_name = 'main/home.html'

    def get(self, request, *argv, **kwargs):
        response = super().get(request, *argv, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'student'):
                tasks = TaskStudent.objects.filter(student=user.student).filter(answer=None)
                _open = []
                _close = []
                _end = []

                for task in tasks:
                    if task.task.closeTask():
                        _end.append(task)
                    else:
                        if task.task.openTask():
                            _open.append(task)
                        else:
                            _close.append(task)

                context['open_task'] = _open
                context['close_task'] = _close
                context['end_task'] = _end
            elif hasattr(user, 'teacher'):
                tasks = Task.objects.filter(teacher=user.teacher)
                task_student = []
                for task in tasks:
                    task_student += TaskStudent.objects.filter(task=task).filter(appraisal=None).exclude(answer=None)
                context['unverified'] = task_student

            if user.resipient.filter(read=False):
                context['unread'] = True

        return context
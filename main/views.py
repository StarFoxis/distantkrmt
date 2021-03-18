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
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'student'):
                _open = []
                _close = []
                _end = []
                tasks_student = TaskStudent.objects.filter(student=user.student).filter(answer=None)
                for task_student in tasks_student:
                    if task_student.task.seenTask():
                        if task_student.task.closeTask():
                            _end.append(task_student)
                        else:
                            if task_student.task.openTask():
                                _open.append(task_student)
                            else:
                                _close.append(task_student)
                kwargs['open_task'] = _open
                kwargs['close_task'] = _close
                kwargs['end_task'] = _end
            elif hasattr(user, 'teacher'):
                tasks = Task.objects.filter(teacher=user.teacher)
                task_student = []
                for task in tasks:
                    task_student += TaskStudent.objects.filter(task=task).filter(appraisal=None).exclude(answer=None)
                kwargs['unverified'] = task_student
        return kwargs
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseNotFound
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from .models import Task, TaskStudent, NumGroup, Answer
from .forms import TaskForm, AnswerForm, EditTaskForm

# Create your views here.
def ajax_get_subject(request):
    subjects = NumGroup.objects.get(id=request.POST['num_group']).subjects.values('id', 'name')
    data = {}
    for obj in subjects:
        data[obj['id']] = obj['name']
    return JsonResponse(data)

def setGroupNum(request):
    group_num = list(GroupNumber.objects.filter(group_id=request.POST.get('id_group')))
    data = {}
    for element in group_num:
        data[element.id] = element.name
    return JsonResponse(data)

class ChoiceView(LoginRequiredMixin, TemplateView):
    # login_url = reverse_lazy('login')
    template_name = 'tasks/choice_action.html'

class CreateTaskView(PermissionRequiredMixin, CreateView):
    template_name = 'tasks/create_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('list-task')
    permission_required = 'tasks.add_task'

    def get_form(self, obj=None, **kwargs):
        form = super().get_form(obj, **kwargs)
        form.fields['teacher'].initial = self.request.user.teacher 
        return form

class ListTaskView(PermissionRequiredMixin, ListView):
    template_name = 'tasks/list_task.html'
    model = Task
    permission_required = 'tasks.change_task'

    def get_queryset(self):
        query = super().get_queryset()
        for obj in query:
            obj.answer_count = len(obj.taskstudent_set.exclude(answer=None))
        return query

class DetailTaskView(PermissionRequiredMixin, DetailView):
    template_name = 'tasks/detail_task.html'
    model = Task
    permission_required = 'tasks.change_task'
    context_object_name = 'detail'

class EditTaskView(PermissionRequiredMixin, UpdateView):
    template_name = 'tasks/edit_task.html'
    model = Task
    form_class = EditTaskForm
    permission_required = 'tasks.change_task'

class DeleteTaskView(PermissionRequiredMixin, DeleteView):
    template_name = 'tasks/delete_task.html'
    model = Task
    permission_required = 'tasks.delete_task'
    success_url = reverse_lazy('list-task')

class StudentListTaskView(UserPassesTestMixin, ListView):
    template_name = 'tasks/student_list_task.html'
    model = TaskStudent
    context_object_name = 'tasks'

    def get_queryset(self):
        return TaskStudent.objects.filter(student=self.request.user.student)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = context['tasks']

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
        
        context['open'] = _open
        context['close'] = _close
        context['end'] = _end 

        # print(context)

        return context

    def test_func(self):
        return hasattr(self.request.user, 'student')

class ListAnswerView(PermissionRequiredMixin, ListView):
    template_name = 'tasks/list_answer.html'
    model = TaskStudent
    permission_required = 'tasks.change_task'
    context_object_name = 'answers'

    def get_queryset(self):
        answers = TaskStudent.objects.filter(task_id=self.kwargs.get('task'))
        return answers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = context['answers']
        context['completed'] = tasks.exclude(answer=None)
        context['unfulfilled'] = tasks.filter(answer=None)
        return context

class CreateAnswerTaskView(UserPassesTestMixin, CreateView):
    template_name='tasks/answer_task.html'
    form_class = AnswerForm
    success_url = reverse_lazy('student-list-task')

    def post(self, request, *argv, **kwargs):
        response = super().post(request, *argv, **kwargs)
        task_student = TaskStudent.objects.get(id=kwargs.get('pk'))

        if task_student.answer_id:
            return HttpResponseNotFound('Вы уже отправили ответ на это задание')
        else:
            answer = self.get_form().save()
            task_student.answer = answer
            task_student.save()
        return response

    def test_func(self):
        return hasattr(self.request.user, 'student') and TaskStudent.objects.get(id=self.kwargs.get('pk')).task.openTask()

class EditAnswerTaskView(UserPassesTestMixin, UpdateView):
    model = Answer
    template_name='tasks/edit_answer.html'
    form_class = AnswerForm
    success_url = reverse_lazy('student-list-task')

    def test_func(self):
        return hasattr(self.request.user, 'student') and TaskStudent.objects.get(id=self.kwargs.get('task')).task.openTask()

class DetailAnswerView(UserPassesTestMixin, DetailView):
    template_name = 'tasks/detail_answer.html'
    model = TaskStudent
    context_object_name = 'answer'

    def test_func(self):
        user = self.request.user
        return hasattr(user, 'teacher') or (hasattr(user, 'student') and user.student.taskstudent_set.filter(answer=TaskStudent.objects.get(pk=self.kwargs.get('pk')).answer))

class CreateAppraisalView(PermissionRequiredMixin, UpdateView):
    template_name = 'tasks/create_appraisal.html'
    model = TaskStudent
    fields = ('appraisal',)
    # success_url = reverse_lazy('detail-answer')
    permission_required = 'tasks.change_task'



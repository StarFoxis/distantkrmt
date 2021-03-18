from django.contrib import admin

from .models import Appraisal, Task, TaskStudent, Answer

from .forms import TaskForm, AnswerForm

# Register your models here.
admin.site.register(Appraisal)
admin.site.register(TaskStudent)
admin.site.register(Answer)


class TaskAdmin(admin.ModelAdmin):
    form = TaskForm
    list_display = ('name', 'teacher')

admin.site.register(Task, TaskAdmin)

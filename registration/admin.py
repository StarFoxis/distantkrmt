from django.contrib import admin

from .models import Group, NumGroup, Subject, Student, Teacher

# Register your models here.
admin.site.register(Group)
admin.site.register(NumGroup)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
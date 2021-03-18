from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.urls import reverse_lazy

from .forms import UserForm, StudentForm, TeacherForm

# Create your views here.
class RecognationView(TemplateView):
    template_name = 'registration/recognation.html'

def signupStudentView(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST)

        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save(user_form.instance)         
            login(request, user_form.instance)
            return redirect('home')
    else:
        user_form = UserForm()
        student_form = StudentForm()
    return render(request, 'registration/signup_student.html', {'user_form': user_form, 'student_form': student_form})

def signupTeacherView(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        teacher_form = TeacherForm(request.POST)

        if user_form.is_valid() and teacher_form.is_valid():
            user_form.save()
            teacher_form.save(user_form.instance)         
            login(request, user_form.instance)
            return redirect('home')
    else:
        user_form = UserForm()
        teacher_form = TeacherForm()
    return render(request, 'registration/signup_teacher.html', {'user_form': user_form, 'teacher_form': teacher_form})
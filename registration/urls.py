from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from .views import RecognationView, signupStudentView, signupTeacherView

urlpatterns = [
    path('login/', LoginView.as_view(success_url='home'), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('recognation/', RecognationView.as_view(), name='recognation'),
    path('signupS/', signupStudentView, name='signup-student'),
    path('signupT/', signupTeacherView, name='signup-teacher')

]
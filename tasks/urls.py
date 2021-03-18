from django.urls import path

from .views import (CreateTaskView, 
                   ChoiceView, 
                   ListTaskView, 
                   StudentListTaskView, 
                   DetailTaskView, 
                   EditTaskView, 
                   DeleteTaskView, 
                   CreateAnswerTaskView, 
                   EditAnswerTaskView, 
                   DetailAnswerView, 
                   ListAnswerView, 
                   CreateAppraisalView, 

                   ajax_get_subject)

urlpatterns = [
    path('', ChoiceView.as_view(), name='choice-action'),
    path('task/create/', CreateTaskView.as_view(), name='create-task'),
    path('tasks/', ListTaskView.as_view(), name='list-task'),
    path('my_tasks/', StudentListTaskView.as_view(), name='student-list-task'),
    path('task/<int:pk>/', DetailTaskView.as_view(), name='detail-task'),
    path('task/<int:pk>/edit/', EditTaskView.as_view(), name='edit-task'),
    path('task/<int:pk>/delete/', DeleteTaskView.as_view(), name='delete-task'),
    path('task/<int:task>/answers/', ListAnswerView.as_view(), name='list-answer'),
    path('task/<int:pk>/answers/answer/create/', CreateAnswerTaskView.as_view(), name='answer-task'),
    path('task/<int:task>/answers/answer/<int:pk>/edit/', EditAnswerTaskView.as_view(), name='edit-answer'),
    path('task/<int:task>/answers/answer/<int:pk>/', DetailAnswerView.as_view(), name='detail-answer'),
    path('task/<int:task>/answers/answer/<int:pk>/appraisal/', CreateAppraisalView.as_view(), name='create-appraisal'),

    path('ajax/get_subject/', ajax_get_subject, name='get-subject'),
]
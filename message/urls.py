from django.urls import path

from . import views

urlpatterns = [
    path('', views.Main.as_view(), name='message'),
    path('create/<int:pk>/', views.CreateMessageView.as_view(), name='create-message'),
]
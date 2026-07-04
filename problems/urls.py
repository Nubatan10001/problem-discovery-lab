from django.urls import path

from . import views

urlpatterns = [
    path('', views.problem_list, name='problem_list'),
    path('ideas/new/', views.problem_create, name='problem_create'),
    path('ideas/<int:pk>/', views.problem_detail, name='problem_detail'),
    path('ideas/<int:pk>/messages/', views.add_message, name='add_message'),
    path('ideas/<int:pk>/structure/', views.structure_idea, name='structure_idea'),
    path('signup/', views.signup, name='signup'),
]

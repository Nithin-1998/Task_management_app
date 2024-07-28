# core/urls.py

from django.urls import path
from .views import home, register, admin_view, manager_view, profile, custom_logout, manager_action,manage_task,task_creation,task_deletion,task_edit,task_view,profile_edit
from django.contrib.auth import views as auth_views
#from .views import TaskDetail

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('logout/', custom_logout, name = 'logout'),  #logout url pattern
    path('admin-view/', admin_view, name='admin_view'),
    path('manager-view/', manager_view, name='manager_view'),
    path('profile/', profile, name='profile'),
    path('manager-action/', manager_action, name = "manager_action" ),
    path('manage-task/<str:slug>/',manage_task, name = "manage_task"),
    path('task_creation/<str:slug>/',task_creation, name = "task_creation"),
    path('task_deletion/<str:slug>/', task_deletion, name = "task_deletion"),
    path('task_edit/<str:slug>/',task_edit, name = "task_edit"),
    path('task_view/<str:slug>/',task_view, name = "task_view"),
    path('profile_edit',profile_edit,name = "profile_edit"),
]

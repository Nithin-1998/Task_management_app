# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import CustomUserCreationForm
from django.contrib.auth import views as auth_views
from django.http import HttpResponseForbidden
from .models import CustomUser, Task
from .task_form import TaskForms
from .profile_edit_form import ProfileEditForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import TaskSerializer



#view function for the user registration

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    elif request.method == 'GET':
        return render(request, 'logout.html')
    else:
        return HttpResponseForbidden()

@login_required
def home(request):
    if not request.user.is_approved:
        return HttpResponseForbidden("you are waiting for approaval")
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.is_approved = False
            user.save()
            return HttpResponseForbidden("you are waiting for approaval")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    if not request.user.is_approved:
        return HttpResponseForbidden("you are waiting for approaval")
    return render(request, 'profile.html')


@login_required
@user_passes_test(lambda u: u.role == 'admin')
def admin_view(request):
    return render(request, 'admin.html')

@login_required
@user_passes_test(lambda u: u.role == 'manager')
def manager_view(request):
    return render(request, 'manager.html')


def redirect_to_login(request):
    return redirect('login')


login_method = auth_views.LoginView.as_view(template_name='login.html')


# view function for the task management

def manager_action(request):
    user_details = CustomUser.objects.filter(role = 'user')
    return render(request,'manager_action.html',{'user_details':user_details})

def manage_task(request,slug):
    user_details = get_object_or_404(CustomUser, slug = slug)
    return render(request,'manage_task.html',{'user_details':user_details})

def task_creation(request,slug):

    user = get_object_or_404(CustomUser, slug = slug)

    if request.method == "POST":
        form = TaskForms(request.POST)
        if form.is_valid():
            user_form = form.save(commit = False)
            user_form.assigned_to = user
            user_form.save()
            return redirect(reverse('core:manage_task',kwargs = {'slug':slug}))
        
    form = TaskForms()
    return render(request,'task_creation.html',{'form':form,'user':user})

def task_deletion(request,slug):

    user = get_object_or_404(CustomUser,slug = slug)
    user_forms = Task.objects.filter(assigned_to = user)

    if request.method == "POST":
        for i, user_form in enumerate(user_forms):
            form_set = TaskForms(request.POST, instance = user_form, prefix = f'id_{i}')
            if form_set.prefix in request.POST:
                user_form.delete()
                break
        return redirect(reverse('core:task_deletion',kwargs={'slug':slug}))
    
    form = []
    for i, user_form in enumerate(user_forms):
        form_set = TaskForms(instance = user_form,prefix = f'id_{i}')
        form.append(form_set)
    return render(request,"task_deletion.html",{'form':form,'user':user})  # is this method will execute delete well

def task_edit(request,slug):

    user = get_object_or_404(CustomUser,slug = slug)
    user_forms = Task.objects.filter(assigned_to = user)
    
    if request.method == "POST":

        for i, user_form in enumerate(user_forms):
            form_set = TaskForms(request.POST,instance = user_form,prefix = f'id_{i}')

        if form_set.is_valid():
            user_form.save()
            if user.role == 'manager':
                return redirect(reverse('core:manage_task',kwargs={'slug':slug}))
            else:
                return redirect(reverse('core:profile'))
    
    form = []
    for i, user_form in enumerate(user_forms):
        form_set = TaskForms(instance= user_form, prefix = f'id_{i}')
        form.append(form_set)
    return render(request,"task_edit.html",{'form':form,'user':user})


def task_view(request,slug):

    user = get_object_or_404(CustomUser,slug = slug)
    user_forms = Task.objects.filter(assigned_to =user)
    form = []

    for i, user_form in enumerate(user_forms):
        form_set = TaskForms(instance= user_form, prefix = f'id_{i}')
        form.append(form_set)

    return render(request,"task_view.html",{'form':form,'user':user})

# Editing the profile
@login_required
def profile_edit(request):

    if request.method == "POST":
        form = ProfileEditForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('core:profile')
        
    form = ProfileEditForm(instance = request.user)
    return render(request,'profile_edit.html',{'form':form})

'''#view function of Rest API
class TaskDetail(APIView):

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        task = self.get_object(pk=pk)
        if task is None:
            return Response({"error":"Task not found"},status = status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        task = self.get_object(pk)
        if task is None:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response({'success':'instance_deleted'},status = status.HTTP_200_OK)'''
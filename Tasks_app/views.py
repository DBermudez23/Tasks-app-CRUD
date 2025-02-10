from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CreateTaskForm
from .models import Task


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm()
        })
    else: 
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            user.save()
            return redirect('tasks')
        else:
            return render(request, 'signup.html',{
                'form': UserCreationForm(),
                'error': 'Passwords did not match or username is already taken'
            })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form' : AuthenticationForm()
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': 'Username and password did not match'
            })
        else:
            login(request, user)
            return redirect('tasks')
        
@login_required
def signout(request):
    logout(request)
    return redirect('home')   
        
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks,
        'user' : request.user
    })

@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'create.html', {
        'form': CreateTaskForm
    })
    else:
        try:
            form = CreateTaskForm(request.POST)
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create.html', {
                'form': CreateTaskForm,
                'error': 'Bad data passed in. Try again.'
            })
            
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'GET':
        form = CreateTaskForm(instance=task)
        return render(request, 'task_details.html', {
            'form' : form,
            'task' : task
        })
    else:
        try:
            form = CreateTaskForm(request.POST, instance=task, user=request.user)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'form' : form,
                'task' : task,
                'error' : 'Error getting the task'
            })
            
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required    
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')
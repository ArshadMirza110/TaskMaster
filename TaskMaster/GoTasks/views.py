from django.shortcuts import render, redirect
from .models import Task
from django.shortcuts import get_object_or_404
import random

quotes = [
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Success is the sum of small efforts, repeated day in and day out.",
    "Don’t watch the clock; do what it does. Keep going.",
    "Believe you can and you're halfway there.",
    "You are never too old to set another goal or to dream a new dream.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Start where you are. Use what you have. Do what you can."
]

def task_list(request):
    tasks = Task.objects.all()
    motivational_quote = None
    if request.session.get('quote_shown'):
        motivational_quote = request.session['quote_shown']
        del request.session['quote_shown']  # Clear the session variable after showing the quote

    return render(request, 'GoTasks/index.html', {'tasks': tasks, 'motivational_quote': motivational_quote})

def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(title=title, description=description)
        return redirect('task_list')
    return redirect('task_list')

def delete_task(request, task_id):
    task = Task.objects.filter(id=task_id).first()
    if task:
        task.delete()
    return redirect('task_list')

# This is the view for toggling the completion status
def toggle_task_completion(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed  # Toggle the completion status
    task.save()  # Save the updated task
    
    # If the task is completed, choose a random quote
    if task.completed:
        random_quote = random.choice(quotes)
        request.session['quote_shown'] = random_quote  # Store the quote in the session to display it on the next page
    
    return redirect('task_list')


from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Todo
from django.http import HttpResponseRedirect
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class IndexView(generic.ListView):
    template_name = 'todos/index.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        """Return all the latest todos."""
        return Todo.objects.order_by('-created_at')

@csrf_exempt
def github_webhook(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        # Here you can verify the GitHub event type or add security checks (like a secret token)
        subprocess.call(['git', 'pull', 'origin', 'main'])  # Pull latest changes from GitHub
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def add(request):
    title = request.POST['title']
    Todo.objects.create(title=title)

    return redirect('todos:index')

def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    return redirect('todos:index')

def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    isCompleted = request.POST.get('isCompleted', False)
    if isCompleted == 'on':
        isCompleted = True
    
    todo.isCompleted = isCompleted

    todo.save()
    return redirect('todos:index')

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from celery.result import AsyncResult
from celery.backends.database.models import Task
import json

from .scraper.github_scraper import github_scraper
from .models import CeleryTask


def home(request):
    tasks = CeleryTask.objects.all().order_by('-created')
    return render(request, "home.html", {'tasks': tasks})


@csrf_exempt
def run_task(request):
    if request.method == 'POST':
        task_type = request.POST.get("type")
        task = github_scraper.delay()
        celery_task = CeleryTask(task_id=task.id, status=task.status)
        celery_task.save()
        return JsonResponse({'task_id': task.id, 'status': task.status, 'created': celery_task.created}, status=202)


@csrf_exempt
def get_tasks(request):
    if request.method == 'POST':
        pending_tasks = CeleryTask.objects.filter(status='PENDING')
        for pending in pending_tasks:
            task_result = AsyncResult(pending.task_id)
            if task_result.status == 'SUCCESS' or task_result.status == 'FAILURE':
                pending.status = task_result.status
                pending.save()

        tasks = CeleryTask.objects.all().order_by('-created')
        tasks = json.loads(serializers.serialize('json', tasks))
        return JsonResponse({'tasks': tasks}, status=200)

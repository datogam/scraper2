from django.contrib import admin
from django.urls import path

from tasks.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", get_tasks, name="get_tasks"),
    path("task/", run_task, name="run_task"),
    path("", home, name="home"),
]

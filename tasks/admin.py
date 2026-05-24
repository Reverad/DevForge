from django.contrib import admin

from tasks.models import Task, TaskType, Tag


admin.site.register(Task)
admin.site.register(TaskType)
admin.site.register(Tag)

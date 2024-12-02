from django.contrib import admin
from .models import Task
from .models import Decision

admin.site.register(Task)
admin.site.register(Decision)
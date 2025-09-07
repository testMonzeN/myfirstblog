from django.contrib import admin
from .models import Taskpy
from .models import Decisionpy
from .models import Taskjs
from .models import Decisionjs

admin.site.register(Taskpy)
admin.site.register(Decisionpy)
admin.site.register(Taskjs)
admin.site.register(Decisionjs)

from django.contrib import admin
from .models import *

admin.site.register(Task)
admin.site.register(Task_assignment)
admin.site.register(Task_status_history)


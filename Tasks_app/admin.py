from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('dateCreated',) # This will make the created field read only
    
admin.site.register(Task, TaskAdmin)


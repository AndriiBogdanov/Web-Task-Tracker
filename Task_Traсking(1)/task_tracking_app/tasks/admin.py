from django.contrib import admin
from tasks.models import Task, InterestingPost

admin.site.register(Task)
admin.site.register(InterestingPost)

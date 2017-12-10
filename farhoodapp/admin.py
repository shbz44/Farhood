from django.contrib import admin
from farhoodapp.models import Event, Comment, Action, EventMember

admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Action)
admin.site.register(EventMember)

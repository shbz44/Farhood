from django.contrib import admin
from farhoodapp.models import Event, Comment, Action, EventMember, User

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Action)
admin.site.register(EventMember)

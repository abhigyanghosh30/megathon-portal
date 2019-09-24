from django.contrib import admin

# Register your models here.
from .models import Team, Participant

admin.site.register(Team)
admin.site.register(Participant)

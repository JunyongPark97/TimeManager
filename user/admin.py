from django.contrib import admin

# Register your models here.
from user.models import User, Timelog, UpdateRequest

admin.site.register(User)
# admin.site.register(Timelog)
admin.site.register(UpdateRequest)

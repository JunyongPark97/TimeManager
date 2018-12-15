from django.contrib import admin

# Register your models here.
from user.models import User, Timelog, UpdateRequest, EnterTimelog, OutTimelog, EnterAtHomeTimelog, OutAtHomeTimelog

admin.site.register(User)
# admin.site.register(Timelog)
admin.site.register(UpdateRequest)
admin.site.register(EnterTimelog)
admin.site.register(OutTimelog)
admin.site.register(EnterAtHomeTimelog)
admin.site.register(OutAtHomeTimelog)

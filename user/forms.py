from django import forms

from user.models import User, UpdateRequest

class EnterEditForm(forms.ModelForm):
    class Meta:
            model = UpdateRequest
            fields = ['update','breaktime', 'receiver','reason']

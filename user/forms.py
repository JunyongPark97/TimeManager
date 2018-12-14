from django import forms

from user.models import User, UpdateRequest

# class DefaultField:
#     def __call__(self, *args, **kwargs):
#         return User.objects.filter(pk=1)

class RequestForm1(forms.ModelForm): #C_level 끼리 시간 수정 요청
    receiver = forms.ModelChoiceField(queryset=User.objects.filter(grade__lte=1)) # receiver = forms.Cho # 1,2,3 별로  receiver 제한
    class Meta:
        model = UpdateRequest
        fields=['update','breaktime', 'receiver','reason']
        # widgets = {'update': DateTimeWidget(usel10n=True, bootstrap_version=3)}


class RequestForm2(forms.ModelForm): # Leader들은 C level 시간 수정 요청
    receiver = forms.ModelChoiceField(queryset=User.objects.filter(grade__lt=2)) # receiver = forms.Cho # 1,2,3 별로  receiver 제한
    class Meta:
        model = UpdateRequest
        fields = ['update','breaktime', 'receiver','reason']

class RequestForm3(forms.ModelForm): #worker들은 clevel과 leader 에게 시간 수정 요청
    receiver = forms.ModelChoiceField(queryset=User.objects.filter(grade__lt=3)) # receiver = forms.Cho # 1,2,3 별로  receiver 제한
    class Meta:
        model = UpdateRequest
        fields = ['update','breaktime', 'receiver','reason']

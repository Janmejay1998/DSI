from django import forms
from DSIApp.models import Student , log

class LogForm(forms.ModelForm):
    class Meta:
        model = log
        widgets = {'Password': forms.PasswordInput()}
        fields = '__all__'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        widgets = {'Pass': forms.PasswordInput(),'Re_Pass': forms.PasswordInput()}
        fields = '__all__'
        


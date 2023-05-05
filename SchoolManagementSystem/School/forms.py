from django import forms
import re
from .models import Student, Teacher, Notice, Attendance, User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
        
        if len(password) < 8:
            raise forms.ValidationError("Your password must contain at least 8 characters.")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = ''
        self.fields['first_name'].widget.attrs['placeholder'] = ''
        self.fields['last_name'].widget.attrs['placeholder'] = ''
        self.fields['email'].widget.attrs['placeholder'] = ''
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



phone_regex = re.compile(r'^\+?1?\d{9,15}$')

class DateInput(forms.DateInput):
    input_type = 'date'

class StudentForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=10)
    class Meta:
        model = Student
        fields = ('profile_picture','gender','date_of_birth','divisions', 'phone_number', 'roll_no', 'fees')
        widgets = {
            'date_of_birth': DateInput(),
        }

    # validate phone number
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_regex.match(phone_number):
            raise forms.ValidationError('Invalid phone number')
        return phone_number

 
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture']
        self.fields['gender'].widget.attrs['placeholder'] = ''
        self.fields['date_of_birth'].widget.attrs['placeholder'] = ''
        self.fields['divisions'].widget.attrs['placeholder'] = ''
        self.fields['phone_number'].widget.attrs['placeholder'] = ''
        self.fields['roll_no'].widget.attrs['placeholder'] = ''
        self.fields['fees'].widget.attrs['placeholder'] = ''
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class TeacherForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=10)
    class Meta:
        model = Teacher
        fields = ('profile_picture','gender','date_of_birth','salary', 'phone_number')
        widgets = {
            'date_of_birth': DateInput(),
        }

        # validate phone number
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_regex.match(phone_number):
            raise forms.ValidationError('Invalid phone number')
        return phone_number

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture']
        self.fields['gender'].widget.attrs['placeholder'] = ''
        self.fields['date_of_birth'].widget.attrs['placeholder'] = ''
        self.fields['phone_number'].widget.attrs['placeholder'] = ''
        self.fields['salary'].widget.attrs['placeholder'] = ''
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('message',)


class AttendanceForm(forms.ModelForm):
    date = forms.DateField()
    class Meta:
        model = Attendance
        fields = ('student','status','date')
    
    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['placeholder'] = ''
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AskDateForm(forms.Form):
    date = forms.DateField()
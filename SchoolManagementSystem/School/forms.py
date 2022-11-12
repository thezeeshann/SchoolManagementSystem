from django import forms
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

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = ''
        self.fields['first_name'].widget.attrs['placeholder'] = ''
        self.fields['last_name'].widget.attrs['placeholder'] = ''
        self.fields['email'].widget.attrs['placeholder'] = ''
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('divisions', 'phone_number', 'roll_no', 'fees')

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['divisions'].widget.attrs['placeholder'] = ''
        self.fields['phone_number'].widget.attrs['placeholder'] = ''
        self.fields['roll_no'].widget.attrs['placeholder'] = ''
        self.fields['fees'].widget.attrs['placeholder'] = ''
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('salary', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs['placeholder'] = ''
        self.fields['salary'].widget.attrs['placeholder'] = ''
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = "__all__"
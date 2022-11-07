from django.contrib import admin
from .models import User, Student, Teacher, Attendance, Notice
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'username', 'role', 'is_admin')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'divisions', 'roll_no', 'fees','phone_number','is_approved')


admin.site.register(Student, StudentAdmin)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'salary','phone_number','is_approved')


admin.site.register(Teacher, TeacherAdmin)



admin.site.register(Attendance)


admin.site.register(Notice)
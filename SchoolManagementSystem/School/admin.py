from django.contrib import admin
from .models import User, Student, Teacher, Attendance, Notice
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'username', 'role', 'is_admin','is_active')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user','profile_picture','gender','date_of_birth', 'divisions', 'roll_no', 'fees','phone_number','is_approved')


admin.site.register(Student, StudentAdmin)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user','profile_picture','gender','date_of_birth','salary','phone_number','is_approved')


admin.site.register(Teacher, TeacherAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student','date','status')

admin.site.register(Attendance,AttendanceAdmin)

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('message','date','post_by')

admin.site.register(Notice,NoticeAdmin)
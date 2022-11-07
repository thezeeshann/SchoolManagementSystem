from django.urls import path
from . import views

urlpatterns = [

    path('', views.IndexPage, name='index_page'),

    # student
    path('studentclick/', views.StudentClick, name='student_click'),
    path('studentapprovedaccounts/', views.StudentApprovedAccounts, name='student_approved_accounts'),
    path('studentsignup/', views.StudentSingup, name='student_signup'),
    path('studentlogin/', views.StudentLogin, name='studnet_login'),
    path('studentlogout/', views.StudentLogOut, name='student_logout'),
    path('studentadmin/', views.StudentAdmin, name='student_admin'),

    # teacher
    path('teacherclick/', views.TeacherClick, name='teacher_click'),
    path('teacherapprovedaccounts/', views.TeacherApprovedAccounts, name='teacher_approved_accounts'),
    path('teachersingup/', views.TeacherSingup, name='teacher_signup'),
    path('teacherlogin/', views.TeacherLogin, name='teacher_login'),
    path('teacheradmin/', views.TeacherAdmin, name='teacher_admin'),
    path('teacherlogout/', views.TeacherLogOut, name='teacher_logout'),

    # admin
    path('adminclick/', views.AdminClick, name='admin_click'),
    path('adminsignup/', views.AdminSingup, name='admin_signup'),
    path('adminlogin/', views.AdminLogin, name='admin_login'),
    path('adminlogout/',views.AdminLogOut,name='admin_logout'),
    path('adminpanel/', views.AdminDashbord, name='admin_panel'),
    path('adminstudent/', views.AdminStudent, name='admin_student'),
    path('adminteacher/', views.AdminTeacher, name='admin_teacher'),
    path('adminfees/', views.AdminFees, name='admin_fees'),
    path('adminattendance/', views.AdminAttendance, name='admin_attendance'),
    path('adminnotice/', views.AdminNotice, name='admin_notice'),


]
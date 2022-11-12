from django.urls import path
from . import views

urlpatterns = [

    path('', views.IndexPage, name='index_page'),

    # -------------------------- Student -------------------------------
    path('studentclick/', views.StudentClick, name='student_click'),
    path('studentapprovedaccounts/', views.StudentApprovedAccounts, name='student_approved_accounts'),
    path('studentsignup/', views.StudentSingup, name='student_signup'),
    path('studentlogin/', views.StudentLogin, name='studnet_login'),
    path('studentlogout/', views.StudentLogOut, name='student_logout'),
    path('studentadmin/', views.StudentAdmin, name='student_admin'),

    # ------------------------- Teacher ------------------------------
    path('teacherclick/', views.TeacherClick, name='teacher_click'),
    path('teacherapprovedaccounts/', views.TeacherApprovedAccounts, name='teacher_approved_accounts'),
    path('teachersingup/', views.TeacherSingup, name='teacher_signup'),
    path('teacherlogin/', views.TeacherLogin, name='teacher_login'),
    path('teacheradmin/', views.TeacherAdmin, name='teacher_admin'),
    path('teacherlogout/', views.TeacherLogOut, name='teacher_logout'),

    # -------------------------- Admin ----------------------
    path('adminclick/', views.AdminClick, name='admin_click'),
    path('adminsignup/', views.AdminSingup, name='admin_signup'),
    path('adminlogin/', views.AdminLogin, name='admin_login'),
    path('adminlogout/',views.AdminLogOut,name='admin_logout'),
    path('adminpanel/', views.AdminDashbord, name='admin_panel'),
    # ------------------------- Admin Student --------------------
    path('adminstudent/', views.AdminStudent, name='admin_student'),
    path('admin-view-student/',views.AdminViewStudent,name='admin_view_student'),
    path('admin-add-student/',views.AdminAddStudent,name='admin_add_student'),
    path('admin-view-student-fees/',views.AdminViewStudentFees,name='admin_view_student_fees'),
    path('admin-approve-student/',views.AdminApproveStudent,name='admin_approve_student'),
    path('approve-student/<int:pk>/',views.ApproveStudent,name='approve_approve'),
    path('delete-student/<int:pk>/',views.DeleteStudent,name='delete_student'),
    path('update-student-school/<int:pk>/',views.UpdateStudentSchool,name='update_student_school'),
    path('delete-student-school/<int:pk>/',views.DeleteStudentSchool,name='delete_student_school'),
    # --------------------------- Admin Teacher --------------------
    path('adminteacher/', views.AdminTeacher, name='admin_teacher'),
    path('adminfees/', views.AdminFees, name='admin_fees'),
    path('adminattendance/', views.AdminAttendance, name='admin_attendance'),
    path('adminnotice/', views.AdminNotice, name='admin_notice'),


]
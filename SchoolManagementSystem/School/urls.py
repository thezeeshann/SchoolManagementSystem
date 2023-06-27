from django.urls import path
from . import views

urlpatterns = [

    path('', views.IndexPage, name='index_page'),  
    path('sample_view', views.sample_view, name='sample_view'),  
    # ---------------------------- ForGot password --------------------------------------
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot_password/',views.ForgotPassword,name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/',views.ResetPasswordValidate,name='reset_password_validate'),
    path('reset_password/',views.ResetPassword,name='reset_password'),
    path('logout/', views.LogoutView, name='logout'),

    # -------------------------- Student -------------------------------
    path('student_click/', views.StudentClick, name='student_click'),
    path('student_approved_accounts/', views.StudentApprovedAccounts, name='student_approved_accounts'),
    path('student_signup/', views.StudentSingup, name='student_signup'),
    path('student_login/', views.StudentLogin, name='studnet_login'),
    path('student_admin/', views.StudentAdmin, name='student_admin'),
    path('student_attendance/',views.StudentAttendance,name='student_attendance'),

    # ------------------------- Teacher ------------------------------
    path('teacher_click/', views.TeacherClick, name='teacher_click'),
    path('teacher_approved_accounts/', views.TeacherApprovedAccounts, name='teacher_approved_accounts'),
    path('teacher_singup/', views.TeacherSingup, name='teacher_signup'),
    path('teacher_login/', views.TeacherLogin, name='teacher_login'),
    path('teacher_admin/', views.TeacherAdmin, name='teacher_admin'),
    path('teacher_notice/',views.TeacherNotice,name='teacher_notice'),
    path('teacher_deletenotice/<int:pk>/',views.TeacherDeleteNotice,name='teacher_delete_notice'),
    path('teacher_attendance/', views.TeacherAttendance, name='teacher_attendance'),
    path('teacher_take_attendance/<str:divisions>/',views.TeacherTakeAttendance,name='teacher_take_attendance'),
    path('teacher_view_attendance/<str:divisions>/',views.TeacherViewAttendance,name='teacher_view_attendance'),
    path('teacher_edite_profile/',views.TeacherEditeProfile,name="teacher_edite_profile"),

    # -------------------------- Admin ----------------------
    path('admin_click/', views.AdminClick, name='admin_click'),
    path('admin_signup/', views.AdminSingup, name='admin_signup'),
    path('admin_login/', views.AdminLogin, name='admin_login'),
    path('admin_panel/', views.AdminDashbord, name='admin_panel'),

    # ------------------------- Admin Student --------------------
    path('admin_student/', views.AdminStudent, name='admin_student'),
    path('admin_view_student/',views.AdminViewStudent,name='admin_view_student'),
    path('admin_add_student/',views.AdminAddStudent,name='admin_add_student'),
    path('admin_view_student_fees/',views.AdminViewStudentFees,name='admin_view_student_fees'),
    path('admin_approve_student/',views.AdminApproveStudent,name='admin_approve_student'),
    path('approve_student/<int:pk>/',views.ApproveStudent,name='approve_approve'),
    path('delete_student/<int:pk>/',views.DeleteStudent,name='delete_student'),
    path('update_student_school/<int:pk>/',views.UpdateStudentSchool,name='update_student_school'),
    path('delete_student_school/<int:pk>/',views.DeleteStudentSchool,name='delete_student_school'),

    # --------------------------- Admin Teacher --------------------
    path('admin_teacher/', views.AdminTeacher, name='admin_teacher'),
    path('admin_view_teacher/',views.AdminViewTeacher,name='admin_view_teacher'),
    path('admin_add_teacher/',views.AdminAddTeacher,name='admin_add_teacher'),
    path('admin_approve_teacher/',views.AdminApproveTeacher,name='admin_approve_teacher'),
    path('admin_view_teacher_salary/',views.AdminViewTeacherSalary,name='admin_view_teacher_salary'),
    path('update_teacher_school/<int:pk>/',views.UpdateTeacherSchool,name='update_teacher_school'),
    path('delete_teacher_school/<int:pk>/',views.DeleteTeacherSchool,name='delete_teacher_school'),
    path('approve_teacher/<int:pk>/',views.ApproveTeacher,name='approve_teacher'),
    path('delete_teacher/<int:pk>/',views.DelteTeacher,name='delete_teacher'),



    # ------------------------- Admin Others --------------------
    path('admin_fees/', views.AdminFees, name='admin_fees'),
    path('admin_salary/', views.AdminViewSalary, name='admin_salary'),
    path('admin_view_fees/<str:divisions>/',views.AdminViewFees,name='admin_view_fees'),
    path('admin_attendance/', views.AdminAttendance, name='admin_attendance'),
    path('admin_take_attendance/<str:divisions>/',views.AdminTakeAttendance,name='admin_take_attendance'),
    path('admin_view_attendance/<str:divisions>/',views.AdminViewAttendance,name='admin_view_attendance'),
    path('admin_notice/', views.AdminNotice, name='admin_notice'),
    path('admin_notice_delete/<int:pk>/',views.AdminDeleteNotice,name='admin_delete_notice')
]
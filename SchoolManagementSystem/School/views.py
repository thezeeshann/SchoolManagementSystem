from django.shortcuts import render, redirect,get_object_or_404
from .forms import UserForm, StudentForm, TeacherForm,NoticeForm,AttendanceForm,AskDateForm
from .models import User, Student, Teacher, Notice,Attendance
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.db.models import Q
from .utils import send_password_reset_email,send_verification_email
# verification
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
# Create your views here.


def IndexPage(request):
    return render(request, 'index.html')

# check role all user
def check_role_student(user):
    if user.role == 1:
        return True
    else:
        return PermissionDenied

def check_role_teacher(user):
    if user.role == 2:
        return True
    else:
        return PermissionDenied


def check_role_admin(user):
    if user.role == 3:
        return True
    else:
        return PermissionDenied
    
def sample_view(request):
    current_user = request.user
    if current_user.role == 1:
        messages.warning(request,'You are already logged in')
        return redirect('student_admin')
    if current_user.role == 2:
        messages.warning(request,'You are already logged in')
        return redirect('teacher_admin')
    else:
        messages.warning(request,'You are already logged in')
        return redirect('admin_panel')
# ----------------------- Email verification and Reset password ---------------------------------

def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated. Please Wait For Admin Approval')
        if user.role == 1:
            return redirect('studnet_login')
        if user.role == 2:
            return redirect('teacher_login')
        else:
            return redirect('admin_login')
    else:
        messages.error(request, 'Invalid activation link')
        if user is not None:
            if user.role == 1:
                    return redirect('studnet_login')
            if user.role == 2:
                return redirect('teacher_login')
            else:
                return redirect('admin_login')
        else:
            return redirect('index_page')


def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # reset email varificatioon
            send_password_reset_email(request,user)
            messages.success(request,'Password reset Link has been send to your email address')
            if user.role == 1:
                return redirect('studnet_login')
            if user.role == 2:
                return redirect('teacher_login')
            else:
                return redirect('admin_login')
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgot_password')
    return render(request,'email/forgot_password.html')


def ResetPasswordValidate(request,uidb64,token):
    # validate the user
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request,'This link has been expired')
        if user.role == 1:
                return redirect('studnet_login')
        if user.role == 2:
            return redirect('teacher_login')
        else:
            return redirect('admin_login')

def ResetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successful')
            if user.role == 1:
                return redirect('studnet_login')
            if user.role == 2:
                return redirect('teacher_login')
            else:
                return redirect('admin_login')
        else:
            messages.error(request,'Password do not match')
            return redirect('reset_password')
    else:
        return render(request,'email/reset_password.html')



#----------------------------------------------- Logout user ---------------------------------------------------------------
def LogoutView(request):
    user = request.user
    logout(request)
    messages.success(request,'You are logged out!')
    if user.role == 1:
        return redirect('studnet_login')
    if user.role == 2:
        return redirect('teacher_login')
    else:
        return redirect('admin_login')

# ------------------------------------------- Student -----------------------------------------------------------------------


def StudentClick(request):
    return render(request, 'student/student_click.html')


@login_required(login_url='studnet_login')
def StudentApprovedAccounts(request):
    return render(request, 'student/stu_accounts_approved.html')


def StudentSingup(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('student_admin')
    elif request.method == "POST":
        form = UserForm(request.POST)
        stu_form = StudentForm(request.POST,request.FILES)
        if form.is_valid() and stu_form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.role = User.STUDENT
            user.save()
            student = stu_form.save(commit=False)
            student.user = user
            student.save()

            # send verification email
            send_verification_email(request,user)
            messages.success(request, 'Your account has been registered successfully. Please verify your email address')
            
            form = UserForm()
            stu_form = StudentForm()
    else:
        form = UserForm()
        stu_form = StudentForm()
    context = {
        'form': form,
        'stu_form': stu_form
    }
    return render(request, 'student/student_singup.html', context)


def StudentLogin(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('student_admin')
    elif request.method == "POST":
        email = request.POST['email']
        print(email)
        password = request.POST['password']
        print(password)
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            if user.role == 1:
                login(request, user)
                accountapproval = Student.objects.all().filter(user_id=request.user.id, is_approved=True)
                if accountapproval:
                    messages.success(request,'Login Successful!')
                    return redirect('student_admin')
                else:
                    return redirect('student_approved_accounts')
            else:
                 messages.warning(request,'Sorry you are not allowed to access this page')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'student/student_login.html')


@login_required(login_url='studnet_login')
@user_passes_test(check_role_student)
def StudentAdmin(request):
    student = Student.objects.filter(user_id=request.user.id)
    notice = Notice.objects.all()
    context = {
        'student': student,
        'notice':notice
    }
    return render(request, 'student/student_admin.html', context)


@login_required(login_url='studnet_login')
@user_passes_test(check_role_student)
def StudentAttendance(request):
    student = Student.objects.filter(user_id=request.user.id)
    form = AskDateForm()
    if request.method == "POST":
        form = AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            student_data = Student.objects.get(user_id=request.user.id)
            student_attendance = Attendance.objects.filter(date=date).filter(Q(status__icontains="present") | Q(status__icontains="absent"), Q(student=student_data) )
            context = {
            'date':date,
            'student':student,
            'student_attendance':student_attendance
            }
            return render(request,'student/student_attendance_view.html',context)
        else:
            messages.error(request,'Please enter a valid date')
    else:
        return render(request,'student/student_attendance_ask_date.html',{'student':student,'form':form})
    return render(request,'student/student_attendance_ask_date.html',{'student':student,'form':form})


# ------------------------------------------- Teacher ------------------------------------------------------------------------


def TeacherClick(request):
    return render(request, 'teacher/teacher_click.html')


@login_required(login_url='teacher_login')
def TeacherApprovedAccounts(request):
    return render(request, 'teacher/teac_accounts_approved.html')


def TeacherSingup(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('teacher_admin')
    elif request.method == "POST":
        form = UserForm(request.POST)
        teac_form = TeacherForm(request.POST,request.FILES)
        if form.is_valid() and teac_form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.role = User.TEACHER
            user.save()
            teacher = teac_form.save(commit=False)
            teacher.user = user
            teacher.save()

            # send verification email
            send_verification_email(request,user)
            messages.success(request, 'Your account has been registered successfully. Please verify your email address')

            form = UserForm()
            teac_form = TeacherForm()
    else:
        form = UserForm()
        teac_form = TeacherForm()
    context = {
        'form':form,
        'teac_form':teac_form
    }
    return render(request, 'teacher/teacher_singup.html',context)


def TeacherLogin(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('teacher_admin')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.role == 2:
                login(request, user)
                accountapproval = Teacher.objects.all().filter(user_id=request.user.id, is_approved=True)
                if accountapproval:
                    messages.success(request,'Login Successful!')
                    return redirect('teacher_admin')
                else:
                    return redirect('teacher_approved_accounts')
            else:
                messages.warning(request,'Sorry you are not allowed to access this page')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'teacher/teacher_login.html')

@login_required(login_url='teacher_login')
@user_passes_test(check_role_teacher)
def TeacherAdmin(request):
    teacher = Teacher.objects.filter(user_id=request.user.id)
    notice = Notice.objects.all().order_by('-date')
    context = {
        'teacher': teacher,
        'notice':notice
    }
    return render(request, 'teacher/teacher_admin.html',context)


@login_required(login_url='teacher_login')
@user_passes_test(check_role_teacher)
def TeacherNotice(request):
    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            post_by = request.user
            data = Notice(message=message,post_by=post_by)
            data.save()
            return redirect('teacher_admin')
        else:
            messages.error(request,'Something Wrong')
    else:
        form = NoticeForm()
    teacher = Teacher.objects.filter(user_id=request.user.id)
    context = {
        'form':form,
        'teacher':teacher
    }
    return render(request,'teacher/teacher_notice.html',context)


@login_required(login_url='teacher_login')
@user_passes_test(check_role_teacher)
def TeacherDeleteNotice(request,pk):
    teacher_delete_notice = Notice.objects.get(id=pk)
    teacher_delete_notice.delete()
    return redirect('teacher_admin')


@login_required(login_url='teacher_login')
@user_passes_test(check_role_teacher)
def TeacherAttendance(request):
    teacher = Teacher.objects.filter(user_id=request.user.id)
    context = {
        'teacher':teacher
    }
    return render(request,'teacher/teacher_attendance.html',context)


@login_required(login_url='teacher_login')
@user_passes_test(check_role_teacher)
def TeacherTakeAttendance(request,divisions):
    teacher = Teacher.objects.filter(user_id=request.user.id)
    students = Student.objects.filter(divisions=divisions)
    attendance_form = AttendanceForm()
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = request.POST.getlist('status')
            date = form.cleaned_data['date']
            if not Attendance.objects.filter(date=date).exists():
                for i in range(len(attendance)):
                    attendance_model = Attendance()
                    attendance_model.date = date
                    attendance_model.status = attendance[i]
                    attendance_model.student = students[i]
                    attendance_model.save()
                return redirect('teacher_admin')
            else:
                messages.warning(request,'Attendance is done for this date')
        else:
            messages.error(request,'Plese entert a valid date')
    else:
        attendance_form = AttendanceForm()
    context = {
        'students':students,
        'divisions':divisions,
        'attendance_form':attendance_form,
        'teacher':teacher
    }
    return render(request,'teacher/teacher_take_attendance.html',context)



@login_required(login_url='teacher_login')
@user_passes_test(check_role_teacher)
def TeacherViewAttendance(request,divisions):
    teacher = Teacher.objects.filter(user_id=request.user.id)
    form = AskDateForm()
    if request.method == 'POST':
        form = AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            student_data = Student.objects.all().filter(divisions=divisions)
            student_attendance  = Attendance.objects.filter(date=date).filter(Q(status__icontains="present") | Q(status__icontains="absent"), Q(student__divisions=divisions))
            context={
                'date':date,
                'divisions':divisions,
                'student_attendance':student_attendance,
                'student_data':student_data,
                'teacher':teacher
            }
            return render(request,'teacher/teacher_view_attendance.html',context)
        else:
            messages.error(request,'Please enter a valid date')
    else:
        return render(request,'teacher/teacher_view_attendance_ask_date.html',{'divisions':divisions,'form':form,'teacher':teacher})
    return render(request,'teacher/teacher_view_attendance_ask_date.html',{'divisions':divisions,'form':form,'teacher':teacher})


@login_required(login_url='teacher_login')
@user_passes_test(check_role_teacher)
def TeacherEditeProfile(request):
    teacher = Teacher.objects.filter(user_id=request.user.id)
    teacher_profile = get_object_or_404(Teacher,user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = TeacherForm(request.POST,request.FILES,instance=teacher_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            teacher = profile_form.save(commit=False)
            teacher.user_form = user_form
            teacher.save()
            messages.success(request, 'Your profile has been updated.')
            # return redirect('teacher_admin')
        else:
            messages.error(request,"Something Wrong")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = TeacherForm(instance=teacher_profile)
    context = {
        'teacher':teacher,
        'user_form':user_form,
        'profile_form':profile_form
    }
    return render(request,'teacher/teacher_edite_profile.html',context)



# ------------------------------------------- Admin --------------------------------------------------------------------------


def AdminClick(request):
    return render(request, 'admin/admin_click.html')


@login_required(login_url='admin_login')
def AdminApprovedAccounts(request):
    return render(request, 'admin/adm_accounts_approved.html')


def AdminSingup(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('teacher_admin')
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.role = User.ADMIN
            user.save()
            messages.success(request, 'Your account has been registered successfully.')
            form = UserForm()
    else:
        form = UserForm()
    context = {
        'form':form
    }
    return render(request, 'admin/admin_signup.html',context)


def AdminLogin(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('admin_panel')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.role == 3:
                login(request, user)
                accountapproval = User.objects.all().filter(id=request.user.id,is_admin=True)
                if accountapproval:
                    messages.success(request,'Login Successful!')
                    return redirect('admin_panel')
                else:
                    messages.warning(request,' Your Account has not been approved yet!')
            else:
                messages.warning(request,'Sorry you are not allowed to access this page')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'admin/admin_login.html')



@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminDashbord(request):
    # teacher
    teachers_counts = Teacher.objects.all().filter(is_approved=True).count()
    teachers_salary = Teacher.objects.filter(is_approved=True).aggregate(Sum('salary'))
    pending_teacher = Teacher.objects.filter(is_approved=False).count()
    pending_teacher_salary = Teacher.objects.filter(is_approved=False).aggregate(Sum('salary'))
    # student
    student_count = Student.objects.all().filter(is_approved=True).count()
    student_fees = Student.objects.filter(is_approved=True).aggregate(Sum('fees'))
    pending_student = Student.objects.filter(is_approved=False).count()
    pending_student_fees = Student.objects.filter(is_approved=False).aggregate(Sum('fees'))
    # notice
    notice = Notice.objects.all().order_by('-date')
   
    

    context = {
        'teachers_counts':teachers_counts,
        'teachers_salary':teachers_salary['salary__sum'],
        'pending_teacher':pending_teacher,
        'pending_teacher_salary':pending_teacher_salary['salary__sum'],
        'student_count':student_count,
        'student_fees':student_fees['fees__sum'],
        'pending_student':pending_student,
        'pending_student_fees':pending_student_fees['fees__sum'],
        'notice':notice,


    }
    return render(request, 'admin/admin_panel.html',context)

# ----------------------------------------------------------- Admin Student --------------------------------------------------------

@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminStudent(request):
    return render(request, 'admin/student/admin_student.html')

    
@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminViewStudent(request):
    all_student = Student.objects.all().filter(is_approved=True)
    context = {
        'all_student':all_student
    }
    return render(request,'admin/student/admin_view_student.html',context)


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminAddStudent(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        stu_form = StudentForm(request.POST,request.FILES)
        if form.is_valid() and stu_form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.role = User.STUDENT
            user.save()
            student = stu_form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, 'Your account has been registered successfully.')
            form = UserForm()
            stu_form = StudentForm()
    else:
        form = UserForm()
        stu_form = StudentForm()
    context = {
        'form': form,
        'stu_form': stu_form
    }
    return render(request,'admin/student/admin_add_student.html',context)


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def UpdateStudentSchool(request,pk):
    if request.method == "POST":
        student = Student.objects.get(id=pk)
        user = User.objects.get(id=student.user_id)
        form = UserForm(request.POST,instance=user)
        stu_form = StudentForm(request.POST,instance=student)
        if form.is_valid() and stu_form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            student = stu_form.save(commit=False)
            student.form = form
            student.save()
            messages.success(request, 'Student Update successfully.')
        else:
            messages.error(request,'Something Wrong')
    else:
        student = Student.objects.get(id=pk)
        user = User.objects.get(id=student.user_id)
        form = UserForm(instance=user)
        stu_form = StudentForm(instance=student)
    context = {
        'form':form,
        'stu_form':stu_form
    }
    return render(request,'admin/student/admin_update_student.html',context)


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def DeleteStudentSchool(request,pk):
    student = Student.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin_view_student')


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminViewStudentFees(request):
    all_student_fees = Student.objects.all().filter(is_approved=True)
    context = {
        'all_student_fees':all_student_fees
    }
    return render(request,'admin/student/admin_view_student_fees.html',context)


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminApproveStudent(request):
    student_approve = Student.objects.all().filter(is_approved=False)
    context = {
        'student_approve':student_approve
    }
    return render(request,'admin/student/admin_approve_student.html',context)


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def ApproveStudent(request,pk):
    student = Student.objects.get(id=pk)
    student.is_approved = True
    student.save()
    return redirect('admin_approve_student')


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def DeleteStudent(request,pk):
    student = Student.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin_approve_student')

# --------------------------------------------------------- Admin Teacher -------------------------------------------------------------

@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminTeacher(request):
    return render(request, 'admin/teacher/admin_teacher.html')


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminViewTeacher(request):
    teacher = Teacher.objects.all().filter(is_approved=True)
    context = {
        'teacher':teacher
    }
    return render(request,'admin/teacher/admin_view_teacher.html',context)


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def UpdateTeacherSchool(request,pk):
    if request.method == "POST":
        teacher = Teacher.objects.get(id=pk)
        user = User.objects.get(id=teacher.user_id)
        form = UserForm(request.POST,instance=user)
        teac_form = TeacherForm(request.POST,instance=teacher)
        if form.is_valid() and teac_form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            teacher = teac_form.save(commit=False)
            teacher.form = form
            teacher.save()
            messages.success(request, 'Teacher Update successfully.')
        else:
            messages.error(request,'Something Wrong')
    else:
        teacher = Teacher.objects.get(id=pk)
        user = User.objects.get(id=teacher.user_id)
        form = UserForm(instance=user)
        teac_form = TeacherForm(instance=teacher)
    context = {
        'form':form,
        'teac_form':teac_form
    }
    return render(request,'admin/teacher/admin_update_teacher.html',context)


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def DeleteTeacherSchool(request,pk):
    teacher = Teacher.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)
    teacher.delete()
    user.delete()
    return redirect('admin_view_teacher')


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminAddTeacher(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        teac_form = TeacherForm(request.POST,request.FILES)
        if form.is_valid() and teac_form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.role = User.TEACHER
            user.save()
            teacher = teac_form.save(commit=False)
            teacher.user = user
            teacher.save()
            messages.success(request, 'Your account has been registered successfully.')
            form = UserForm()
            teac_form = TeacherForm()
    else:
        form = UserForm()
        teac_form = TeacherForm()
    context = {
        'form':form,
        'teac_form':teac_form
    }
    return render(request,'admin/teacher/admin_add_teacher.html',context)


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminApproveTeacher(request):
    teacher_approve = Teacher.objects.all().filter(is_approved=False)
    context= {
        'teacher_approve':teacher_approve
    }
    return render(request,'admin/teacher/admin_approve_teacher.html',context)


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def ApproveTeacher(request,pk):
    teacher = Teacher.objects.get(id=pk)
    teacher.is_approved = True
    teacher.save()
    return redirect('admin_approve_teacher')


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def DelteTeacher(request,pk):
    teacher = Teacher.objects.get(id=pk)
    user = User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin_approve_teacher')


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminViewTeacherSalary(request):
    teacher_salary = Teacher.objects.all().filter(is_approved=True)
    context = {
        'teacher_salary':teacher_salary
    }
    return render(request,'admin/teacher/admin_view_teacher_salary.html',context)


# ------------------------------------------- Fees -------------------------------------------------------------------------
@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminFees(request):
    return render(request, 'admin/other/admin_fees.html')


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminViewFees(request,divisions):
    student_fees = Student.objects.all().filter(divisions=divisions)
    context = {
        'student_fees':student_fees,
        'divisions':divisions
    }
    return render(request,'admin/other/admin_view_fees.html',context)


# ------------------------------------------ salary --------------------------------------------------------------------------
@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminViewSalary(request):
    teacher_salary = Teacher.objects.all().filter(is_approved=True)
    context = {
        'teacher_salary':teacher_salary
    }
    return render(request, 'admin/other/admin_view_salary.html',context)


# ------------------------------------------- Attendance -------------------------------------------------------------------
@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminAttendance(request):
    return render(request, 'admin/other/admin_attendance.html')

@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminTakeAttendance(request,divisions):
    students = Student.objects.filter(divisions=divisions)
    attendance_form = AttendanceForm()
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = request.POST.getlist('status')
            date = form.cleaned_data['date']
            if not Attendance.objects.filter(date=date).exists():
                for i in range(len(attendance)):
                    attendance_model = Attendance()
                    attendance_model.date = date
                    attendance_model.status = attendance[i]
                    attendance_model.student = students[i]
                    attendance_model.save()
                return redirect('admin_attendance')
            else:
                messages.warning(request,'Attendance is done for this date')
        else:
            messages.error(request,'Plese entert a valid date')
    else:
        attendance_form = AttendanceForm()
    context = {
        'students':students,
        'divisions':divisions,
        'attendance_form':attendance_form
    }
    return render(request,'admin/other/admin_take_attendance.html',context)


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminViewAttendance(request,divisions):
    form = AskDateForm()
    if request.method == 'POST':
        form = AskDateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            student_data = Student.objects.all().filter(divisions=divisions)
            student_attendance  = Attendance.objects.filter(date=date).filter(Q(status__icontains="present") | Q(status__icontains="absent"), Q(student__divisions=divisions))
            context={
                'date':date,
                'divisions':divisions,
                'student_attendance':student_attendance,
                'student_data':student_data
            }
            return render(request,'admin/other/admin_view_attendance.html',context)
        else:
            messages.error(request,'Please enter a valid date')
    else:
        return render(request,'admin/other/admin_view_attendance_ask_date.html',{'divisions':divisions,'form':form})
    return render(request,'admin/other/admin_view_attendance_ask_date.html',{'divisions':divisions,'form':form})



# ------------------------------------------- Notice -----------------------------------------------------------------------

@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminNotice(request):
    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            post_by = request.user
            data = Notice(message=message,post_by=post_by)
            data.save()
            return redirect('admin_panel')
        else:
            messages.error(request,'Something Wrong')
    else:
        form = NoticeForm()
    context = {
        'form':form
    }
    return render(request, 'admin/other/admin_notice.html',context)


@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminDeleteNotice(request,pk):
    delete_notice = Notice.objects.get(id=pk)
    delete_notice.delete()
    return redirect('admin_panel')
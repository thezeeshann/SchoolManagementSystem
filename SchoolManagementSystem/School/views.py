from django.shortcuts import render, redirect
from .forms import UserForm, StudentForm, TeacherForm
from .models import User, Student, Teacher, Notice,Attendance
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
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

# ------------------------------------------- Student -----------------------------------------------------------------------


def StudentClick(request):
    return render(request, 'student/student_click.html')


@login_required(login_url='studnet_login')
def StudentApprovedAccounts(request):
    return render(request, 'student/stu_accounts_approved.html')


def StudentSingup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        stu_form = StudentForm(request.POST)
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
    return render(request, 'student/student_singup.html', context)


def StudentLogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.role == 1:
                login(request, user)
                accountapproval = Student.objects.all().filter(
                user_id=request.user.id, is_approved=True)
                if accountapproval:
                    return redirect('student_admin')
                else:
                    return redirect('student_approved_accounts')
            else:
                 messages.warning(request,'Sorry you are not allowed to access this page')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'student/student_login.html')


# @login_required(login_url='studnet_login')
def StudentLogOut(request):
    logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('studnet_login')


@login_required(login_url='studnet_login')
@user_passes_test(check_role_student)
def StudentAdmin(request):
    student = Student.objects.filter(user_id=request.user.id)
    context = {
        'student': student
    }
    return render(request, 'student/student_admin.html', context)

# ------------------------------------------- Teacher ------------------------------------------------------------------------


def TeacherClick(request):
    return render(request, 'teacher/teacher_click.html')


@login_required(login_url='teacher_login')
def TeacherApprovedAccounts(request):
    return render(request, 'teacher/teac_accounts_approved.html')


def TeacherSingup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        teac_form = TeacherForm(request.POST)
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
    return render(request, 'teacher/teacher_singup.html',context)


def TeacherLogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.role == 2:
                login(request, user)
                accountapproval = Teacher.objects.all().filter(
                    user_id=request.user.id, is_approved=True)
                if accountapproval:
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
    context = {
        'teacher': teacher
    }
    return render(request, 'teacher/teacher_admin.html',context)

# @login_required(login_url='teacher_login')
def TeacherLogOut(request):
    logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('teacher_login')

# ------------------------------------------- Admin --------------------------------------------------------------------------


def AdminClick(request):
    return render(request, 'admin/admin_click.html')


@login_required(login_url='admin_login')
def AdminApprovedAccounts(request):
    return render(request, 'admin/adm_accounts_approved.html')


def AdminSingup(request):
    if request.method == "POST":
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
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.role == 3:
                login(request, user)
                accountapproval = User.objects.all().filter(id=request.user.id,is_admin=True)
                if accountapproval:
                    return redirect('admin_panel')
                else:
                    messages.warning(request,' Your Account has not been approved yet!')
            else:
                messages.warning(request,'Sorry you are not allowed to access this page')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'admin/admin_login.html')


@login_required(login_url='admin_login')
def AdminLogOut(request):
    logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('admin_login')


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
    notice = Notice.objects.all()

    context = {
        'teachers_counts':teachers_counts,
        'teachers_salary':teachers_salary['salary__sum'],
        'pending_teacher':pending_teacher,
        'pending_teacher_salary':pending_teacher_salary['salary__sum'],
        'student_count':student_count,
        'student_fees':student_fees['fees__sum'],
        'pending_student':pending_student,
        'pending_student_fees':pending_student_fees['fees__sum'],
        'notice':notice

    }
    return render(request, 'admin/admin_panel.html',context)

@login_required(login_url='admin_login')
def AdminStudent(request):
    return render(request, 'admin/admin_student.html')

@login_required(login_url='admin_login')
def AdminTeacher(request):
    return render(request, 'admin/admin_teacher.html',)


# ------------------------------------------- Fees -------------------------------------------------------------------------
@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminFees(request):
    return render(request, 'admin/admin_fees.html')


# ------------------------------------------- Attendance -------------------------------------------------------------------
@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminAttendance(request):
    return render(request, 'admin/admin_attendance.html')


# ------------------------------------------- Notice -----------------------------------------------------------------------

@login_required(login_url='admin_login')
@user_passes_test(check_role_admin)
def AdminNotice(request):
    # if request.method == "POST":
    #     form = NoticeForm(request.POST)
    #     print(form)
    #     if form.is_valid():
    #         form.save(commit=False)
    #         form.by = request.user.first_name
    #         form.save()
    #         form = NoticeForm()
    #         messages.success(request,'Your Message Successfully Send')
    #         return redirect('admin_panel')
    #     else:
    #         messages.error(request,'Something Wrong')
    # else:
    #     form = NoticeForm()
    # context = {
    #     'form':form
    # }
    return render(request, 'admin/admin_notice.html')

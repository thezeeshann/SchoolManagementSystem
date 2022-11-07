from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    STUDENT = 1
    TEACHER = 2
    ADMIN = 3

    ROLE_CHOICE = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (ADMIN, 'Admin'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICE, blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_role(self):
        if self.role == 1:
            user_role = 'Student'
        elif self.role == 2:
            user_role = 'Teacher'
        elif self.role == 3:
            user_role = 'Admin'
        return user_role


student_divisions = (
    ('one', 'One'),
    ('two', 'Two'),
    ('three', 'Three'),
    ('four', 'Four'),
    ('five', 'Five'),
    ('six', 'Six'),
    ('seven', 'Seven'),
    ('eight', 'Eight'),
    ('nine', 'Nine'),
    ('ten', 'Ten'),
)


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True)
    divisions = models.CharField(
        default='Division', choices=student_divisions, max_length=10)
    roll_no = models.PositiveIntegerField(null=True, blank=True)
    fees = models.PositiveIntegerField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    def full_name(self):
        return f'{self.user.first_name}, {self.user.last_name}'


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    def full_name(self):
        return f'{self.user.first_name}, {self.user.last_name}'


class Notice(models.Model):
    message = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    by = models.CharField(max_length=10)

    def __str__(self):
        return self.message


attendance_satus = (
    ('present', 'Present'),
    ('absent', 'Absent'),
)


class Attendance(models.Model):
    roll_no = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=attendance_satus,
                              default='present', max_length=10)

    def __str__(self):
        return self.roll_no
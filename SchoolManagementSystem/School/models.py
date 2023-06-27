from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
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
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
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


STUDENT_DIVISIONS = (
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

GENDER_CHOICES = (
    ("male", "Male"), 
    ("female", "Female")
)


FEES = (
    (1000,"1,000"),
    (2000,"2,000"),
    (3000,"3,000"),
    (4000,"4,000"),
    (5000,"5,000"),
    (6000,"6,000"),
    (7000,"7,000"),
    (8000,"8,000"),
    (9000,"9,000"),
    (10000,"10,000"),
)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='student/profile_pictures',blank=True,null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    phone_number = models.IntegerField(null=False, blank=False)
    divisions = models.CharField(default='Division', choices=STUDENT_DIVISIONS, max_length=10)
    roll_no = models.PositiveIntegerField(null=False, blank=False)
    fees = models.PositiveIntegerField(choices=FEES, default="1000",null=False, blank=False)
    is_approved = models.BooleanField(default=False)



    def __str__(self):
        return str(self.user.first_name)

    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='teacher/profile_pictures',blank=True,null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    phone_number = models.IntegerField(null=False, blank=False)
    salary = models.PositiveIntegerField(null=False, blank=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Notice(models.Model):
    message = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    post_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.post_by)

    def __str__(self):
        return self.message
    

attendance_satus = (
    ('present', 'Present'),
    ('absent', 'Absent'),
)


class Attendance(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField()
    status = models.CharField(choices=attendance_satus,default='present', max_length=10)

    def __str__(self):
        return str(self.student)

    def __str__(self):
        return self.status
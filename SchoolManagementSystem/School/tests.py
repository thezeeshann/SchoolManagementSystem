from django.test import TestCase
from .models import User,Notice,Attendance
# Create your tests here.


class UserTest(TestCase):
    def create_user(self,first_name="demo",last_name="test",username="demo",email="demo_test@gmail.com",role=1):
        return User.objects.create(first_name=first_name,last_name=last_name,username=username,email=email,role=role)
    
    def test_user(self):
        obj = self.create_user()
        self.assertTrue(isinstance(obj,User))
        self.assertEqual(obj.full_name(),obj.first_name+" "+obj.last_name)
        print("User created successfully : ",obj)



class NoticeTest(TestCase):    
    def test_model_notice(self):
        message = Notice.objects.create(message="demo notice")
        self.assertEqual(str(message),"demo notice")


class AttendanceTest(TestCase):
    def test_model_attendance(self):
        status = Attendance.objects.create(status="present")
        self.assertEqual(str(status),"present")


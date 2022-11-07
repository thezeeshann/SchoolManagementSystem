from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('School.urls'))
]

admin.site.site_header = "School Management System"
admin.site.index_title = "Welcome To School Management System Admin Panel "
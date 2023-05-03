from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('School.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "School Management System"
admin.site.index_title = "Welcome To School Management System Admin Panel "

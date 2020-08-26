from admindash.admin import admin

from django.urls import path, include

urlpatterns = [
    path('admin/', include('admindash.urls', namespace='admindash')),
    path('admin/', admin.urls),
]

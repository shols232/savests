from django.urls import path
from . import views

app_name='admindash'

urlpatterns = [
    path('send_email/', views.send_email, name='send_email'),
    path('toggle_active/<int:id>', views.toggle_user_activity, name='toggle_user_activity'),
    path('toggle_admin/<int:id>', views.toggle_admin, name='toggle_admin')
]

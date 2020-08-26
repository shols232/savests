from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite
from itertools import zip_longest
from django.urls import reverse
import datetime
from .views import toggle_user_activity
from django.urls import path
import pytz

utc=pytz.UTC

class MyAdminSite(AdminSite):
    index_template = 'admin/admindash/index.html'
    site_header = 'Savests admin'
    site_title = 'Savests admin'
    index_title = 'Savests administration'

    def index(self, request, extra_context=None):
        date_past_24_hours = datetime.datetime.now() - datetime.timedelta(days=1)
        date_past_month = datetime.datetime.now() - datetime.timedelta(days=30)
        date_past_year = datetime.datetime.now() - datetime.timedelta(days=365)
        extra_context = extra_context or {}
        last_24_hours = []
        last_month = []
        last_year = []
        admins = []
        staff = []
        non_staff = []
        for user in User.objects.all():
            if user.date_joined != None:
                if user.date_joined.replace(tzinfo=utc) >= date_past_24_hours.replace(tzinfo=utc):
                    last_24_hours.append(user)
                elif user.date_joined >= date_past_month.replace(tzinfo=utc):
                    last_month.append(user)
                elif user.date_joined >= date_past_year.replace(tzinfo=utc):
                    last_year.append(user)
                if user.is_superuser:
                    admins.append(user)
                    staff.append(user)
                elif user.is_staff:
                    staff.append(user)
                elif user.is_staff == False:
                    non_staff.append(user)
        user_status = []

        for admin, staf, non_staf in zip_longest(admins, staff, non_staff, fillvalue=''):
            user_status.append({'admin':admin, 'staff':staf, 'non_staff': non_staf})

        extra_context['last_24_hours'] = last_24_hours
        extra_context['last_month'] = last_month
        extra_context['last_year'] = last_year
        extra_context['user_status'] = user_status

        return super(MyAdminSite, self).index(request, extra_context=extra_context)

admin = MyAdminSite(name='myadmin')

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'active', 'toggle_active', 'admin', 'toggle_admin')

    change_list_template='admin/admindash/user_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('toggle_user_activity', toggle_user_activity, name='toggle_user_activity')
        ]
        return custom_urls + urls

    def toggle_active(self, obj):
        action = 'Deactivate'
        if obj.is_active != 1:
            action='Activate'
        return format_html(
            '<a class="button" href="%s">%s</a>&nbsp;' %
            (reverse('admindash:toggle_user_activity', args=[obj.pk]), action)
        )

    def toggle_admin(self, obj):
        action = 'Strip Admin'
        if obj.is_superuser != 1:
            action = 'Make Admin'

        return format_html(
            '<a class="button" href="%s">%s</a>&nbsp;' %
            (reverse('admindash:toggle_admin', args=[obj.pk]), action)
        )
    def active(self, obj): 
        return obj.is_active == 1

    def admin(self, obj): 
        return obj.is_superuser == 1
  
    active.boolean = True
    admin.boolean = True

admin.register(User, CustomUserAdmin)

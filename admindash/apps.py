from django.apps import AppConfig


class AdminConfig(AppConfig):
    default_site = 'savest.admindash.admin.MyAdminSite'
    name = 'admindash'

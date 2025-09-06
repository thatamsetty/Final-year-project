from django.contrib import admin
from django.urls import path,include
from app.views import *
urlpatterns = [
    path('',index,name='index' ),
    path('admin_login/', admin_login,name='admin_login'),
    path('department_login/',department_login,name='department_login'),
    path('logout/',logout,name='logout'),
    path('add_department/',add_department, name='add_department'),
    path('manage_department/',manage_department,name='manage_department'),
    path('add_faculty/',add_faculty,name='add_faculty'),
    path('add_subject/',add_subject,name='add_subject'),
    path('department_dashboard/',department_dashboard,name='department_dashboard'),
    path('dashboard/',dashboard,name='dashboard'),
    path('generate_timetable/',generate_timetable,name='generate_timetable'),
    path('view_table/',view_table,name='view_table'),
    path('department_logout/',department_logout,name='department_logout'),
    path('edit/<int:department_id>/', edit_department, name='edit_department'),
    path('delete/<int:department_id>/', delete_department, name='delete_department')
]
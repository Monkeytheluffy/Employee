from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('employee-list/', views.employee_list, name='employee_list'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('edit-employee/<employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete-employee/<str:employee_id>/', views.delete_employee, name='delete_employee'),
]

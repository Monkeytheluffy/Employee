from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from pymongo import MongoClient
from employees.models import Department, Employee
from .forms import EmployeeForm
from bson.objectid import ObjectId 

myClient = MongoClient("mongodb://localhost:27017")
mydatabase = myClient['Employee_Management']
employee_collection = mydatabase['Employee']

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('employee_list')
        else:
            return render(request, 'employees/login.html', {'error': 'Invalid credentials or not an admin'})
    return render(request, 'employees/login.html')


def admin_logout(request):
    logout(request)
    return redirect('login')


@login_required
def employee_list(request):
    employees = list(employee_collection.find()) 
    for employee in employees:
        employee['id'] = str(employee['_id']) 
    return render(request, 'employees/employee_list.html', {'employees': employees})


@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            
            department = form.cleaned_data['department']
            if isinstance(department, Department): 
                department_name = department.name 
            else:
                department_name = department 

         
            employee_data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'position': form.cleaned_data['position'],
                'department': department_name,  
            }

            try:
                employee_collection.insert_one(employee_data)
                return redirect('employee_list')
            except Exception as e:
                print(f"Error inserting employee into MongoDB: {e}")
                return render(request, 'employees/add_employee.html', {'form': form, 'error': 'Failed to save employee data'})
    else:
        form = EmployeeForm()
    return render(request, 'employees/add_employee.html', {'form': form})


@login_required
def edit_employee(request, employee_id):
    try:
        employee_data = employee_collection.find_one({'_id': ObjectId(employee_id)})
        if not employee_data:
            return redirect('employee_list') 
    except Exception as e:
        print(f"Error fetching employee: {e}")
        return redirect('employee_list')
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            department = form.cleaned_data['department']
            department_name = department.name if isinstance(department, Department) else department

            updated_employee = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'position': form.cleaned_data['position'],
                'department': department_name, 
            }

            try:
                employee_collection.update_one(
                    {'_id': ObjectId(employee_id)},
                    {'$set': updated_employee}
                )
                return redirect('employee_list')
            except Exception as e:
                print(f"Error updating employee: {e}")
    else:
    
        initial_data = {
            'name': employee_data['name'],
            'email': employee_data['email'],
            'phone': employee_data['phone'],
            'position': employee_data['position'],
            'department': employee_data.get('department', ''),
        }
        form = EmployeeForm(initial=initial_data)

    return render(request, 'employees/edit_employee.html', {'form': form})


@login_required
def delete_employee(request, employee_id):
    try:
        employee_collection.delete_one({'_id': ObjectId(employee_id)}) 
    except Exception as e:
        print(f"Error deleting employee: {e}")
        return redirect('employee_list') 
    return redirect('employee_list')

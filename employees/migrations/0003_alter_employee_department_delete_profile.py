# Generated by Django 5.1.3 on 2024-11-23 14:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_alter_employee_department_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.department'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]

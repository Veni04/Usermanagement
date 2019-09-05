from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # note that 'many-to-many (i.e. authors)' field can not be displayed

    search_fields = ['eid','ename','econtact','eemail']

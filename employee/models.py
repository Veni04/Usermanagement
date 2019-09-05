from django.db import models
from mongoengine import *

from django.core.exceptions import ValidationError



class Employee(models.Model):
    dept = (
        ('d009', 'Customer Service'),
        ('d005', 'Development'),
        ('d002', 'Finance'),
        ('d003', 'Human Resources'),
        ('d001', 'Marketing'),
        ('d004', 'Production'),
        ('d006', 'Quality Management'),
        ('d008', 'Research'),
        ('d007', 'Sales')
    )
    sal = (
        ('Staff', 'Staff'),
        ('SeniorStaff', 'SeniorStaff'),
        ('AssistantEngineer', 'AssistantEngineer'),
        ('Engineer', 'Engineer'),
        ('SeniorEngineer', 'SeniorEngineer'),
        ('TechniqueLead', 'TechniqueLead'),
        ('Manger', 'Manger')

    )
    gender = (
        ('M', 'M'),
        ('F', 'F')
    )
    tit = {
        'Staff': '3L',
        'SeniorStaff':'5L',
        'AssistantEngineer': '7L',
        'Engineer': '9L',
        'SeniorEngineer': '12L',
        'TechniqueLead': '20L',
        'Manger': '30L'
    }

    def validate_dob(value):
        if value < 1959 or value > 2100:
            raise ValidationError(u'%s You should between 18-60 age range!' % value)

    def validate_hire_date(value):
        if value < 2015 or value > 2100:
            raise ValidationError(u'%s Please Enter Correct HireDate From 2015!' % value)
    eid = models.IntegerField()

    edob = models.CharField(max_length=50,validators=[validate_dob])
    egender = models.CharField(max_length=50,choices=gender)
    efistname = models.CharField(max_length=50)
    ehiredate = models.CharField(max_length=50,validators=[validate_hire_date])
    elastname = models.CharField(max_length=50)
    erole = models.CharField(max_length=69, choices=sal)
    esalary = models.IntegerField()
    dept = models.CharField(max_length=6, choices=dept)
    salary = models.IntegerField()


   




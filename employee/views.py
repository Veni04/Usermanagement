from django.shortcuts import render, redirect

from employee.models import Employee
from employee.forms import EmployeeForm
import datetime

import pymysql
from rest_framework import generics

from .connect import cursor
from .serializers import UserSerializer
from dateutil.relativedelta import relativedelta


class PostList(generics.ListAPIView):
    dep = {
        'Customer Service': 'd009',
        'Development': 'd005',
        'Finance': 'd002',
        'Human Resources': 'd003',
        'Marketing': 'd001',
        'Production': 'd004',
        'Quality Management': 'd006',
        'Research': 'd008',
        'Sales': 'd007'
    }

    # Open database connection
    db = pymysql.connect(host="localhost", user="veni", password="veni#123", db="employee", charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()


    queryset = Employee.objects.all()
    serializer_class = UserSerializer
    esult = Employee.objects.values()
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    list_result = [entry for entry in esult]  # converts ValuesQuerySet into Python list
    for e in list_result:
        if "int" in str(type(e.get('eid'))):
            ehiredate = datetime.datetime.strptime(e.get('ehiredate'), '%Y-%m-%d').date()
            now = datetime.datetime.now()
            difference_hire = relativedelta(now, ehiredate)
            exp= int(difference_hire.years)
            edob = datetime.datetime.strptime(e.get('edob'), '%Y-%m-%d').date()
            difference_age = relativedelta(now, edob)
            age = int(difference_age.years)
            try:
                cursor.execute("INSERT INTO `employee`.`employees`(`emp_no`,`birth_date`,`first_name`,`last_name`,"
                               "`gender`,`hire_date`,`Exp`,`Age`)VALUES(%d,'%s','%s','%s','%s','%s',%d,%d)"%(int(e.get(
                    'eid')),
                                                                                              e.get('edob'),
                                                                    e.get('efistname'),e.get('elastname'),
                                                                    e.get('egender'), e.get('ehiredate'),int(exp),
                                                                                                             int(age)))
            except Exception as e:print(e)

            try:
                cursor.execute("INSERT INTO `employee`.`dept_emp`(`emp_no`,`dept_no`,`from_date`,`to_date`)VALUES(%d,%d,"
                           "'%s','%s')" % (int(e.get('eid')), int(dep.get(e.get('dept'))),
                e.get('ehiredate'),today_date))
            except Exception as e: print(e)

            try:
                cursor.execute("INSERT INTO `employee`.`dept_emp`(`emp_no`,`dept_no`,`from_date`,`to_date`)VALUES(%d,"
                               "%d,"
                           "'%s','%s')" % (int(e.get('eid')), int(dep.get(e.get('dept'))),
                                       e.get('ehiredate'), today_date))
            except Exception as e: print(e)
            try:

                 cursor.execute("INSERT INTO `employee`.`salaries`(`emp_no`,`salary`,`from_date`,`to_date`)VALUES(%d,%d,'%s',"
                            "'%s')"%(int(e.get('eid')),int(e.get('salary')),e.get('ehiredate'),e.get('ehiredate')))
            except Exception as e:
                print(e)

            try:

                 cursor.execute("INSERT INTO `employee`.`titles`(`emp_no`,`title`,`from_date`,`to_date`)VALUES(%d,%s,"
                                "'%s',"
                            "'%s')"%(int(e.get('eid')),(e.get('role')),e.get('ehiredate'),e.get('ehiredate')))
            except Exception as e: print(e)


class PostDetail(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = UserSerializer




def emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        form = EmployeeForm()
    return render(request,'index.html',{'form':form})
def show(request):

    employees = Employee.objects.all()
    #return JsonResponse("Ideal weight should be:" + str(employees) + " kg", safe=False)
    return render(request,"show.html",{'employees':employees})

def employee_hike(request):
    Hike = []
    tit = {
        'Staff': '3L',
        'SeniorStaff': '5L',
        'AssistantEngineer': '7L',
        'Engineer': '9L',
        'SeniorEngineer': '12L',
        'TechniqueLead': '20L',
        'Manger': '30L'
    }
    select1 = cursor.execute("SELECT a.emp_no FROM employee.dept_emp a inner join titles b on a.emp_no=b.emp_no where a.dept_no not in ('d009','d005','d003','d002','d007') and b.title not in ('SeniorEngineer','Staff','Engineer','SeniorStaff', 'AssistantEngineer', 'TechniqueLeader')")

    if select1>0:
        empnoList = cursor.fetchall()
        for row in empnoList:
            select2 = cursor.execute("SELECT emp_no From employee.employees where Exp<=1 and Age<=20 and emp_no ="+
                                     row['emp_no']+" ")
            if select2>0:
                empnoList2 = cursor.fetchall()
                for row2 in empnoList2:
                    print(row2["emp_no"])
                    select2 = cursor.execute(
                        "SELECT a.emp_no,b.title FROM employee.employees a inner join titles b on a.emp_no=b.emp_no "
                        "where "
                        "a.Gender='M' and "
                        "emp_no ="+ row2['emp_no'] + "and b.title ='TechniqueLeader' " )

                    if select2>0:
                        empnoList3 = cursor.fetchall()
                        for row3 in empnoList3:
                            print(row3["emp_no"])
                        Hike.append({"hike":"True","desg":row3["title"]})
                        index_key= tit.keys().index(row3["title"])

                        try:
                            cursor.execute("Update `title` set title = "+tit[index_key+1] +"where emp_no = row3["
                                           "'emp_no'] ")
                        except:pass
                    else:
                        Hike.append({"hike": "False"})
            else:
                Hike.append({"hike": "False"})
    else:
        Hike.append({"hike": "False"})

    return Hike


# def search(request):
#     if request.method == 'GET':
#         #query= request.GET.get('q')
#
#         Hike = []
#         tit = {
#             'Staff': '3L',
#             'SeniorStaff': '5L',
#             'AssistantEngineer': '7L',
#             'Engineer': '9L',
#             'SeniorEngineer': '12L',
#             'TechniqueLead': '20L',
#             'Manger': '30L'
#         }
#         select1 = cursor.execute(
#             "SELECT a.emp_no FROM employee.dept_emp a inner join titles b on a.emp_no=b.emp_no where a.dept_no not in ('d009','d005','d003','d002','d007') and b.title not in ('SeniorEngineer','Staff','Engineer','SeniorStaff', 'AssistantEngineer', 'TechniqueLeader')")
#
#         if select1 > 0:
#             empnoList = cursor.fetchall()
#             for row in empnoList:
#                 print(row["emp_no"])
#                 select2 = cursor.execute(
#                     "SELECT emp_no From employee.employees where Exp<=1 and Age<=20 and emp_no = row['emp_no'] ")
#                 if select2 > 0:
#                     empnoList2 = cursor.fetchall()
#                     for row2 in empnoList2:
#                         print(row2["emp_no"])
#                         select2 = cursor.execute(
#                             "SELECT a.emp_no,b.title FROM employee.employees a inner join titles b on a.emp_no=b.emp_no "
#                             "where "
#                             "a.Gender='M' and "
#                             "emp_no = row2["
#                             "'emp_no'] and b.title ='TechniqueLeader' ")
#                         if select2 > 0:
#                             empnoList3 = cursor.fetchall()
#                             for row3 in empnoList3:
#                                 print(row3["emp_no"])
#                             Hike.append({"hike": "True", "desg": row3["title"]})
#                             index_key = tit.keys().index(row3["title"])
#
#                             try:
#                                 cursor.execute("Update `title` set title = tit[index_key+1] where emp_no = row3["
#                                                "'emp_no'] ")
#                             except:
#                                 pass
#                         else:
#                             Hike.append({"hike": "False"})
#                 else:
#                     Hike.append({"hike": "False"})
#         else:
#             Hike.append({"hike": "False"})
#
#         return Hike
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import pandas as pd
import os
from random import randint
import shutil

@csrf_protect
def search_form(request):
    return render(request, 'ques.html')

@csrf_protect
def search(request):
    print(request)
    print(request.method)
    if request.method == "POST":
        ques = request.POST['ques']
        marks = request.POST['marks']
        level = request.POST['level']
        BASE_DIR = os.getcwd()+"/QuesList.csv"
        my_dict = {"Ques":[ques],"Marks":[marks],"Level":[level]}
        df = pd.DataFrame.from_dict(my_dict, orient='columns')
        if not os.path.exists(BASE_DIR):
            df.to_csv(BASE_DIR,index=False)
        df.to_csv(BASE_DIR, mode='a', header=False,index=False)

    return HttpResponse("Question Added")

@csrf_protect
def paperGen_form(request):
    return render(request, 'paperGen.html')

def paperGen(request):
    totalmarks = int(request.POST['totalmarks'])

    easylevel = int(request.POST['easylevel'])
    mediumlevel = int(request.POST['mediumlevel'])
    hardlevel = int(request.POST['hardlevel'])
    if  (easylevel + mediumlevel + hardlevel)>100 or (easylevel + mediumlevel + hardlevel)<100:
        return HttpResponse("Invalid Selection of Levels")

    easyPer = int(easylevel/100*totalmarks)
    mediumPer = int(mediumlevel / 100 * totalmarks)
    hardPer = int(hardlevel / 100 * totalmarks)

    BASE_DIR = os.getcwd() + "/QuesList.csv"
    copy_data = shutil.copy(BASE_DIR,os.getcwd() + "/QuesList_temp.csv")
    data = pd.read_csv(copy_data)

    file = open(os.getcwd() + "/QuesPaper.txt","a")

    def sequence(n):

        a, m, c = [], randint(1, n), n
        while n > m > 0:
            a.append((m))
            n -= m
            m = randint(0, n)
        if n: a += [(n)]
        return a

    levels = ['easy','medium','hard']
    perc = [easyPer,mediumPer,hardPer]

    for j in range(len(perc)):
        level_list = []
        for i in range(len(perc)):
            level_list.append(sequence(perc[j]))
        level_list= list(set(tuple(sorted(sub)) for sub in level_list))
        for l in level_list:
            d =data[data['Level'] == levels[j]]
            # print(all(elem in d['Marks'].tolist()  for elem in l))
            if all(elem in d['Marks'].tolist()  for elem in l):
                for item in range(len(l)):
                    writeData = d[d['Marks']==l[item]]
                    file.write(str(writeData['Ques'].tolist())+str(writeData['Marks'].tolist())+"\n")
                    data.drop(writeData.index[writeData['Marks']==l[item]])

                    # l.pop(item)
            else:
                return HttpResponse("Not all possible questions present.Only Few or No questions added. Please add the "
                                    "Question "
                                    "with "
                                    "relevent marks "
                                    "and level or Try again!!!"+"\n\n "+"File Path:"+str(os.getcwd() + "/QuesPaper.txt"))

    return HttpResponse(easylevel)
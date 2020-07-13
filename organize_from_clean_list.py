import time
import os
import shutil

places=[]
count=0
with open('clean_list_128Vec_WT051_P010.txt', 'r') as filehandle:
    filecontents = filehandle.readlines()

    for line in filecontents:
        # remove linebreak which is the last character of the string
        current_place = line[:-1]
        spl=current_place.split(' ')
        spl[1]="G:/machine learning/Celeb 1 M/"+spl[1]
        places.append(spl)


for i in range(len(places)):
    origin=places[i][1]
    destination="G:/machine learning/Celeb 1M cleaned no relabeling/"+places[i][0]+"/"+str(i)+".jpg"
    directory="G:/machine learning/Celeb 1M cleaned no relabeling/"+places[i][0]+"/"
    os.makedirs(directory, exist_ok=True)
    newPath = shutil.copyfile(origin, destination)
    if i%1000==0:
        print(str(i),str(i/(len(places)-1))+"%")

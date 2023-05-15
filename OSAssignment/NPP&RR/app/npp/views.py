from django.shortcuts import render
from django.views.generic import ListView
import pandas as pd
# Create your views here.
    
def home(request):
    return render(request, 'home.html')

def getnpp(request):
    processes = request.GET.get("processes",'')
    arrivaltimeslist = request.GET.get("arrivaltimeslist",'')
    bursttimeslist = request.GET.get("bursttimeslist",'')
    prioritylist = request.GET.get("prioritylist",'')
    
    originalprocesseslist = processes.split()
    processeslist = processes.split()
    arrivallist = [int(num) for num in arrivaltimeslist.split()]
    burstlist = [int(num) for num in bursttimeslist.split()]
    plist = [int(num) for num in prioritylist.split()]
    
    while (len(processeslist) != len(arrivallist) or len(processeslist) != len(burstlist) or len(processeslist) != len(plist)):
        return render(request, 'home.html', {'errormessage':'Invalid Input!'})
    
    processeslist, arrivallist, burstlist, plist = rearrangelist(processeslist, arrivallist, burstlist, plist)
    
    finishedjob, finishedjob_arrival, finishedjob_burst, finishing_time, turnaround_time, waiting_time = calcAllTime(processeslist,arrivallist,burstlist,plist)
    npp_table = drawtable(originalprocesseslist, finishedjob, finishedjob_arrival, finishedjob_burst, finishing_time, turnaround_time, waiting_time)
    
    npp = pd.DataFrame.from_dict(npp_table)
    column_name = list(npp.columns)
    values = list(npp.values)
    
    totaltt, avgtt = calturnaroundtime(originalprocesseslist,turnaround_time)
    totalwt, avgwt = calwaitingtime(originalprocesseslist,waiting_time)
    
    return render(request, 'result.html', {"column_name": column_name, "values": values, "totaltt": totaltt, "avgtt":avgtt, "totalwt": totalwt, "avgwt":avgwt, "finishedjob":finishedjob, "firstfinishedjob_arrival":finishedjob_arrival[0], "finishing_time":finishing_time})

def rearrangelist(processeslist, arrivallist, burstlist, plist):
    for i in range(0, len(processeslist)):
        for j in range(i+1, len(processeslist)):
            if(arrivallist[i] > arrivallist[j]):
                tempp = plist[i]
                temparr = arrivallist[i]
                tempprocess = processeslist[i]
                tempbur = burstlist[i]
                            
                plist[i] = plist[j] 
                arrivallist[i] = arrivallist[j]
                processeslist[i] = processeslist[j]
                burstlist[i] = burstlist[j]
                            
                plist[j] = tempp
                arrivallist[j] = temparr
                processeslist[j] = tempprocess
                burstlist[j] = tempbur    
                  
            elif(arrivallist[i] == arrivallist[j]):
                if (plist[i] > plist[j]):
                    temparr = arrivallist[i]
                    tempprocess = processeslist[i]
                    tempbur = burstlist[i]
                    tempp = plist[i]
                        
                    arrivallist[i] = arrivallist[j]
                    processeslist[i] = processeslist[j]
                    burstlist[i] = burstlist[j]
                    plist[i] = plist[j]
                    
                    arrivallist[j] = temparr
                    processeslist[j] = tempprocess
                    burstlist[j] = tempbur
                    plist[j] = tempp
    return processeslist, arrivallist, burstlist, plist

def reaarangereadyqueue(readyQueueprocess,readyQueuearrival,readyQueueburst,readyQueuepriority):
    for i in range(0, len(readyQueueprocess)):
        for j in range(i+1,len(readyQueueprocess)):
            if (readyQueuepriority[i] > readyQueuepriority[j]):
                tempprocess = readyQueueprocess[i]
                tempp = readyQueuepriority[i]
                tempbur = readyQueueburst[i]
                temparr = readyQueuearrival[i]
                           
                readyQueueprocess[i] = readyQueueprocess[j] 
                readyQueuepriority[i] = readyQueuepriority[j] 
                readyQueueburst[i] = readyQueueburst[j]
                readyQueuearrival[i] = readyQueuearrival[j]
                            
                readyQueueprocess[j] = tempprocess
                readyQueuepriority[j] = tempp
                readyQueueburst[j] = tempbur
                readyQueuearrival[j] = temparr
    return readyQueueprocess,readyQueuearrival,readyQueueburst,readyQueuepriority
    
def calcAllTime(processeslist,arrivallist,burstlist,plist):
    tempburstlist = burstlist
    
    finishing_time =[]
    turnaround_time=[]
    waiting_time=[]
    finishedjob =[]
    finishedjob_arrival =[]
    finishedjob_burst =[]
    
    readyQueueprocess =[]
    readyQueuearrival =[]
    readyQueueburst =[]
    readyQueuepriority =[]
    
    for i in range(0, len(processeslist)):
        if i == 0:
            finishedjob.append(processeslist[i])
            finishedjob_burst.append(burstlist[i])
            finishedjob_arrival.append(arrivallist[i])
            finishing_time.append(arrivallist[i] + burstlist[i])
            turnaround_time.append(finishing_time[i] - arrivallist[i])
            waiting_time.append(turnaround_time[i] - burstlist[i])
            tempburstlist[i] = 0    
        else:
            if (len(readyQueueprocess) == 0):
                finishedjob.append(processeslist[i])
                finishing_time.append(finishing_time[i-1] + burstlist[i])
                turnaround_time.append(finishing_time[i] - arrivallist[i])
                waiting_time.append(turnaround_time[i] - burstlist[i])
                finishedjob_burst.append(burstlist[i])
                finishedjob_arrival.append(arrivallist[i])
                tempburstlist[i] = 0
            else:
                readyQueueprocess,readyQueuearrival,readyQueueburst,readyQueuepriority = reaarangereadyqueue(readyQueueprocess,readyQueuearrival,readyQueueburst,readyQueuepriority)
                finishedjob.append(readyQueueprocess[0])
                finishing_time.append(finishing_time[i-1] + readyQueueburst[0])
                turnaround_time.append(finishing_time[i] - readyQueuearrival[0])
                waiting_time.append(turnaround_time[i] - readyQueueburst[0])
                finishedjob_burst.append(readyQueueburst[0])
                finishedjob_arrival.append(readyQueuearrival[0])

                index = processeslist.index(readyQueueprocess[0])
                tempburstlist[index] = 0
                
                readyQueueprocess.pop(0)
                readyQueuearrival.pop(0)
                readyQueueburst.pop(0)
                readyQueuepriority.pop(0)
                      
        for j in range(i+1, len(processeslist)):
            if (arrivallist[j]<=finishing_time[i]):
                if (tempburstlist[j] != 0):
                    readyQueueprocess.append(processeslist[j])
                    readyQueuearrival.append(arrivallist[j])
                    readyQueueburst.append(burstlist[j])
                    readyQueuepriority.append(plist[j])
                    tempburstlist[j] = 0

    return finishedjob, finishedjob_arrival, finishedjob_burst, finishing_time, turnaround_time, waiting_time
                        
    
def drawtable(originalprocesseslist, finishedjob, finishedjob_arrival, finishedjob_burst, finishing_time, turnaround_time, waiting_time ):
    processesl=[]
    table_at = []
    table_bt =[]
    table_ft = []
    table_tt = []
    table_wt = []
    
    for i in range(0, len(originalprocesseslist)):
        index = finishedjob.index(originalprocesseslist[i])
        processesl.append(finishedjob[index])
        table_at.append(finishedjob_arrival[index])
        table_bt.append(finishedjob_burst[index])
        table_ft.append(finishing_time[index])  
        table_tt.append(turnaround_time[index])
        table_wt.append(waiting_time[index])
        
    npp_table = { 'PROCESS' : processesl,
                  'ARRIVAL TIME' : table_at,
                  'BURST TIME' : table_bt,
                  'FINISHING TIME' : table_ft,
                  'TURNAROUND TIME' : table_tt,
                  'WAITING TIME' : table_wt }
    return npp_table

def calturnaroundtime(originalprocesseslist,turnaround_time):
    totaltt = sum(turnaround_time)
    avgtt = totaltt / len(originalprocesseslist)
    return totaltt, round(avgtt,3)

def calwaitingtime(originalprocesseslist,waiting_time):
    totalwt = sum(waiting_time)
    avgwt = totalwt / len(originalprocesseslist)
    return totalwt, round(avgwt,3)




from django.shortcuts import render
from django.views.generic import ListView
import pandas as pd
# Create your views here.
    
def home(request):
    return render(request, 'rrhome.html')

def getrr(request):
    processes = request.GET["processes"]
    arrivaltimeslist = request.GET["arrivaltimeslist"]
    bursttimeslist = request.GET["bursttimeslist"]
    prioritylist = request.GET["prioritylist"]
    quantum = 3
    
    originalprocesseslist = processes.split()
    processeslist = processes.split()
    oriarrivallist = [int(num) for num in arrivaltimeslist.split()]
    arrivallist = [int(num) for num in arrivaltimeslist.split()]
    oriburstlist = [int(num) for num in bursttimeslist.split()]
    burstlist = [int(num) for num in bursttimeslist.split()]
    plist = [int(num) for num in prioritylist.split()]
    
    
    while (len(processeslist) != len(arrivallist) or len(processeslist) != len(burstlist) or len(processeslist) != len(plist)):
        return render(request, 'home.html', {'errormessage':'Invalid Input!'})
    
    processeslist, arrivallist, burstlist, plist = rearrangelist(processeslist, arrivallist, burstlist, plist)
    
    finishedjob, finishing_time = calcAllTime(processeslist,arrivallist,burstlist,plist, quantum)
    rr_table,tt,wt = drawtable(originalprocesseslist,oriarrivallist, oriburstlist, finishedjob, finishing_time)
    
    firstarrival = getfirstarrivaltime(finishedjob,originalprocesseslist,oriarrivallist)
    
    rr = pd.DataFrame.from_dict(rr_table)
    column_name = list(rr.columns)
    values = list(rr.values)
    
    totaltt, avgtt = calturnaroundtime(originalprocesseslist,tt)
    totalwt, avgwt = calwaitingtime(originalprocesseslist,wt)
    
    return render(request, 'result2.html', {"column_name": column_name, "values": values, "totaltt": totaltt, "avgtt":avgtt, "totalwt": totalwt, "avgwt":avgwt, "finishedjob":finishedjob, "firstfinishedjob_arrival":firstarrival, "finishing_time":finishing_time})

def getfirstarrivaltime(finishedjob,originalprocesseslist,arrivallist):
    index = originalprocesseslist.index(finishedjob[0])
    return arrivallist[index]

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
            if (readyQueuearrival[i]>readyQueuearrival[j]):
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
            elif (readyQueuearrival[i]==readyQueuearrival[j]):
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
    
def calcAllTime(processeslist,arrivallist,burstlist,plist,quantum):
    tempburstlist = burstlist.copy()
    
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
    
    totalbursttime = sum(burstlist)
    for i in range(0, len(processeslist)):
        if i == 0:
            if (burstlist[i] <= quantum):
                finishedjob.append(processeslist[i])
                finishedjob_burst.append(burstlist[i])
                finishedjob_arrival.append(arrivallist[i])
                finishing_time.append(arrivallist[i] + burstlist[i])
                turnaround_time.append(finishing_time[i] - arrivallist[i])
                waiting_time.append(turnaround_time[i] - burstlist[i])
                tempburstlist[i] = 0
            else:
                finishedjob.append(processeslist[i])
                finishedjob_burst.append(quantum)
                finishing_time.append(arrivallist[i] + quantum)
                finishedjob_arrival.append(arrivallist[i])
                readyQueueprocess.append(processeslist[i])
                readyQueuearrival.append(finishing_time[i])
                readyQueueburst.append(burstlist[i] - quantum)
                readyQueuepriority.append(plist[i])
                tempburstlist[i] = 0
        else:
            if (len(readyQueueprocess) == 0):
                if (burstlist[i] <= quantum):
                    finishedjob.append(processeslist[i])
                    finishedjob_burst.append(burstlist[i])
                    finishedjob_arrival.append(arrivallist[i])
                    finishing_time.append(finishing_time[i-1] + burstlist[i])
                    turnaround_time.append(finishing_time[i] - arrivallist[i])
                    waiting_time.append(turnaround_time[i] - burstlist[i])
                    tempburstlist[i] = 0
                    
                else:
                    finishedjob.append(processeslist[i])
                    finishedjob_burst.append(quantum)
                    finishedjob_arrival.append(arrivallist[i])
                    finishing_time.append(finishing_time[i-1] + quantum)
                    readyQueueprocess.append(processeslist[i])
                    readyQueuearrival.append(finishing_time[i])
                    readyQueueburst.append(burstlist[i] - quantum)
                    readyQueuepriority.append(plist[i])
                    tempburstlist[i] = 0
                    
            else:
                readyQueueprocess,readyQueuearrival,readyQueueburst,readyQueuepriority = reaarangereadyqueue(readyQueueprocess,readyQueuearrival,readyQueueburst,readyQueuepriority)
                index = processeslist.index(readyQueueprocess[0])
                if (readyQueueburst[0] <= quantum):
                    finishedjob.append(readyQueueprocess[0])
                    finishing_time.append(finishing_time[i-1] + readyQueueburst[0])
                    finishedjob_burst.append(readyQueueburst[0])
                    finishedjob_arrival.append(arrivallist[index])
                    
                    readyQueueprocess.pop(0)
                    readyQueuearrival.pop(0)
                    readyQueueburst.pop(0)
                    readyQueuepriority.pop(0)
                    
                else: 
                    finishedjob.append(readyQueueprocess[0])
                    finishing_time.append(finishing_time[i-1] + quantum)
                    finishedjob_burst.append(quantum)
                    finishedjob_arrival.append(arrivallist[index])
                    
                    readyQueueprocess.append(readyQueueprocess[0])
                    readyQueuearrival.append(finishing_time[i])
                    readyQueueburst.append(readyQueueburst[0] - quantum)
                    readyQueuepriority.append(plist[index])
                    
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
                    readyQueueprocess,readyQueuearrival,readyQueueburst,readyQueuepriority = reaarangereadyqueue(readyQueueprocess,readyQueuearrival,readyQueueburst,readyQueuepriority)

    lastfinishing_time_index = len(finishing_time)-1
    
    if finishing_time[lastfinishing_time_index] != totalbursttime:
        while finishing_time[len(finishing_time) - 1] < totalbursttime:
            if (readyQueueburst[0] <= quantum):
                finishedjob.append(readyQueueprocess[0])
                finishing_time.append(finishing_time[len(finishing_time)-1] + readyQueueburst[0])
                finishedjob_burst.append(readyQueueburst[0])
                finishedjob_arrival.append(arrivallist[index])
                
                readyQueueprocess.pop(0)
                readyQueuearrival.pop(0)
                readyQueueburst.pop(0)
                readyQueuepriority.pop(0)
                
            else:
                finishedjob.append(readyQueueprocess[0])
                finishing_time.append(finishing_time[len(finishing_time)-1] + quantum)
                finishedjob_burst.append(quantum)
                finishedjob_arrival.append(readyQueuearrival[0])
                
                readyQueueprocess.append(readyQueueprocess[0])
                readyQueuearrival.append(readyQueuearrival[0])
                readyQueueburst.append(readyQueueburst[0] - quantum)
                readyQueuepriority.append(readyQueuepriority[0])
                
                readyQueueprocess.pop(0)
                readyQueuearrival.pop(0)
                readyQueueburst.pop(0)
                readyQueuepriority.pop(0)
    
    #print(finishedjob, finishing_time)
    return finishedjob, finishing_time

def drawtable(originalprocesseslist, arrivallist, burstlist, finishedjob, finishing_time):
    processesl=[]
    table_at = []
    table_bt =[]
    table_ft = []
    table_tt = []
    table_wt = []
    res = []
    
    for i in range(0, len(originalprocesseslist)):
        res.append(max(idx for idx, val in enumerate(finishedjob) if val == originalprocesseslist[i]))

    #print(res)
    
    for i in range(0, len(originalprocesseslist)):
        processesl.append(originalprocesseslist[i])
        table_at.append(arrivallist[i])
        table_bt.append(burstlist[i])
        #print(res[i])
        table_ft.append(finishing_time[res[i]])
        table_tt.append(finishing_time[res[i]]-arrivallist[i])
        table_wt.append(finishing_time[res[i]]-arrivallist[i]-burstlist[i])
        
    rr_table = { 'PROCESS' : processesl,
                  'ARRIVAL TIME' : table_at,
                  'BURST TIME' : table_bt,
                  'FINISHING TIME' : table_ft,
                  'TURNAROUND TIME' : table_tt,
                  'WAITING TIME' : table_wt }
    return rr_table, table_tt, table_wt

def calturnaroundtime(originalprocesseslist,turnaround_time):
    totaltt = sum(turnaround_time)
    avgtt = totaltt / len(originalprocesseslist)
    return totaltt, round(avgtt,3)

def calwaitingtime(originalprocesseslist,waiting_time):
    totalwt = sum(waiting_time)
    avgwt = totalwt / len(originalprocesseslist)
    return totalwt, round(avgwt,3)
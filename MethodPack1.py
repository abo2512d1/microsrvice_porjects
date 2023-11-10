from Schedule import *
from Instance import *
from Machine import *
from MethodPack2 import *
from MDGraphClass import *
import pandas as pd
import random
from Node import *
from SetUpschedule import *

#====================
#  I have cahnge the getDM_MigrationNode() method in MDGraophClass to getDM_ReplicaToNode()

# ====================
# read csv file and return as list

def reaCsvFile(f_dir, fileName, selcolomn):
    fileDataAsList = []
    fileDataAsList = (
        list(genfromtxt(f_dir + fileName, delimiter=",", skip_header=1, dtype=None, loose=False, usecols=selcolomn)))
    return fileDataAsList


# ===================
# add the physical machine id to the job data with 7 features
def addMachineIdTo7featuresData(oldData, newData):
    dataset = []
    for i in oldData:
        for j in newData:
            if i[0] == j[0]:
                print('t')
                i[8] = j[4]
                break
    return dataset


# =====================

def selectColumn(array, columnNum):  # select one colum fo table
    retArray = []
    for a in array:
        retArray.append(a[columnNum])
    return retArray


# ======================
# function that arrange data baed on the range and if the data has non will make it 0
def selectDataFromRangWithConsiderNon(OneRecord, Datarange):
    data = []
    for r in Datarange:
        if OneRecord[r] == None:
            data.append(0)
        data.append(OneRecord[r])

    return data


# ==========================
def writeFinalResultDataToFile(FileDierction, fheader, array6):
    f1 = open(FileDierction, 'w')  # create or opne file for all jobs alone
    writer3 = csv.writer(f1)  # write the data to the file
    writer3.writerow(fheader)
    for i in range(len(array6)):
        writer3.writerow(array6[i])


# ==========================
def getMachineID(dataset, start_time, end_time):
    machineIDs = []
    for i in dataset:
        if i[6] < end_time and i[7] > start_time:
            machineIDs.append(i[1])
    return machineIDs


# =========================
def getMachineAttribute(machinesID, MachinesData):
    machineAttr = []
    for i in machinesID:
        for j in MachinesData:
            if i == j[0]:
                machineAttr.append(j)
                break
    return machineAttr


# =========================
# add the job to the machine
def returnJobforMachines(machineIDs, DataSet):
    dataToAdd = []
    avgCpu = 0
    avgMem = 0
    for i in DataSet:
        if i[1] == machineIDs:
            # if i[9]<0.363045282 and i[10]>0.361976408:
            avgCpu = (i[2] + i[4]) / 2
            avgMem = (i[3] + i[5]) / 2

            dataToAdd.append([i[0], avgCpu, avgMem, i[6], i[7], i[8], i[9]])
    return dataToAdd


# =========================
def calculateMaxOfUtalization(schedual):
    cpuMax = 0
    memoryMax = 0
    statrTime = 0
    endTime = 0
    duration = 0
    if len(schedual.job) > 0:
        if len(schedual.job) == 1:
            cpuMax = schedual.getjobCPUUsage()
            memoryMax = schedual.getjobMemUsage()
            statrTime = schedual.getjobStartTime()
            endTime = schedual.getjobEndTime()
            duration = schedual.getjobDuration()
        elif len(schedual.job) > 1:
            cpuMax = sum(schedual.getjobCPUUsage())
            memoryMax = sum(schedual.getjobMemUsage())
            statrTime = max(schedual.getjobStartTime())
            endTime = max(schedual.getjobEndTime())
            duration = max(schedual.getjobDuration())
    else:
        cpuMax = 0
        memoryMax = 0
        statrTime = 0
        endTime = 0
        duration = 0
    return cpuMax, memoryMax, statrTime, endTime, duration


# =====================
def calculateMaxOfUtalizationEach5Mints(schedual):
    startTimeclo = 0.5095887345679012
    cpuMax = 0
    memoryMax = 0
    statrTime = 0
    endTime = 0
    duration = 0
    retList = []
    retList1 = []
    for i in range(100):
        # print(i,'->',len(schedual.job))
        x = i * 0.000114155 + startTimeclo
        for j in schedual.job:
            # print(j.jobStartTime,'<',x+0.000114155,' and', j.jobEndTime,'>',x)
            if (j.jobStartTime < x and j.jobEndTime > 0.5109583333333333):
                # print('here')
                retList.append([j.jobCPUUsage / 9, j.jobMemUsage / 9, j.jobStartTime / 9,
                                j.jobEndTime / 9, j.jobDuration / 9])
                # print(retList)
            elif (j.jobStartTime < x + 0.000114155 and j.jobEndTime > x and (j.jobStartTime > x)):
                retList.append((j.jobCPUUsage, j.jobMemUsage, j.jobStartTime,
                                j.jobEndTime, j.jobDuration))

            # else:
            # print('f')
        retList1.append(retList)
        retList = []
    return retList1


# =====================
# for k,m in zip(schedual.getjobStartTime(),schedual.getjobEndTime()):
#                print('k',k,'x1',x,'m',m,'x2',x+0.000114155)
#                if (m>x and k<x+0.000114155):
#                        if len(schedual.job)>0:
#                            if len(schedual.job)==1:
#                                cpuMax=schedual.getjobCPUUsage()
#                                memoryMax=schedual.getjobMemUsage()
#                                statrTime=schedual.getjobStartTime()
#                                endTime=schedual.getjobEndTime()
#                                duration=schedual.getjobDuration()
#                            elif len(schedual.job)>1:
#                                cpuMax=sum(schedual.getjobCPUUsage())
#                                memoryMax=sum(schedual.getjobMemUsage())
#                                statrTime=max(schedual.getjobStartTime())
#                                endTime=max(schedual.getjobEndTime())
#                                duration=max(schedual.getjobDuration())
#                        else:
#                            cpuMax=0
#                            memoryMax=0
#                            statrTime=0
#                            endTime=0
#                            duration=0
# return cpuMax,memoryMax,statrTime,endTime,duration
# ====================
def calculateThePercentageOfUsage(pHCapacity, jobRequ, i):
    pec = 0
    # print('clcuate pe cent ',pHCapacity)
    pec = np.asarray(jobRequ) / np.asarray(pHCapacity)
    return pec


# ====================
def plot_distribution(inp):
    plt.figure()
    ax = sns.distplot(inp)
    plt.axvline(np.mean(inp), color="k", linestyle="dashed", linewidth=5)
    plt.axvline(stdev(inp), color='r', linestyle='-')
    plt.text(stdev(inp), .9, "SD: {:.4f}".format(stdev(inp)), color="r")
    _, max_ = plt.ylim()
    plt.text(
        np.mean(inp) + np.mean(inp) / 10,
        max_ - max_ / 10,
        "Mean: {:.4f}".format(np.mean(inp)),
    )

    return plt.figure


def plottingSD(x1, y1, c, t):
    fig, ax = plt.subplots()
    plt.scatter(x1, y1, color=c)
    plt.title(t)
    plt.xlabel("utiliazation")
    plt.ylabel("time")
    # ax = sns.distplot(selectColumn(SortCluster0,2))
    plt.axvline(np.mean(x1), color="k", linestyle="dashed", linewidth=5, label='mean')
    plt.text(np.mean(x1), .5, "Mean: {:.4f}".format(np.mean(x1)), color="r")
    # plt.scatter(selectColumn(SortCluster0,9),selectColumn(SortCluster0,4))
    plt.axvline(stdev(x1), color='r', linestyle='-')
    plt.text(stdev(x1), .9, "SD: {:.4f}".format(stdev(x1)), color="r")
    sns.displot(x=x1, y=y1)
    plt.title(t)
    plt.xlabel("utiliazation")
    plt.ylabel("time")
    return plt.figure


# ========================
# allocate instance onto node

def allocateInstanceOntoNodes(schedul, dataset):  # node could be the schedual like alibabaschedul
    instList = []
    count = 0
    for i in schedul:
        nodeID = i.node.getID()
        count = count + 1
        print(count)
        for j in dataset.index:
            # if j==124588790 or j==0:
            # print(j, "point")
            if dataset["nodeid"][j] == nodeID and dataset["msinstanceid"][j] not in instList:
                # print("here",nodeID)
                i.addInstances(dataset["msinstanceid"][j], dataset["instance_cpu_utilization"][j],
                               dataset["instance_memory_utilization"][j], dataset["msname"][j])
                instList.append(dataset["msinstanceid"][j])
                if len(instList) > 6:
                    break
        instList.clear()


# =============================
# write the scheduling in file
def wirteSchedulInFileToBackup(FileDierction, fheader, schedul):  # one node at te time
    nameOftheFile = schedul.node.getID()
    f1 = open(FileDierction + "\\" + nameOftheFile + ".csv", 'w', newline='')  # create or opne file for all jobs alone
    writer3 = csv.writer(f1)  # write the data to the file
    writer3.writerow(fheader)
    for i in range(len(schedul.instances)):
        # print(schedul.instances[i].getID())
        writer3.writerow([schedul.instances[i].getID(), schedul.instances[i].getCPU(), schedul.instances[i].getMem(),
                          schedul.instances[i].getMSserviceName()])


# ================================
def wirteSchedulInFileToBackupwithNodeIdInOneFile(FileDierction, fheader, indexOftheRwa,
                                                  schedul):  # one node at te time
    nameOftheFile = schedul.node.getID()
    f1 = open(FileDierction, 'a', newline='')  # create or opne file for all jobs alone
    writer3 = csv.writer(f1)  # write the data to the file
    if indexOftheRwa == 0:
        writer3.writerow(fheader)
    for i in range(len(schedul.instances)):
        # print(schedul.instances[i].getID())
        writer3.writerow([schedul.node.getID(), schedul.instances[i].getID(), schedul.instances[i].getCPU(),
                          schedul.instances[i].getMem(), schedul.instances[i].getMSserviceName()])
    f1.close()


# ================================
# restoring the scheduling data from file
def restorSchedulFromFileConfigration(FileDierction, nodeifo):
    restorschedul = []
    print("1")
    nmachineID = 0
    for i, x in zip(nodeifo.index, range(0, len(nodeifo))):
        nmachineID += 10
        print("2 machine id ", nmachineID)

        restorschedul.append(schedul(nodeifo["nodeid"][i], nmachineID, nodeifo["max_cpu_utilization"][i],
                                     nodeifo["max_memory_utilization"][i]))
        instanceInfo = pd.read_csv(FileDierction + "//" + nodeifo["nodeid"][i] + '.csv')
        for j in instanceInfo.index:
            restorschedul[x].addInstances(instanceInfo["msinstanceid"][j], instanceInfo["instance_cpu_utilization"][j],
                                          instanceInfo["instance_memory_utilization"][j], instanceInfo["msname"][j])
        print("Done")
        instanceInfo = pd.DataFrame()
    return restorschedul


# =================================
# write the result of scheduling into files
# # dirForSaveSchedualData=Dir+"\\allDataFro100NodeInoneHourNoDoublicatioFromSchedul.csv"
# instHeader=["nodeid","msinstanceid","instance_cpu_utilization","instance_memory_utilization","msname"]
# for i in AlibabCluster:
#     wirteSchedulInFileToBackup(dirForSaveSchedualData,instHeader,i)

# ================================
def wirteSchedulInFileToBackupwithInstanceDMsInOneFile(FileDierction, fheader,
                                                       schedul_instance):  # one instance at te time
    nameOftheFile = schedul_instance.getID()
    f1 = open(FileDierction + "\\" + nameOftheFile + ".csv", 'w', newline='')
    writer3 = csv.writer(f1)  # write the data to the file
    writer3.writerow(fheader)
    for i in range(len(schedul_instance.DMGraphs)):
        # print(schedul.instances[i].getID())
        writer3.writerow([schedul_instance.DMGraphs[i].getDM_ID(), schedul_instance.DMGraphs[i].getDM_NodeID()])
    f1.close()


# ================================
# count the number of dependencis between nodes by count how many MS in the same node or in different node and counting the satate MD
# it prints the results as SCV file
def count_the_Nmber_of_DM_where_Its_inThesameNode_or_InDifferentNode(schedul):
    node = 0
    StateDMcount = 0
    countSameNode = 0
    countDiffNode = 0

    eachNOdcountSameNode = 0
    eachNOdcountDiffNode = 0
    eachNOdcountStateDM = 0
    print("Node No,#total, MD in the same node, MD in the different node, Staste MD")

    for i in schedul:
        node = node + 1
        eachNOdcountSameNode = 0
        eachNOdcountDiffNode = 0
        eachNOdcountStateDM = 0
        for j in i.instances:
            for k in j.DMGraphs:
                if k.getDM_NodeID() != -1 and k.getDM_NodeID == i.node.getID():
                    countSameNode = countSameNode + 1
                    eachNOdcountSameNode = eachNOdcountSameNode + 1
                elif k.getDM_NodeID() != -1 and k.getDM_NodeID != i.node.getID():
                    countDiffNode = countDiffNode + 1
                    eachNOdcountDiffNode = eachNOdcountDiffNode + 1
                elif k.getDM_NodeID() == -1:
                    StateDMcount = StateDMcount + 1
                    eachNOdcountStateDM = eachNOdcountStateDM + 1
        countEachNode = eachNOdcountSameNode + eachNOdcountDiffNode + eachNOdcountStateDM
        print(node, ",", countEachNode, ",", eachNOdcountSameNode, ",", eachNOdcountDiffNode, ",", eachNOdcountStateDM)
    count = StateDMcount + countSameNode + countDiffNode
    print("total=", count, "\n MD in the same node=", countSameNode, "\n MD in the different node=", countDiffNode,
          "\n Staste MD=", StateDMcount)


# ==================================
# find nodeid forthe dm
def find_nodeid_for_DM(dm, table):
    nodeid = ""
    for t in table.index:
        if dm == table["dm"][t]:
            # print("f",table["nodeid"][t])
            nodeid = table["nodeid"][t]
            break
    return nodeid


# ==================================
# check if dm alrody been assing to the um service
def checkDM_inTheList(x, list1):
    t = False
    for i in list1:
        if i == x:
            t = True
            break
    return t


# ==================================
# find nodeid forthe dm
def find_If_nodeid_for_DM_Is_One_Of_TheSchedulNode(nodeId, table):
    t = False
    for t in table.index:
        if nodeId == table["nodeid"][t]:
            # print("f",table["nodeid"][t])
            t = True
            break
    return t


# ====================================
# # return the utilization of resources by DM one each time
def returnTheUtilizationOfDM(DM, Re_Utilization):
    cpu_uti = 0
    mem_uti = 0
    for i in Re_Utilization.index:
        if Re_Utilization["dm"][i] == DM:
            cpu_uti = Re_Utilization["max_cpu_utilization"][i]
            mem_uti = Re_Utilization["max_memory_utilization"][i]
            break
    return cpu_uti, mem_uti


# ====================================

# restor dm info from files based on instances id
def restorDmInfoFromFilesBasedOnInstanceId(FileDierction, instance, DM_Re_Utilization,DM_machIDsRandom):
    Dmtype=1
    Dm = -1
    DM_machineIDsIndex = 0
    for i, x in zip(instance, range(0, len(instance))):
        instanceID = i.getID()
        DmLists = pd.read_csv(FileDierction + "/" + instanceID + '.csv')
        for j in DmLists.index:
            if pd.isna(DmLists["nodeid"][j]):
                Dmtype = 0  # statefull service
                Dm = -1  # nodeIde

            else:
                Dmtype = 1  # stateless service
                Dm = DmLists["nodeid"][j]
                # DM_machineID=Return_machienId_for_DM_Is_One_Of_TheSchedulNode(DmLists["dm"][j],instanceID_With_TheirMachinesIDs)#need to be finished
            DM_CPU_Uti, DM_Mem_Uti = returnTheUtilizationOfDM(DmLists["dm"][j],
                                                              DM_Re_Utilization)  # return the utilization of resources by DM one each time
            if DM_CPU_Uti == 0:
                DM_CPU_Uti = random.uniform(0.00445833333333402,
                                            0.780749999999534)  # random number based on the minmum number of utilization of cpu among DMs
            if DM_Mem_Uti == 0:
                DM_Mem_Uti = random.uniform(0.00722503662109375, 0.981824398040772)
            DM_machineID = DM_machIDsRandom["machineIdForDMs"][DM_machineIDsIndex]
            i.addServce(DmLists["dm"][j], DM_machineID, Dm, DM_CPU_Uti, DM_Mem_Uti, -1, Dmtype)
            DM_machineIDsIndex = DM_machineIDsIndex + 1
        DmLists = pd.DataFrame()


# =====================================
# find If nodeid for DM Is One Of TheSchedulNode
def find_If_nodeid_for_DM_Is_One_Of_TheSchedulNode(DM_NodeID, nodeId):
    t = False
    for i in nodeId:
        if DM_NodeID == i:
            t = True
            break
    return t


# ====================================
def Return_machienId_for_DM_Is_One_Of_TheSchedulNode(DM_NodeID, instncelistWithMachineIDs):
    listOFmachnesIDs = []
    for i in instncelistWithMachineIDs.index:
        if instncelistWithMachineIDs["theServerInTheinstancesID"][i] == DM_NodeID:
            print("mach")
            listOFmachnesIDs.append(instncelistWithMachineIDs["machineID"][i])
    return random.choice(listOFmachnesIDs)


# ===================================
# calculate the utilization of instances

def calculteInstanceUtilization(node):
    cpu_Utiliation = 0
    Mem_Utiliztion = 0
    for i in node.instances:
        cpu_Utiliztion = cpu_Utiliation + i.getCPU()
        Mem_Utiliztion = Mem_Utiliztion + i.getMem()
    return cpu_Utiliztion, Mem_Utiliztion


# ==================================
# return the pod of the michine that host DM
def find_machine_pod_forDM(dm_ID, mchineList):
    pod = 0
    switch = 0
    port = 0
    for i in mchineList:
        if i.getMachID() == dm_ID:
            pod = i.getpodNumber()
            switch = i.getswitchNumber()
            port = i.getportNumber()
            break
    return pod, switch, port


# ==================================
# count the number of dependncy based on the pods (one node each time)
def calculateDepedenciesConsideringTopology(schedule, mchineList):

    for i in schedule:
        node_machinepod = 0
        node_machineswitch = 0
        node_machineport = 0
        node_machinepod, node_machineswitch, node_machineport = find_machine_pod_forDM(i.node.getMachineID(),
                                                                                       mchineList)
        for j in i.instances:
            j.DM_Dependencies=[0] * len(j.DMGraphs)
            if j.getmigrating_ToMachine_Number() != -1:
                node_machinepod, node_machineswitch, node_machineport = find_machine_pod_forDM(
                    j.getmigrating_ToMachine_Number(), mchineList)
                # print("find instnce thet is migrated")
            for k, index in zip(j.DMGraphs, range(0, len(j.DMGraphs))):
                DM_machinepod = 0
                DM_machineswitch = 0
                DM_machineport = 0
                Dependencies_num = 0
                #if k.getDM_type()==1:
                if k.getDM_ReplicaToNode() == -1:
                            # print("not migrated")
                    DM_machinepod, DM_machineswitch, DM_machineport = find_machine_pod_forDM(k.getDM_MachineId(),
                                                                                                     mchineList)  # return the pod of the michine that host DM
                else:
                            # print("migrated")
                    DM_machinepod, DM_machineswitch, DM_machineport = find_machine_pod_forDM(k.getDM_ReplicaToNode(),
                                                                                                     mchineList)
                if DM_machinepod != node_machinepod:
                    Dependencies_num = 6
                else:
                        if (k.getDM_ReplicaToNode()==i.node.getMachineID() and k.getDM_ReplicaToNode()!=-1) or( k.getDM_MachineId() == i.node.getMachineID() and k.getDM_ReplicaToNode()==-1):
                             Dependencies_num = 0

                        elif (DM_machineswitch != node_machineswitch and  k.getDM_ReplicaToNode()!=i.node.getMachineID() and k.getDM_ReplicaToNode()!=-1) or (DM_machineswitch != node_machineswitch and  k.getDM_MachineId()!=i.node.getMachineID() and k.getDM_ReplicaToNode()==-1):
                            Dependencies_num = 4
                        else:
                            Dependencies_num = 2
                        # if k.getDM_ReplicaToNode() == -1:
                j.DM_Dependencies[index] = Dependencies_num#j.add_DepananciesToDMs(Dependencies_num)
                        # else:
                        #     j.DM_Dependencies[index] = Dependencies_num
#===================================
def calculateDepedenciesConsideringTopologyForSataelessandStaful(schedule, mchineList):# This calculating the dependencies without affecting dependecies list in instance calss
    Dependencies_num = 0
    for i in schedule:
        node_machinepod = 0
        node_machineswitch = 0
        node_machineport = 0
        node_machinepod, node_machineswitch, node_machineport = find_machine_pod_forDM(i.node.getMachineID(),
                                                                                       mchineList)
        for j in i.instances:
            #j.DM_Dependencies=[0] * len(j.DMGraphs)
            if j.getmigrating_ToMachine_Number() != -1:
                node_machinepod, node_machineswitch, node_machineport = find_machine_pod_forDM(
                    j.getmigrating_ToMachine_Number(), mchineList)
                # print("find instnce thet is migrated")
            for k, index in zip(j.DMGraphs, range(0, len(j.DMGraphs))):
                DM_machinepod = 0
                DM_machineswitch = 0
                DM_machineport = 0

                # if k.getDM_type()==1:
                if k.getDM_ReplicaToNode() == -1:
                            # print("not migrated")
                    DM_machinepod, DM_machineswitch, DM_machineport = find_machine_pod_forDM(k.getDM_MachineId(),
                                                                                                     mchineList)  # return the pod of the michine that host DM
                else:
                            # print("migrated")
                    DM_machinepod, DM_machineswitch, DM_machineport = find_machine_pod_forDM(k.getDM_ReplicaToNode(),
                                                                                                     mchineList)
                if DM_machinepod != node_machinepod:
                    Dependencies_num += 6
                else:
                        if (k.getDM_ReplicaToNode()==i.node.getMachineID() and k.getDM_ReplicaToNode()!=-1) or( k.getDM_MachineId() == i.node.getMachineID() and k.getDM_ReplicaToNode()==-1):
                            Dependencies_num += 0

                        elif (DM_machineswitch != node_machineswitch and  k.getDM_ReplicaToNode()!=i.node.getMachineID() and k.getDM_ReplicaToNode()!=-1) or (DM_machineswitch != node_machineswitch and  k.getDM_MachineId()!=i.node.getMachineID() and k.getDM_ReplicaToNode()==-1):
                            Dependencies_num += 4
                        else:
                            Dependencies_num += 2
                        # if k.getDM_ReplicaToNode() == -1:
                #j.add_DepananciesToDMs(Dependencies_num)#return Dependencies_num#
                        # else:
                j.DM_Dependencies[index] = Dependencies_num



# ===================================
# common methods for Autoencoder
def Plotting(his):
    # plotting the result
    plt.plot(his.history['accuracy'])
    plt.plot(his.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(his.history['loss'])
    plt.plot(his.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
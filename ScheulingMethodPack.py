# all methodes for secheduling
# sorting the DMs in list with execludeing migrated one (for each instance indveduley) one instance each time
#  I have cahnge the getDM_MigrationNode() method in MDGraophClass to getDM_ReplicaToNode()

def Return_sorted_DMs_InList_BasedOn_Dependencies_and_ResourceUtilization(inst):  # list of DMs for ech instance
    listOf_potintioalDMs = []
    for DM, Depend, in zip(inst.DMGraphs, inst.DM_Dependencies):
        if DM.getDM_MigrationNode() == -1:
            listOf_potintioalDMs.append(
                [DM.getDM_ID(), DM.CPU_Utilization, DM.Memory_Utilization, DM.getDM_MigrationNode()])
    listOf_potintioalDMs.sort(key=operator.itemgetter(1, 2))
    listOf_potintioalDMs.sort(key=lambda x: x[3], reverse=True)
    return listOf_potintioalDMs


# ===================================
# return list of cpu utilization and memory utilization for a node
def return_SUM_of_cpu_Mem_utilization(node):
    CPUUti = []
    MemUti = []
    for j in node.instances:
        if node.node.getID() == j.getmigrating_ToMachine_Number() or j.getmigrating_ToMachine_Number() == -1:
            CPUUti.append(j.getCPU())
            MemUti.append(j.getMem())
    return sum(CPUUti), sum(MemUti)


# ======================================
def return_SUM_of_cpu_Mem_utilization_for_PMs_beyond_98(machineNumber, schedul):
    CPUUti = 0
    MemUti = 0
    for s in schedul:
        for inst in s.instances:
            if (s.node.getMachineID() == machineNumber and inst.getmigrating_ToMachine_Number() == -1) or (
                    inst.getmigrating_ToMachine_Number() != -1 and inst.getmigrating_ToMachine_Number() == machineNumber):
                CPUUti += inst.getCPU()
                MemUti += inst.getMem()
                for dm in inst.DMGraphs:
                    if (dm.getDM_MachineId() == machineNumber and dm.getDM_MigrationNode() == -1) or (
                            dm.getDM_MigrationNode() != -1 and m.getDM_MigrationNode() == machineNumber):
                        CPUUti += dm.getDM_CPUUti()
                        MemUti += dm.getDM_MemUti()
    return CPUUti, MemUti


# ===================================
def return_list_of_Potentioal_Machines(ListOfmachines, machine_number):
    switch_number = 0
    pod_number = 0
    listOMachinesForReturn = []
    for i in ListOfmachines:
        if i.getMachID() == machine_number:
            switch_number = i.getswitchNumber()
            pod_number = i.getpodNumber()
            break

    for i in ListOfmachines:
        if i.getpodNumber() == pod_number:  # or i.getswitchNumber()==switch_number:# and i.getMachID()!=machine_number:
            listOMachinesForReturn.append(i.getMachID())
    return listOMachinesForReturn


# ===================================
def Returen_Sorted_ListOf_potentioal_Hosts_ForDMs(machines, schedul_node, MachineID_ForTheInsatance, instance):
    TotalnodeCapacity_CPU = 0  # each machine has just one node therfore the capacity of the mahine is the utilizatoion of all instances in the node
    TotalnodeCapacity_Mem = 0
    The_Sum_OfTheCPU_Utilization = 0
    The_Sum_OfTheMem_Utilization = 0
    listOf_Potential_Hosts = []

    # machineOfTheNode_Number=i.getMachineID()

    #
    # break


# ================================
def UpdateDMStatse(instance, DM, MachineID):
    for DMs in instance.DMGraphs:
        if DMs.getDM_ID() == DM:
            DMs.setMigrationStatse(MachineID)
            # print("change the host node")
            break


# =================================
# calaculte the number of dependncy from the nstance list
def sum_TheLIstOf_Dependncies_FromInstance(shedule):
    sumDep = 0
    for s in shedule:
        for inst in s.instances:
            for d in inst.DM_Dependencies:
                sumDep += d
    return sumDep


# ===============================
# return the utilization matrix of machines and nodes
def Utilization_Of_machines_and_Node_Matrix(schedul, machileList):
    list_of_migratedDM = []
    list_of_utilizationOfnode_byInstances = []
    listOFUtilizationByNode = []
    ListOfMachineCapacity = []
    for s, m in zip(schedul, machileList):
        sumCPUUti = 0
        sumMemUti = 0
        sumDMCPUUti = 0
        sumDMMemUti = 0
        listOFUtilizationByNode.append([s.node.getCPU(), s.node.getMem()])
        ListOfMachineCapacity.append([m.vcpu, m.memory])
        for inst in s.instances:
            # find if the instance was mograted just do not consider it as been from the current nodes
            if inst.getmigrating_ToMachine_Number() == -1:
                sumCPUUti += inst.getCPU()
                sumMemUti += inst.getMem()
                print("inst not migrated")
        for s2 in schedul:
            for inst2 in s2.instances:
                if inst2.getmigrating_ToMachine_Number() == s.node.getMachineID():
                    sumCPUUti += inst2.getCPU()
                    sumMemUti += inst2.getMem()
                    print("inst migrated")
        for s3 in schedul:
            for inst3 in s3.instances:
                for DM in inst3.DMGraphs:
                    if DM.getDM_MigrationNode() == s.node.getMachineID() or DM.getDM_MachineId() == s.node.getMachineID():
                        sumDMCPUUti += DM.getDM_CPUUti()
                        sumDMMemUti += DM.getDM_MemUti()

        list_of_utilizationOfnode_byInstances.append([sumCPUUti, sumMemUti])
        list_of_migratedDM.append([sumDMCPUUti, sumDMMemUti])
    com = []
    df = pd.DataFrame()
    for i in range(0, len(schedul)):
        print(listOFUtilizationByNode[i], list_of_utilizationOfnode_byInstances[i], list_of_migratedDM[i],
              ListOfMachineCapacity[i])
        com.append(listOFUtilizationByNode[i] + list_of_utilizationOfnode_byInstances[i] + list_of_migratedDM[i] +
                   ListOfMachineCapacity[i])
    df = pd.DataFrame(com,
                      columns=['node utilization CPU', 'node utilization Mem', 'instance utilization CPU',
                               'instance utilization Mem', 'migrated DM utilization CPU', 'migrated DM utilization Mem',
                               'machine capacity CPU ', 'machine capacity Mem'])
    return df


# ==========================================
# printing the result of scheduling compare to Alibab scheduling

def display_The_scheduling_result_andStatistics(AlibabaScheduling, optimizedSchedulig, machineList):
    print(sum_TheLIstOf_Dependncies_FromInstance(optimizedSchedulig),
          sum_TheLIstOf_Dependncies_FromInstance(AlibabaScheduling), "reduction",
          (sum_TheLIstOf_Dependncies_FromInstance(AlibabaScheduling) - sum_TheLIstOf_Dependncies_FromInstance(
              optimizedSchedulig)) / sum_TheLIstOf_Dependncies_FromInstance(AlibabaScheduling))

    DataAnalysis = Utilization_Of_machines_and_Node_Matrix(optimizedSchedulig, machineList)
    DataAnalysis.head()

    cpu_utilization = []
    Mem_utilization = []
    cpu_utilization = np.array(DataAnalysis.loc[:, 'instance utilization CPU'] + DataAnalysis.loc[:,
                                                                                 'migrated DM utilization CPU']) / DataAnalysis.loc[
                                                                                                                   :,
                                                                                                                   'machine capacity CPU ']
    Mem_utilization = np.array(DataAnalysis.loc[:, 'instance utilization Mem'] + DataAnalysis.loc[:,
                                                                                 'migrated DM utilization Mem']) / DataAnalysis.loc[
                                                                                                                   :,
                                                                                                                   'machine capacity Mem']

    plt.scatter(range(0, len(cpu_utilization)), cpu_utilization, color="blue")
    plt.bar(range(0, len(Mem_utilization)), Mem_utilization, color="green")
    plt.ylabel('machines')
    plt.ylabel("resource utilization ")

    # calculate the mean annd SD
    pointsCPU = []
    pointsMem = []
    pointsCPU = np.array(
        DataAnalysis.loc[:, 'instance utilization CPU'] + DataAnalysis.loc[:, 'migrated DM utilization CPU'])
    pointsMem = np.array(
        DataAnalysis.loc[:, 'instance utilization Mem'] + DataAnalysis.loc[:, 'migrated DM utilization Mem'])
    print("Mean=", np.mean(pointsCPU), "SD=", np.std(pointsCPU))
    print("Mean=", np.mean(pointsMem), "SD=", np.std(pointsMem))

    # pliting the distribution

    plot_distribution(pointsCPU)
    plot_distribution(pointsMem)
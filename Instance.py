from MDGraphClass import * # instance class

#  I have cahnge the getDM_MigrationNode() method in MDGraophClass to getDM_ReplicaToNode()

class Instance:
    def __init__(self, inst_id, inst_cpu, inst_mem, ms_name):
        self.instID = inst_id
        self.instCPU_utilization = inst_cpu
        self.instMem_utilization = inst_mem
        self.instCPU_capacity=2
        self.instMem_capacity=8
        self.msName = ms_name
        self.migrating_ToMachine_Number = -1
        self.DMGraphs = []
        self.DM_Dependencies = []

    def addServce(self, DM_id, DM_machID, DM_nodeid, CpuUtil, MemUtil, megrateTo, typ):
        self.DMGraphs.append(DMGraph(DM_id, DM_machID, DM_nodeid, CpuUtil, MemUtil, megrateTo, typ))

    def getID(self):
        return self.instID

    def getCPU(self):
        return self.instCPU_utilization

    def getMem(self):
        return self.instMem_utilization
    def getCPU_capacity(self):
        return self.instCPU_capacity

    def getMem_capacity(self):
        return self.instMem_capacity

    def getMSserviceName(self):
        return self.msName

    def show(self):
        print('Instance ID=', self.instID,
              '\nInstance  CPU requirment', self.instCPU_utilization,
              '\nInstance  Memory requirment', self.instMem_utilization,
              '\nInstance microservice namw', self.msName,
              '\nInstance migration machine nimber', self.migrating_ToMachine_Number,)

    def ReturnNumberOfDm(self):
        return len(self.DMGraphs)

    def ReturnNumberOfStateFullDmAndStateless(self):
        satFullCount = 0
        satLessCount = 0
        for i in self.DMGraphs:
            if i.getDM_type() == 1:
                satLessCount = satLessCount + 1
            else:
                satFullCount = satFullCount + 1
        return satFullCount, satLessCount

    def add_DepananciesToDMs(self, Dependency_number):
        self.DM_Dependencies.append(Dependency_number)

    def setMigrationStatse(self, macineID):
        self.migrating_ToMachine_Number = macineID

    def getmigrating_ToMachine_Number(self):
        return self.migrating_ToMachine_Number
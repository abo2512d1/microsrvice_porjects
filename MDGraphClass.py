# DMGraph class
#  I have cahnge the getDM_MigrationNode() method in MDGraophClass to getDM_ReplicaToNode()

class DMGraph:
    def __init__(self, DM_id, machId, DM_nodeid, CPU_Uti, Mem_Util, replica, typ):
        self.DM_ID = DM_id
        self.DM_MachID = machId
        self.DM_NodeID = DM_nodeid
        self.CPU_Utilization = CPU_Uti
        self.Memory_Utilization = Mem_Util
        self.DM_ReplicaToNodeID = replica
        self.ServicType = typ

    def getDM_ID(self):
        return self.DM_ID

    def getDM_CPUUti(self):
        return self.CPU_Utilization

    def getDM_MemUti(self):
        return self.Memory_Utilization

    def getDM_MachineId(self):
        return self.DM_MachID

    def getDM_NodeID(self):
        return self.DM_NodeID

    def getDM_type(self):
        return self.ServicType

    def getDM_ReplicaToNode(self):
        return self.DM_ReplicaToNodeID

    def show(self):
        print('DM ID=', self.DM_ID,
              '\nDM Nodeid', self.DM_NodeID,
              '\nDM orginal machine id', self.DM_MachID,
              '\nDM type', self.ServicType,
              '\nDM migrated machine id ', self.DM_ReplicaToNodeID)

    def setreplicaOnNode(self, macineID):
        self.DM_ReplicaToNodeID = macineID
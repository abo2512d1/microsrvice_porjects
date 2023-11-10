#Node
#  I have cahnge the getDM_MigrationNode() method in MDGraophClass to getDM_ReplicaToNode()

class Node:
        def __init__(self, node_id, pm, node_cpu, node_mem):
            self.physicalMachineId = pm
            self.nodeID = node_id
            self.nodeCPU = node_cpu
            self.nodeMem = node_mem

        def getMachineID(self):
            return self.physicalMachineId

        def getID(self):
            return self.nodeID

        def getCPU(self):
            return self.nodeCPU

        def getMem(self):
            return self.nodeMem

        def show(self):
            print('Node ID ', self.nodeID,
                  '\nNode CPU capacity', self.nodeCPU,
                  '\nNode CPU capacity', self.nodeMem,
                  '\nNode CPU machine id', self.physicalMachineId)

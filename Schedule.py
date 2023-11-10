import Node#schedul cals
import Instance# s
#  I have cahnge the getDM_MigrationNode() method in MDGraophClass to getDM_ReplicaToNode()

class schedul:
    def __init__(self,iid,pmid,cpu,mem):
        self.node= Node.Node(iid,pmid,cpu,mem)
        self.instances=[]
    def addInstances(self,ID,cpu,mem,MSname):
        self.instances.append(Instance.Instance(ID,cpu,mem,MSname))
    def showInstanceRequ(self):
        for i in self.instances:
                print(i.getID(),
                        i.getCPU(),
                        i.getMem(),
                        i.getMSserviceName())
    def reportToTheManagerOfTheschedule(self):
        CPU_utilization=0
        Memor_utilization=0
        numberOfSatefullDM=0
        numberOfSatelessDM=0
        numberOfIntance=0
        NumberofDmIneachInstance=[]
        for i in self.instances:
                CPU_utilization=CPU_utilization+i.getCPU()
                Memor_utilization=Memor_utilization+i.getMem()
                NumberofDmIneachInstance.append(i.ReturnNumberOfDm())
                numberOfSatefullDM,numberOfSatelessDM=i.ReturnNumberOfStateFullDmAndStateless()
        numberOfInstance=len(self.instances)
        return CPU_utilization,Memor_utilization,numberOfSatefullDM,numberOfSatelessDM,numberOfInstance,NumberofDmIneachInstance
#machine class
#  I have cahnge the getDM_MigrationNode() method in MDGraophClass to getDM_ReplicaToNode()

class Machine:
    def __init__(self,Mach_ID,pod_Nu,swit_Nu,port_nu):
            self.machineID=Mach_ID
            self.cpu=64
            self.vcpu=128
            self.memory=512
            self.podNumber=pod_Nu
            self.switchNumber=swit_Nu
            self.portNumber=port_nu
    def getMachID(self):
        return self.machineID
    def getpodNumber(self):
        return self.podNumber
    def getswitchNumber(self):
        return self.switchNumber
    def getportNumber(self):
        return self.portNumber
    def setPodNumber(self,podNum):
        self.podNumber=podNum
    def setSwitchNumber(self,switchNum):
        self.switchNumber=switchNum
    def setPortNumber(self,portNum):
        self.portNumber=portNum 
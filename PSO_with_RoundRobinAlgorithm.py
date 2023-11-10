from PSO import perparSwarm_and_nodeData,PSO,creatPointOfNodeRemainresourceUtilization,fitnessFunction2
from vritulizing_PSO_result import *
from AliBabaSchedul import *
from PSO_with_BestFitAlgorithm import returnResrourceUtilizationInTwoLists_dm,returnResrourceUtilizationInTwoLists_Node
from latency_calculation import *
#================================
PSO_withRRA_schedul=[]
PSO_withRRA_schedul=copy.deepcopy(AlibabCluster)

#============================
def ParticleSwarmOptimizationMethod_with_RRA(PSO_sc):
    print(" I am here RRA")
    #initial = [.001, .001]  # initial starting location [x1,x2...]

    bounds = [(0, 128), (0, 512)]  # input bounds [(x1_min,x1_max),(x2_min,x2_max)...]
    thershold=.75
    #swarmlist=[]
    plotg = []
    swarm_inf_as_dm=[]
    countPOsMigrated=0
    for sch in PSO_sc:
        swarm_inf_as_dm = []
        swarm_inf_as_dm,ListOfNodeForhosting_DMs, max_bound,count= perparSwarm_and_nodeData(sch)# return the swarm potions, target postion, bound and the counf of swarm
        #=============================================calculting thereshold
        # SwarmCPU_req,SwarmMem_req=returnResrourceUtilizationInTwoLists_dm(swarm_inf_as_dm)
        # NodeCPU_FreeCap, NodeMem_FreeCap = returnResrourceUtilizationInTwoLists_Node(ListOfNodeForhosting_DMs)
        # Total_CPU_utlization_byAlLswarm= sum(SwarmCPU_req)
        # Total_CPU_utization_byAllNodes = len(ListOfNodeForhosting_DMs)*128-NodeCPU_FreeCap
        # Total_CPU_nedded_byEach_node=(Total_CPU_utlization_byAlLswarm+Total_CPU_utization_byAllNodes)/len(ListOfNodeForhosting_DMs)
        # thershold=Total_CPU_nedded_byEach_node/(len(ListOfNodeForhosting_DMs)*128)
        # print("thershold  ->",thershold)
        # =============================================calculting thereshold end
        if len(swarm_inf_as_dm)>0:
                    pos = PSO(swarm_inf_as_dm)  # inital swarm
                    ListOfNodeForhosting_DMs=[sch]+ListOfNodeForhosting_DMs
                    # print("nod posstion",NodeXYpostion)
                    # for dm in swarm_inf_as_dm:
                    #     print("cpu uti by BM",dm.getDM_CPUUti()*2)#allocate each dm to instnace that has 2 vcpu and 8 GB of memeory
                    #     print("memory uti by BM", dm.getDM_MemUti()*8)
                #     print(swarmXYpostion)
                #for swarm in swarmXYpostion:

                    # print('count=',count)
                    # print('swarm length1=',len(swarm_inf_as_dm))
                    best_Pos = []

                    best_Pos=creatPointOfNodeRemainresourceUtilization(ListOfNodeForhosting_DMs)
                    index=0
                    countMigratedParticles = 0
                    while countMigratedParticles< count:
                            #print("get in while--->")
                            print("index", index)
                            print("count", count)
                            print("countMigratedParticles", countMigratedParticles)

                            if index==len(best_Pos):
                                index=0
                            eachPostion= best_Pos[index]
                            pos.PSO_method(fitnessFunction2, bounds, eachPostion, num_particles=count, maxiter=500)# swrm the particles to best distination
                            eachPostionOfNode_reprecenting_CPU=eachPostion[0]
                            eachPostionOfNode_reprecenting_Mem = eachPostion[1]
                            for particle in pos.swarm:
                                capcity_for_CPUfor_nodes=0
                                capcity_for_Memfor_nodes = 0
                                CreateReplica = -1
                                #print("particle.position_i[0]== eachPostion[0] and particle.position_i[1]== eachPostion[1] =",particle.position_i[0],"==", eachPostion[0] , particle.position_i[1],"==", eachPostion[1] )
                                # print("migrating status",particle.getDM_ReplicaToNode)

                                # if particle.particle_replicaTONode != -1:
                                #     print("replica machine id", particle.particle_replicaTONode)
                                if round(particle.position_i[0], 2)== round(eachPostion[0], 2) and round(particle.position_i[1], 2)== round(eachPostion[1] , 2)and particle.particle_cpu_req<= eachPostionOfNode_reprecenting_CPU*thershold and particle.particle_mem_req<= eachPostionOfNode_reprecenting_Mem*thershold and particle.particle_replicaTONode==-1:# when swarm reach the distinaion it ned to cheek the resource avalibailty and check the node that reach
                                        # print("I hcna migrtated hear")
                                        particle.particle_replicaTONode = ListOfNodeForhosting_DMs[index].node.getMachineID()# get the node id for the distination node Id to migrate it
                                        index += 1

                                        for inst in sch.instances:
                                                # if migratingStatus == 1:
                                                #     break
                                                # print("run for record migrating 2")
                                                for dm in inst.DMGraphs:
                                                    # print("run for record migrating 3")
                                                    # print("dm.getDM_ID()==particle.particle_DMname:",dm.getDM_ID(),"==",particle.particle_DMname)
                                                    # if migratingStatus==1:
                                                    #     break
                                                    if dm.getDM_ID()==particle.particle_DMname:
                                                        dm.setreplicaOnNode(particle.particle_replicaTONode)
                                                        countPOsMigrated+=1
                                                        print("done migrating",dm.getDM_ID())
                                                        #print("update Capacity before",eachPostion[0],eachPostion[1],eachPostionOfNode_reprecenting_CPU,eachPostionOfNode_reprecenting_Mem)
                                                        eachPostionOfNode_reprecenting_CPU-=particle.particle_cpu_req
                                                        eachPostionOfNode_reprecenting_Mem-= particle.particle_mem_req
                                                        #print("update Capacity After", eachPostion[0], eachPostion[1],
                                                                #eachPostionOfNode_reprecenting_CPU,
                                                                #eachPostionOfNode_reprecenting_Mem)
                                                        CreateReplica=1
                                                         #particle.particle_replicaTONode == 1
                                                        countMigratedParticles+=1
                                                        break
                                                if CreateReplica==1:

                                                    break
                                if CreateReplica==1:
                                    break
    print("here")
    print("# of migrated dm by pso",countPOsMigrated)

ParticleSwarmOptimizationMethod_with_RRA(PSO_withRRA_schedul)
#====================================
calculateDepedenciesConsideringTopology(PSO_withRRA_schedul, machines)


depInSamePM_rr,depInSamePod_sameSwitch_rr,depInSamePod_deffSwitch_rr,depInDeffPod_rr,latency_rr=calculatingLatencyBasedOnAlibabMetric(PSO_withRRA_schedul)
print("depInSamePM=", depInSamePM_rr,"depInSamePod_sameSwitch=",depInSamePod_sameSwitch_rr,"depInSamePod_deffSwitch=",depInSamePod_deffSwitch_rr,"depInDeffPod", depInDeffPod_rr,"latency=",latency_rr)

    # disply the results
# print(" all dependncies for out strategy=" ,calculateDepedenciesConsideringTopologyForSataelessandStaful(PSO_withRRA_schedul, machines))
# print(" all dependncies for Alibab =" ,calculateDepedenciesConsideringTopologyForSataelessandStaful(AlibabCluster, machines))
display_The_scheduling_result_andStatistics(AlibabCluster, PSO_withRRA_schedul, machines)
PSO_vertilization(PSO_withRRA_schedul)

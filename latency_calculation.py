def calculatingLatencyBasedOnAlibabMetric(schedul):
    dep_inSame_PM = 0
    dep_inSame_Pod_sameSwitch=0
    dep_inDeff_Pod_defferSwitch=0
    dep_inDeff_Pod=0
    latency=0
    for n in schedul:
        for ins in n.instances:
            for d in ins.DM_Dependencies:
                if d ==0:
                    dep_inSame_PM+=1
                elif d==2:
                    dep_inSame_Pod_sameSwitch += 1
                elif d==4:
                    dep_inDeff_Pod_defferSwitch+=1
                elif d==6:
                    dep_inDeff_Pod+=1
    latency=dep_inDeff_Pod*175
    return dep_inSame_PM ,dep_inSame_Pod_sameSwitch,dep_inDeff_Pod_defferSwitch,dep_inDeff_Pod,latency
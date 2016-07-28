import UseCaseInterface.avoid

'Functions to make the uav ables to identify what is around it'

'Function to create a list of obstacles which are in the range view of the UAV'
'The obstacles for this are statics objects, uav and pheromone'
def checksdobst(pheromonelist, x, y, speed, env):
    viewrange = speed + 2
    obstaclelist = env.get_static_objects()
    uavpositionlist = env.getUAVs()
    obstaclelistcheck = []
    onrange = False
    for i in range(0, len(obstaclelist)):
        obs = [obstaclelist[i].posx, obstaclelist[i].posy, obstaclelist[i].lenx, obstaclelist[i].leny]
        obsf = UseCaseInterface.avoid.obstacle_fun(obs)
        if y + viewrange > obsf[0] > y - viewrange:
            onrange = True
        elif y + viewrange > obsf[1] > y - viewrange:
            onrange = True
        elif x - viewrange < obsf[2] < x + viewrange:
            onrange = True
        elif x - viewrange < obsf[3] < x + viewrange:
            onrange = True
        if onrange:
            obstaclelistcheck.append([obstaclelist[i].posx, obstaclelist[i].posy, obstaclelist[i].lenx, obstaclelist[i].leny])
        onrange = False
    for uav_id, uav in uavpositionlist.items():
        uavp = [uav.posx, uav.posy]
        if x + viewrange > uavp[0] > x - viewrange:
            onrange = True
        elif y + viewrange > uavp[1] > y - viewrange:
            onrange = True
        if onrange:
            obstaclelistcheck.append([uav.posx, uav.posy, 0, 0])
    onrange = False
    for pherop in range(0, len(pheromonelist)):
        if pherop[0] > x - viewrange and pherop[1] < x + viewrange:
            onrange = True
        elif y + viewrange > pherop[1] > y - viewrange:
            onrange = True
        if onrange:
            obstaclelistcheck.append([pherop[0], pherop[1], 0, 0])
    return obstaclelistcheck

'Function to check if there is a Job in the range view of the UAV'
def checkjobrange(jobposlist, x, y, speed):
    viewrange = speed + 2
    i = 0
    joblistchek = []
    jobonrange = False
    for jobp in jobposlist:
        if not (not (jobposlist[2] == "Laying around") or not (x - viewrange < jobp[0] < x + viewrange)) or (
                    y + viewrange > jobp[1] > y - viewrange):
            jobonrange = True
        if jobonrange:
            joblistchek.append([jobp[0], jobp[1], jobp[2], jobp[3]])
    return joblistchek

'''
Function to select the closest job in the range view of the UAV
This function checks the distance between the uav and the job and select the closest
'''
def selectjob(joblistcheck, x, y, speed):
    viewrange = speed + 2
    i = 0
    closejobp = 0
    closejob = UseCaseInterface.avoid.distance([x, y], [x + viewrange, y + viewrange])
    for i in range(0, len(joblistcheck)):
        if UseCaseInterface.avoid.distance([x, y], joblistcheck[i]) < closejob:
            closejobp = i
    return joblistcheck[closejobp]

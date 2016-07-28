import math


'Avoidance Algorithm'
'This algorithm is based in the VFH algorithm.'
numvect = 17
turnrange = 5.0

'Function to determinate the angle between uav position and uav destination'


def angle(p0, p1):
    [x1, y1] = p0
    [x2, y2] = p1
    a = math.degrees(math.atan((y1 - y2) / (x1 - x2)))
    if x2 < x1:
        b = a + 90
        return b
    else:
        return a


'Function to determinate the distance between uav position and uav destination'


def distance(p0, p1):
    return math.sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)


'Function to determinate the factor of change in the coordinates'


def factordist(ang):
    ang = math.radians(ang)
    return [math.cos(ang), math.sin(ang)]


'Function to determinate the move position of the UAV'


def move(p0, ahg, dest, speed):
    v_fac = factordist(ahg)
    newx = p0[0] + speed * v_fac[1]
    newy = p0[1] + speed * v_fac[0]
    news = [newx, newy]
    if distance(p0, dest) < distance(p0, news):
        newx = p0[0] + math.sqrt((dest[0] - dest[1])**2) * v_fac[1]
        newy = p0[1] + math.sqrt((dest[0] - dest[1])**2) * v_fac[0]
        news = [newx, newy]
    return news


'Function to determinate functions for every obstacle in the list, to create borders'


def obstacle_fun(obs):
    obs_top = obs[1]
    obs_bot = obs[1] - obs[3]
    obs_lef = obs[0]
    obs_rig = obs[0] + obs[1]
    return [obs_top, obs_bot, obs_lef, obs_rig]


'Function to determinate intersection point between every vector field and obstacle functions in the x coordinate'


def xvect(angle_vector, sen_sadist, pos, obstacle, obs_lef, obs_rig):
    angle_vector = math.radians(angle_vector)
    xv = ((obstacle - pos[1]) * (sen_sadist * math.cos(angle_vector)) + pos[0] * (
        sen_sadist * math.sin(angle_vector))) / (sen_sadist * math.sin(angle_vector))
    yv = obstacle
    if xv > obs_lef < obs_rig or distance(pos, [xv, yv]) > sen_sadist:
        xv = pos[0]
        yv = pos[1]
    return [xv, yv]


'Function to determinate intersection point between every vector field and obstacle functions in the y coordinate'


def yvect(angle_vector, sen_sadist, pos, obstacle, obs_top, obs_bot):
    angle_vector = math.radians(angle_vector)
    yv = ((obstacle - pos[0]) * (sen_sadist * math.sin(angle_vector)) + pos[1] * (
        sen_sadist * math.cos(angle_vector))) / (sen_sadist * math.cos(angle_vector))
    xv = obstacle
    if yv > obs_top < obs_bot or distance(pos, [xv, yv]) > sen_sadist:
        yv = pos[1]
        xv = pos[0]
    return [xv, yv]


'''
Function to field the vector
This function creates an empty array list to fill it with the intersection position. The angles to evaluate are
determinate by the numbers of vector to create. The vector in every angle has the longest density by default. All the
obstacles are checked to determinate de density of the vector and all the intersections are reviewed to determinate if
the intersection is in the range view of the UAV.
'''


def vectorfield(position, obstacblelist, destination, speed):
    sensadist = speed + 2.0
    vectorsensor = []
    delt = 180 / (len(vectorsensor) - 1)
    if position[1] > destination[1]:
        delt *= -1
    for i in range(0, numvect):
        vecang = math.radians(i * delt)
        vectorsensor.append([position[0] + sensadist * math.cos(vecang), position[1] + sensadist * math.sin(vecang)])
        for obsta in obstacblelist:
            obstaf = obstacle_fun(obsta)
            if i * delt == 90:
                xvt = xvect(vecang, sensadist, position, obstaf[0], obstaf[2], obstaf[3])
                xvb = xvect(vecang, sensadist, position, obstaf[1], obstaf[2], obstaf[3])
                yvl = position
                yvr = position
            elif i * delt == 180:
                xvt = position
                xvb = position
                yvl = yvect(vecang, sensadist, position, obstaf[2], obstaf[0], obstaf[1])
                yvr = yvect(vecang, sensadist, position, obstaf[3], obstaf[0], obstaf[1])
            elif i * delt == 0:
                xvt = position
                xvb = position
                yvl = yvect(vecang, sensadist, position, obstaf[2], obstaf[0], obstaf[1])
                yvr = yvect(vecang, sensadist, position, obstaf[3], obstaf[0], obstaf[1])
            else:
                xvt = xvect(vecang, sensadist, position, obstaf[0], obstaf[2], obstaf[3])
                xvb = xvect(vecang, sensadist, position, obstaf[1], obstaf[2], obstaf[3])
                yvl = yvect(vecang, sensadist, position, obstaf[2], obstaf[0], obstaf[1])
                yvr = yvect(vecang, sensadist, position, obstaf[3], obstaf[0], obstaf[1])
            inter = [xvt, xvb, yvl, yvr]
            for intense in inter:
                den = distance(position, intense)
                denv = distance(position, vectorsensor[i])
                if den != 0 and den < denv:
                    vectorsensor[i] = intense
    return vectorsensor


'Function to determinate the closest vector to the heading destination'


def closevectgoal(vect, position, destination):
    angledest = angle(position, destination)
    difan = 360.0
    closevec = 0
    delt = 180 / (len(vect) - 1)
    if position[1] > destination[1]:
        delt *= -1
    for i in range(0, len(vect)):
        if angledest - i * delt < difan and difan > 0:
            difan = angledest - i * delt
            closevec = i
    return closevec


'Function to determinate which vector is close to the angle destination in the turn range to set the direction'


def densivector(position, vect, closevec):
    global vecthide
    hidens = 0
    for vecthide in range(int(closevec - turnrange), int(closevec + turnrange)):
        if distance(position, vect[vecthide]) > hidens:
            hidens = distance(position, vect[vecthide])
    return vecthide


'Function to determinate which vector has a useful density to set the direction'


def selectvector(position, vectorns, closevec, vecthide, speed):
    vectselect = closevec
    if distance(position, vectorns[closevec]) < distance(position, vectorns[vecthide]):
        vectselect = vecthide
    while distance(position, vectorns[vectselect]) < speed:
        if vectselect > len(vectorns):
            vectselect = 0
        else:
            vectselect += 1
        if vectselect == len((vectorns)):
            break
    return vectselect


'Final function to set the next UVA position with the avoidance algorithm'


def nextstep(position, destination, obstaclelistcheck, speed):
    if len(obstaclelistcheck) == 0:
        anglens = angle(position, destination)
        nexts = move(position, anglens, destination, speed)
    else:
        vectorns = vectorfield(position, obstaclelistcheck, destination, speed)
        closevecns = closevectgoal(vectorns, position, destination)
        vecthide = densivector(position, vectorns, closevecns)
        anglens = selectvector(position, vectorns, closevecns, vecthide, speed)
        nexts = move(position, anglens, destination, speed)
    return nexts


'''
Optimizations:
If there is no vector useful? One possible implementation could be changing the heading (from Up to Down
and the other way around)'
'''

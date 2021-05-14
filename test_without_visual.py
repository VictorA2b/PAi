import json_treatment as jt
import plan_treatment as pt
import numpy as np
import json
import soft_information
import os


"Amount of iteration"    
tmax = 3

"Initial mesh"
plan = pt.create_mesh(2000,1000)

Nx = len(plan[0])
Ny = len(plan)


"Adding the rooms"
pt.create_room(300,300,50,50,plan)
pt.create_room(900,40,330,130,plan)
pt.create_room(40,300,530,130,plan)
pt.create_room(600,200,400,430,plan)
pt.create_room(40,300,530,530,plan)
pt.create_room(30,500,100,330,plan)
pt.create_room(40,30,60,470,plan)
pt.create_room(800,200,60,770,plan)
pt.create_room(900,300,1000,60,plan)
pt.create_room(300,600,1600,160,plan)
pt.create_room(40,500,1200,300,plan)
pt.create_room(300,40,900,500,plan)
pt.create_room(200,200,1100,780,plan)


"Nuances"
delta = 4
plan_nuances = pt.create_nuances(plan,delta/Nx)
#Matrix is stored in order to be used for SCI
np.save(os.path.join("soft_information\data","plan_nuances"),plan_nuances)


"Scale of the picture choice"
scale = round(2000/Nx)

"Creation of inital plan picture"                  
im1 = pt.create_picture(plan,scale)
W, H = im1.size
px1 = im1.load()


"Scale of agent choice"
scaleagent = max(round(W/200),1) 

"Amount and inital position on the mesh of agents"
position_agent0 = [[210,200],
                   [540,250],
                   [1200,800],
                   [1700,500]]

"Placing the agent on the picture"
pt.place_agent(position_agent0,scaleagent,px1,(255,0,255))


"Stadard deviation of measure of each SI"
std_position = W/35
std_distance = 2*std_position
std_angle = 3
std_cap = 0.3


"Stores each type of coordinates for each agent for all iteration "
COORR = []
COORM = []
COORD = []

    
"Stores each type of coordinates for each agent at a given iteration"
position_agent = position_agent0
position_simulated =[]
position_SI = []
        

"Stores the velocity and heading for each agent at a given iteration"
velocity_agent=[]

#Arbitrary values
for i in position_agent0:
    velocity_agent.append([1e-2,0])


"Time counter"
time = 1
           
    
"Dictionary containing information on each agent (real positions, velocity and heading)"
data = {}
for i in range (0,len(position_agent)):
    data[('Agent ' + str(i+1))] = []
    data[('Agent ' + str(i+1))].append({'X' : position_agent[i][0], 'Y' : position_agent[i][1], 'speed' : velocity_agent[i][0], 'cap' : velocity_agent[i][1]})
       
    
"List containing information on each agent (measured positions, velocity and heading)"   
data_measured = []        
        
print('t = ' + str(time))
        


def SI(json_simulated,position_simulated):
        
    """
    Generate a the list of coordinatesfor each agent mentionned 
    in the standardised JSON file filled with measured information
    
    Args:
        json_simulated : JSON file in the standardised format of the 
        main program, filled with simulated measured information
        position_simulated : list of measured coordinates of each agent 
                
    Output:
        listeposbis : list of coordinates for each agent deduced thanks 
        to SI fusion
    """
    
    listepos=[]
    SI_list = soft_information.parse_scenario('soft_information\data\data_simulated.json')
    positions, _ = soft_information.compute_positions(SI_list, len(position_simulated), listepos)
    listeposbis = []
    for pos in positions:
        listeposbis.append([int(pos[0]),int(pos[1])])
    return(listeposbis)
     


def aberrant(position_SI):
        
    """
    Specify if the position deduced from the SI fusion are aberrant or 
    not (if the coordinates can be displayed or not). Criterion can be 
    improuved.
    
    Args:
        position_SI : list of deduced coordinates of each agent 
        
    Output:
        indicator : True if one or more coordinates is/are aberrant, 
        False ortherwise 
    """
            
    indicator = False 
    for coor in position_SI:
        if coor[0]<10 or coor[1]<10 or coor[0]>W or coor[1]>H:
            indicator = True
    return(indicator)           


def write_in_json(data,time):
        
    """
    Generates two standardised .JSON files filled with real and measured
    information.
    
    Args:
        data : Dictionary containing information on each agent (real positions,
        velocity and heading) 
        time : time
    """
        
    liste_info = []
    N = len(data)
        
    #time
    jt.add_time(time,liste_info)        
        
    #position
    for n in range(0,N):
        coor = data['Agent ' + str(n+1)][-1]
        jt.add_position(n,coor['X'],coor['Y'],std_position,liste_info)            
            
    #heading
    for n in range(0,N):
        info = data['Agent ' + str(n+1)][-1]
        jt.add_cap(n,info['cap'],std_cap,liste_info)                        

    #distance
    if N>1:
        for n in range(0,N-1):
            for k in range(n+1,N):
                coora = data['Agent ' + str(n+1)][-1]
                coorb = data['Agent ' + str(k+1)][-1]
                dist = np.sqrt((coora['X']-coorb['X'])**2+(coora['Y']-coorb['Y'])**2)
                jt.add_distance(n,k,round(dist*100)/100,std_distance,liste_info)        

    #angle
    if N>1:
        for n in range(0,N-1):
            for k in range(n+1,N):
                coora = data['Agent ' + str(n+1)][-1]
                coorb = data['Agent ' + str(k+1)][-1]
                u = [coorb['X']-coora['X'],coorb['Y']-coora['Y']]
                v = [np.cos(coora['cap'])*coora['speed'],np.sin(coora['cap'])*coora['speed']]
                theta = np.arccos((u[0]*v[0]+u[1]*v[1])/(np.sqrt(u[0]**2+u[1]**2)*np.sqrt(v[0]**2+v[1]**2)))
                jt.add_angle(n,k,round(theta),std_angle,liste_info)
        
        
    json_object = json.dumps(liste_info, indent = 4) 
    with open("soft_information\data\data_true.json", "w") as outfile: 
        outfile.write(json_object)
        
    jt.simulated_json("soft_information\data\data_true.json",
                      'soft_information\data\data_simulated.json')
                    



def suivi(time,position_agent,position_simulated,position_SI,velocity_agent,data,data_measured,COORR,COORM,COORD):
        
    """
    Represents an iteration of the algorithm : 
        -new real position, velocity and heading are generated thanks to 
        the random walk model for each agent
        -simulated measured datas are generated from them 
        -deduced datas are generated from the measured ones thanks to the 
        SI fusion and are tested
        -picture is refreshed 
        -each type of coordinates is saved
        
    Args:
        time : time
        position_agent : list of real coordinates of each agent 
        position_simulated : list of measured coordinates of each agent 
        position_SI : list of deduced coordinates of each agent by SI fusion
        velicity_agent : list of velocity and heading for each agent at a given 
        iteration
        data : Dictionary containing information on each agent (real positions,
        velocity and heading) 
        data_measure :  Dictionary containing information on each agent (measured
        positions,velocity and heading) 
        COORR,COORM,COORD : lists of each types of coordinates 
        
    """
        
    #new real position, velocity and heading are generated thanks to the 
    #random walk model for each agent
    new_pos_agent = []
    new_velocity_agent = []
    for i in range(0,len(position_agent)):
        (x,y,v,teta)=pt.random_walk(position_agent[i][0],position_agent[i][1],scaleagent,plan,4,1,0.3)
        new_pos_agent.append([x,y])
        new_velocity_agent.append([v,teta])
    position_agent=new_pos_agent
    velocity_agent=new_velocity_agent
            
    for i in range (0,len(position_agent)):
        data[('Agent ' + str(i+1))].append({'X' : position_agent[i][0], 'Y' : position_agent[i][1],'speed' : velocity_agent[i][0], 'cap' : velocity_agent[i][1]})
        
        
    #simulated measured datas are generated from them       
    write_in_json(data,time)
    data_measured = jt.json2coor('soft_information\data\data_simulated.json')
    position_simulated = []
    for i in range(0,len(data_measured)):
        position_simulated.append([data_measured[i]['Agent ' + str(i+1)]['X'],data_measured[i]['Agent ' + str(i+1)]['Y']])
        
        
    #deduced datas are generated from the measured ones thanks to the 
    #SI fusion and are tested
    position_SI = SI('soft_information\data\data_simulated.json',position_simulated)
    c=1
    while aberrant(position_SI) and c<10:
        c+=1
        position_SI = SI('soft_information\data\data_simulated.json',position_simulated)

        
    #each type of coordinates is saved
    COORD.append(position_SI)
    COORM.append(position_simulated)
    COORR.append(position_agent)
 
    
    
"------------------------------------Loop-------------------------------------" 
    
    

while time <= tmax:
    time += 1
    suivi(time,position_agent,position_simulated,position_SI,velocity_agent,data,data_measured,COORR,COORM,COORD)      
    print('t = ' + str(time))
        
    
    
"-----------------------------------------------------------------------------"    
    
    

"Data extraction for performance testing of the algorithm"
DISTRM = []
DISTRD = []

for t in range(0,tmax):
    for i in range(0,len(COORR[0])):
        DISTRM.append(np.sqrt((COORR[t][i][0]-COORM[t][i][0])**2+(COORR[t][i][1]-COORM[t][i][1])**2))
        DISTRD.append(np.sqrt((COORR[t][i][0]-COORD[t][i][0])**2+(COORR[t][i][1]-COORD[t][i][1])**2))


file2write=open("soft_information\data\distRM",'w')
file2write.write(str(DISTRM))
file2write.close()

file2write=open("soft_information\data\distRD",'w')
file2write.write(str(DISTRD))
file2write.close()


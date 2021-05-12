import json_treatment as jt
import plan_treatment as pt
from PIL import ImageTk
import numpy as np
import os

import json
import soft_information


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
im2 = pt.create_picture(plan,scale)  

W, H = im1.size
px1 = im1.load()
px2 = im2.load()

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


from tkinter import Tk, Button, Canvas
import tkinter

"Stores each type of coordinates for each agent for all iteration "
COORR = []
COORM = []
COORD = []

class Window(Tk):
    
    
    
    def __init__(self): 
                                                                   
        Tk.__init__(self)
        self.title('Plan du lieu')        
        self.plan = im1
        W, H = self.plan.size
        self.plan = self.plan.resize((1250, round(H/W*1250)))   
        self.canevas = Canvas(self)                 
        self.canevas.pack()
        
        #Stores each type of coordinates for each agent at a given iteration
        self.position_agent = position_agent0
        self.position_simulated =[]
        self.position_SI = []
        
        #Stores the velocity and heading for each agent at a given iteration
        self.velocity_agent=[]
        
        self.time = 1
        
        #Arbitrary values
        for i in position_agent0:
            self.velocity_agent.append([1e-2,0])
              
        self.photo = ImageTk.PhotoImage(self.plan)     
        self.canevas.create_image(0,0,anchor=tkinter.NW, image=self.photo,tags="tag")
        self.indic_auto = True
        self.canevas.config(height=self.photo.height(),width=self.photo.width())
        
        #Stores each type of coordinates for each agent for all iteration
        self.coorR = []
        self.coorM=[]
        self.coorD=[]
             
        h = tkinter.Frame(self)                                                                 #->un Frame
        h.pack(side=tkinter.LEFT, padx=5, pady=15)
     
        self._quitter=Button(h, text ='Quitter', command = self.quitter)
        self._quitter.pack(side=tkinter.RIGHT,padx = 5,pady = 5)                                #->un bouton 'Quitter'      

        self._suivi=Button(h, text ='Suivis', command = self.suivi)
        self._suivi.pack(side=tkinter.LEFT,padx = 5,pady = 5)      
        
        self._auto=Button(h, text ='Suivis automatique', command = self.auto)
        self._auto.pack(side=tkinter.LEFT,padx = 5,pady = 5)
                
        self._stop=Button(h, text ='Stop suivis', command = self.stop)
        self._stop.pack(side=tkinter.LEFT,padx = 5,pady = 5)      
        self._stop.config(state='disabled')
        
        #Dictionary containing information on each agent (real positions, velocity and heading)
        self.data = {}
        for i in range (0,len(self.position_agent)):
             self.data[('Agent ' + str(i+1))] = []
             self.data[('Agent ' + str(i+1))].append({'X' : self.position_agent[i][0], 'Y' : self.position_agent[i][1], 'speed' : self.velocity_agent[i][0], 'cap' : self.velocity_agent[i][1]})
         
        #List containing information on each agent (measured positions, velocity and heading)    
        self.data_measured = []        
        
        print('t = ' + str(self.time))
        


    def SI(self,json_simulated):
        
            """
            Generate a the list of coordinatesfor each agent mentionned 
            in the standardised JSON file filled with measured information
        
            Args:
                json_simulated : JSON file in the standardised format of the 
                main program, filled with simulated measured information
                
            Output:
                listeposbis : list of coordinates for each agent deduced thanks 
                to SI fusion
            """
    
            listepos=[]
            SI_list = soft_information.parse_scenario('data_simulated.json')
            positions, _ = soft_information.compute_positions(SI_list, len(self.position_simulated), listepos)
            listeposbis = []
            for pos in positions:
                listeposbis.append([int(pos[0]),int(pos[1])])
            return(listeposbis)
     


    def aberrant(self):
        
            """
            Specify if the position deduced from the SI fusion are aberrant or 
            not (if the coordinates can be displayed or not). Criterion can be 
            improuved.
        
            Output:
                indicator : True if one or more coordinates is/are aberrant, 
                False ortherwise 
            """
            
            indicator = False 
            for coor in self.position_SI:
                if coor[0]<10 or coor[1]<10 or coor[0]>W or coor[1]>H:
                    indicator = True
            return(indicator)           



    def suivi(self):
        
        """
        Represents an iteration of the algorithm : 
            -time is increased
            -new real position, velocity and heading are generated thanks to 
            the random walk model for each agent
            -simulated measured datas are generated from them 
            -deduced datas are generated from the measured ones thanks to the 
            SI fusion and are tested
            -picture is refreshed 
            -each type of coordinates is saved
        """
        
        #time is increased
        self.time += 1
        
        
        #new real position, velocity and heading are generated thanks to the 
        #random walk model for each agent
        new_pos_agent = []
        new_velocity_agent = []
        for i in range(0,len(self.position_agent)):
            (x,y,v,teta)=pt.random_walk(self.position_agent[i][0],self.position_agent[i][1],scaleagent,plan,4,1,0.3)
            new_pos_agent.append([x,y])
            new_velocity_agent.append([v,teta])
        self.position_agent=new_pos_agent
        self.velocity_agent=new_velocity_agent
            
        for i in range (0,len(self.position_agent)):
             self.data[('Agent ' + str(i+1))].append({'X' : self.position_agent[i][0], 'Y' : self.position_agent[i][1],'speed' : self.velocity_agent[i][0], 'cap' : self.velocity_agent[i][1]})
        
        
        #simulated measured datas are generated from them       
        self.write_in_json()
        self.data_measured = jt.json2coor('data_simulated.json')
        self.position_simulated = []
        for i in range(0,len(self.data_measured)):
            self.position_simulated.append([self.data_measured[i]['Agent ' + str(i+1)]['X'],self.data_measured[i]['Agent ' + str(i+1)]['Y']])
        
        
        #deduced datas are generated from the measured ones thanks to the 
        #SI fusion and are tested
        self.position_SI = self.SI('data_simulated.json')
        c=1
        while self.aberrant() and c<10:
            c+=1
            self.position_SI = self.SI('data_simulated.json')

        
        #picture is refreshed 
        photonew = pt.create_new_picture(im2,scaleagent,self.position_agent,self.position_simulated,self.position_SI)
        photonew = photonew.resize((1250, round(H/W*1250)))
        self.plan = ImageTk.PhotoImage(photonew)  

        self.canevas.itemconfigure(self.canevas.find_withtag("un"), image=self.plan)
        self.canevas.create_image(0,0, anchor = tkinter.NW , image=self.plan,tags="tag")
        
        
        #each type of coordinates is saved
        self.coorD.append(self.position_SI)
        self.coorM.append(self.position_simulated)
        self.coorR.append(self.position_agent)
        
        print('t = ' + str(self.time))
        
        
        
    def quitter(self):
        N = len(self.coorD)
        for i in range(0,N):
            for j in range(0,len(position_agent0)):
                COORR.append(self.coorR[i][j])
                COORM.append(self.coorM[i][j])
                COORD.append(self.coorD[i][j])
        self.destroy()

      
        
    def auto(self):
        self.indic_auto=True
        self.run()  



    def run(self):
        if self.indic_auto:
            self._stop.config(state='normal')
            self._auto.config(state='disabled')
            self.suivi()
            win.after(10, self.run)
        else:
            self._stop.config(state='disabled')
            self._auto.config(state='normal')

            
            
    def stop(self):
        self._stop.config(state='disabled')
        self._auto.config(state='normal')
        self.indic_auto=False

        
        
    def write_in_json(self):
        
        """
        Generates two standardised .JSON files filled with real and measured
        information.
        """
        
        liste_info = []
        data = self.data
        N = len(data)
        
        #time
        jt.add_time(self.time,liste_info)        
        
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
        with open("data_true.json", "w") as outfile: 
            outfile.write(json_object)
        
        jt.simulated_json("data_true.json",'data_simulated.json')
                    
        
        

                
win = Window()
win.mainloop()




"Data extraction for performance testing of the algorithm"
DISTRM = []
DISTRD = []

for i in range(0,len(COORR)):
    DISTRM.append(np.sqrt((COORR[i][0]-COORM[i][0])**2+(COORR[i][1]-COORM[i][1])**2))
    DISTRD.append(np.sqrt((COORR[i][0]-COORD[i][0])**2+(COORR[i][1]-COORD[i][1])**2))


file2write=open("soft_information\data\distRM",'w')
file2write.write(str(DISTRM))
file2write.close()

file2write=open("soft_information\data\distRD",'w')
file2write.write(str(DISTRD))
file2write.close()





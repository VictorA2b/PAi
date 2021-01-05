
import random as r
from PIL import Image, ImageTk
import copy


def create_maillage(l,L):
    maillage = []
    for y in range(0,L):
        maillage.append([1])
        for x in range(0,l-1):
            maillage[y].append(1)
    return(maillage)




def create_room(l,L,x0,y0,matrice):
    if x0+l >len(matrice[0]) and y0+L >len(matrice):
        return('Error')
    for x in range(x0,x0+l+1):
        for y in range(y0,y0+L+1):
            matrice[y][x] = 0
        
            
plan = create_maillage(2000,1000)
#
#plan = [[1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
#        [1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
#        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
#        [1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#        ]

Nx = len(plan[0])
Ny = len(plan)

scale = round(2000/Nx)


im1 = Image.new('RGB', (scale*Nx, scale*Ny))
im2 = Image.new('RGB', (scale*Nx, scale*Ny))
 
W, H = im1.size
px1 = im1.load()
px2 = im2.load()

scalecaptor = max(round(W/80),1) 


create_room(600,900,30,30,plan)
create_room(900,100,630,130,plan)
create_room(100,500,1530,130,plan)
create_room(500,450,1330,530,plan)

position = [[1500,400],
            [300,100],
            [700,500],
            [30,30]]

def add_captor(N,captor,W,H,scalecaptor):
    for i in range(0,N):
        captor.append([r.randint(round(scalecaptor/2+1),W-round(scalecaptor/2+1)), r.randint(round(scalecaptor/2+1),H-round(scalecaptor/2+1))])

add_captor(10,position,W,H,scalecaptor)

def create_picture(Nx,Ny,scale,px):
    for x in range(0,Nx):
        for y in range(0,Ny):
            if plan[y][x] == 0:
                for w in range(x*scale,scale*(x+1)):
                    for h in range(y*scale,scale*(y+1)):
                        px[w,h] = (255,255,255)
                   
create_picture(Nx,Ny,scale,px1)
create_picture(Nx,Ny,scale,px2)

def place_captors(position,scalecaptor,px):
    color = []            
    for coor in position:
        if  px[coor[0],coor[1]] == (255,255,255):
                color.append((0,255,0))
        else:
            color.append((255,0,0))
            
    for i in range(0,len(color)):
        coor = position[i]
        if color[i] == (0,255,0):
            for w in range(round(coor[0]-0.5*scalecaptor),round(coor[0]+0.5*scalecaptor)):
                for h in range(round(coor[1]-0.5*scalecaptor),round(coor[1]+0.5*scalecaptor)):
                         px[w,h] = (0,255,0)
        else:
            for w in range(round(coor[0]-0.5*scalecaptor),round(coor[0]+0.5*scalecaptor)):
                for h in range(round(coor[1]-0.5*scalecaptor),round(coor[1]+0.5*scalecaptor)):
                         px[w,h] = (255,0,0)
    
place_captors(position,scalecaptor,px1)
         
#im1.show()
#im2.show()
            
    
def create_new_plan(imageblanc):
    W, H = imageblanc.size
    position = []
    image_new = Image.new('RGB', (W,H))
    px = image_new.load()
    px1 = imageblanc.load()
    for w in range(0,W):
         for h in range(0,H):
             px[w,h] = px1[w,h]
    
    add_captor(10,position,W,H,max(round(W/80),1))
    place_captors(position,max(round(W/80),1),image_new.load())
    return(image_new)
    




from tkinter import Tk, Button, Canvas


#-------------------------------MonBouton--------------------------------------




        
#-------------------------------FenPrincipale----------------------------------      
   

    
#Enfin on définit la classe FenPrincipale, héritée de Tk, qui correspond à la fenetre
#principale avec laquelle le joueur interagira lorsqu'il jouera au pendu. 
            
class FenPrincipale(Tk):
    
    
    
    def __init__(self):                                                                    #Les différents attributs:
        Tk.__init__(self)
        self.title('Plan du lieu')                                                         
        

        self.plan = im1
        W, H = self.plan.size
        self.plan = self.plan.resize((1250, round(H/W*1250))) #->un objet PhotoImage  
        self.canevas = Canvas(self)                 
        self.canevas.pack()

        self.photo = ImageTk.PhotoImage(self.plan)     
                
        self.canevas.create_image(0,0,anchor=NW, image=self.photo,tags="tag")
  

        
        self.canevas.config(height=self.photo.height(),width=self.photo.width())
   
   

      
        h = Frame(self)                                                                 #->un Frame
        h.pack(side=LEFT, padx=5, pady=15)

        
        self.__quitter=Button(h, text ='Quitter', command = self.quitter)
        self.__quitter.pack(side=LEFT,padx = 5,pady = 5)                                #->un bouton 'Quitter'
        
        self.__quitter=Button(h, text ='Replacer capteurs', command = self.reload)
        self.__quitter.pack(side=LEFT,padx = 5,pady = 5)       

        self.__quitter=Button(h, text ='Suivis', command = self.reload)
        self.__quitter.pack(side=LEFT,padx = 5,pady = 5)       

        
        self.mainloop()
        


   
   
        
        
    def reload(self):
        photonew = create_new_plan(im2)
        photonew = photonew.resize((1250, round(H/W*1250)))
        self.plan = ImageTk.PhotoImage(photonew)  

        self.canevas.itemconfigure(self.canevas.find_withtag("un"), image=self.plan)
        self.canevas.create_image(0,0, anchor=NW, image=self.plan,tags="tag")
        self.mainloop()
  

        


        
    def quitter(self):

        self.destroy()
      
        
        
#Ouverture du jeu         
fen = FenPrincipale()
fen.mainloop()    




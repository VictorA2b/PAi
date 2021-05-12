from PIL import Image, ImageFilter
import numpy as np

"------------------------------------Plan-------------------------------------"    


def create_mesh(Nx,Ny):
    
    """
    Generate a matrix (Nx*Ny) filled with zeros 

    Args:
        Nx : length
        Ny : width
        
    Output:
        mesh : matrix (Nx*Ny) filled with zeros
    """
    
    mesh = []
    for y in range(0,Ny):
        mesh.append([0])
        for x in range(0,Nx-1):
            mesh[y].append(0)
    return(mesh)



def create_room(Nx,Ny,x0,y0,mesh):
    
    """
    Add an area (Nx*Ny) filled with ones starting at the point (x0,y0) to the 
    mesh

    Args:
        Nx : length
        Ny : width
        x0,y0 : starting point coordinates (top left corner)
        mesh : matrix to be modified
    """
    
    if x0+Nx >len(mesh[0]) and y0+Ny >len(mesh):
        return('Error')
    for x in range(x0,x0+Nx):
        for y in range(y0,y0+Ny):
            mesh[y][x] = 1
        
        
        
def create_nuances(mesh,deepness):           
                
    """
    Creates a Blured version of the mesh : the new mesh obtain represents the 
    mask of probability of presence of an agent in regard of the given plan

    Args:
        mesh : reference matrix
        deepness : closely linked to delta which represents the size of the area
        used for the calculation of each coefficient
        
     Output:
        mesh_bis : matrix (same size as mesh) filled with values between 0 and 1
        (mask of probability)
    """
                                                               
    Nx = len(mesh[0])
    delta = round(Nx*deepness)
    Ny = len(mesh)
    mesh_bis = create_mesh(Nx,Ny)
    
    for y in range (0,Ny):
        for x in range(0,Nx):

            if mesh[y][x]==0:
                
            
                if x + delta > Nx-1:
                    xsupp = Nx-1
                else :
                    xsupp = x + delta
                    
                if x - delta < 0:
                    xinf = 0
                else :
                    xinf = x - delta
                    
                if y + delta > Ny-1:
                    ysupp = Ny-1
                else :
                    ysupp = y + delta
                    
                if y - delta < 0:
                    yinf= 0
                else :
                    yinf = y - delta
                       
                somme = 0 
                
                for i in range(xinf,xsupp):
                    for j in range(yinf,ysupp):
                        if mesh[j][i]==1:
                            somme+=1
                
                ratio =  round(somme/((xsupp-xinf)*(ysupp-yinf))*100)/100

                mesh_bis[y][x] = ratio
                
            else:
                mesh_bis[y][x] = 1
    return(mesh_bis)           
    
            
    
def create_nuances_bis(image,deepness):
    "Alternative to create_nuance using ImageFilter function"    
    blurred_image = image.filter(ImageFilter.BoxBlur(deepness))
    return(blurred_image)
 
    
                                                              
def create_picture(mesh,scale):
                  
    """
    Creates a picture in shades of grey representing the given mesh. 

    Args:
        mesh : matrix
        scale : each value of the matrix will represent scale*scale pixels on 
        created picture
        
     Output:
        image : picture in shades of grey (the plan) with (Nx*scale)*(Ny*scale)
        pixels
    """
    
    Nx = len(mesh[0])
    Ny = len(mesh)
    image = Image.new('RGB', (scale*Nx, scale*Ny))
    px = image.load()
    for x in range(0,Nx):
        for y in range(0,Ny):
                for w in range(x*scale,scale*(x+1)):
                    for h in range(y*scale,scale*(y+1)):
                        level = int(mesh[y][x]*255)
                        px[w,h] = (level,level,level)
    return(image)
                       
    

    
    
    
"------------------------------------Agent------------------------------------"    


def place_agent(position,scaleagent,px,color):
                   
    """
    Add square shapped agentson a given picture

    Args:
        position : list of coordinates of the agents
        scaleagent : size in pixels of the agent  
        px : pixels of the given picture
        color : triplets of the square color

    """
    
    for coor in position:
        
        winf = int(round(coor[0]-0.5*scaleagent))
        wsup = int(round(coor[0]+0.5*scaleagent))
        hinf = int(round(coor[1]-0.5*scaleagent))
        hsup = int(round(coor[1]+0.5*scaleagent))  
        
        for w in range(winf,wsup):
            for h in range(hinf,hsup):
                px[w,h] = color


    
def create_new_picture(image_base,scaleagent,position_agent,position_simulated,position_SI):
    
    """
    Generates a new picture based on the initial site plan picture and the 
    of each type of agent

    Args:
        image_base : picture of the site plan
        scaleagent : size in pixels of the agent  
        position_agent : list of coordinates of the agents
        position_simulated : list of coordinates of the agents according to the 
        measures
        position_SI : list of coordinates of the agents according to the SI 
        algorithm

    Output:
        image_new : picture of the plan with the different type of agent placed
        on it
    """
    
    W, H = image_base.size
    image_new = Image.new('RGB', (W,H))
    px = image_new.load()
    px1 = image_base.load()
    for w in range(0,W):
         for h in range(0,H):
             px[w,h] = px1[w,h]

    #Legends color can be modified here"
    place_agent(position_agent,scaleagent,image_new.load(),(255,0,255))
    place_agent(position_simulated,scaleagent,image_new.load(),(255,0,0))
    place_agent(position_SI,scaleagent,image_new.load(),(0,0,255))
    
    return(image_new)
    


def random_walk(x0,y0,scaleagent,plan,vmean,vstd,delta_t):
    
    """
    Generates random coordinates, velocity and heading of a given agent at 
    t+delta_t based on its position at t, the site plan and normal law 
    distribution parameters

    Args:
        x0,y0 : coordinates of the agent at t
        scaleagent : size in pixels of the agent  
        position_agent : list of coordinates of the agents
        plan : matrix representing the site plan
        vmean : mean value for the normal law representing the volicity of the 
        agent
        vstd : standard deviation for the normal law representing the volicity 
        of the agent
        delta_t : amount of time between each iteration

    Output:
        x_new,y_new : generated coordinates
        v : velocity of the agent
        teta : heading of the agent
    """
    
    xmax = len(plan[0])-scaleagent
    ymax = len(plan)-scaleagent
    x_new = xmax+1
    y_new = ymax+1

    while (not(scaleagent <= x_new <= xmax) or not(scaleagent <= y_new <= ymax)) or plan[y_new][x_new] == 0:
        v = np.random.randn() * vstd + vmean
        distance = round(v * delta_t * scaleagent)
        teta = np.random.rand()*2*np.pi
        dep_X = round(np.cos(teta)*distance)
        dep_Y = round(np.sin(teta)*distance)
        x_new = int(x0 + dep_X)
        y_new = int(y0 + dep_Y)
        
    return(x_new,y_new,v,teta)





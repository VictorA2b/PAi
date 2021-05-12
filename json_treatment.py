import json 
import numpy as np
      
    
"-----------------Standardisation of the Soft Information---------------------"


"""
 The purpose of these functions is to create a list of standardised 
 dictionaries containing the SI data so that they can be used in the main 
 program. 
"""


def add_position(idx,X,Y,std,listinfo):
    
    """
    Add the SI related to the position as a dictionnary to a given list.

    Args:
        idx : agent ID
        X,Y : coordinates
        std : standard deviation of the measurement
        listinfo : list in which the dictionnary is added  
    """
    
    dictionary ={ 
            "SI_type": "position",
            "features": {
                    "idx": idx,
                    "measured_x": X,
                    "measured_y": Y,
                    "std":std
            } 
    }  
    listinfo.append(dictionary)
    
    
    
def add_distance(idxa,idxb,dist,std,listinfo):
    
    """
    Add the SI related to the distance as a dictionnary to a given list.

    Args:
        idxa : agent A ID
        idxb : agent B ID
        dist : measured distance between the two agents
        std : standard deviation of the measurement 
        listinfo : list in which the dictionnary is added  
    """
    
    dictionary ={ 
            "SI_type": "distance",
            "features": {
                    "idx_a":idxa,
                    "idx_b":idxb,
                    "measured_dist":dist,
                    "std":std
            } 
    }  
    listinfo.append(dictionary)
    
    
    
def add_angle(idxa,idxb,angle,std,listinfo):
    
    """
    Add the SI related to the angle as a dictionnary to a given list.

    Args:
        idxa : agent A ID
        idxb : agent B ID
        angle : measured angle between the two agents
        std : standard deviation of the measurement 
        listinfo : list in which the dictionnary is added  
    """
    
    dictionary ={ 
            "SI_type": "angle",
            "features": {
                    "idx_a": idxa,
		        	"idx_b": idxb,
                    "measured_angle": angle,
                    "std": std
            } 
    }  
    listinfo.append(dictionary)



def add_cap(idx,cap,std,listinfo):
    
    """
    Add the SI related to the heading as a dictionnary to a given list.

    Args:
        idx : agent ID
        cap : measured heading
        std : standard deviation of the measurement 
        listinfo : list in which the dictionnary is added  
    """
    
    dictionary ={ 
            "SI_type": "cap",
            "features": {
                   "idx": idx,
                   "measured_h": cap,
                   "std":std
            } 
    }  
    listinfo.append(dictionary)
 
    
    
def add_time(time,listeinfo):
    
        
    """
    Add the SI related to the time as a dictionnary to a given list.

    Args:
        time : measured time
        listinfo : list in which the dictionnary is added  
    """
    

    dictionary ={
        "SI_type": "time",
        "features": {
            "measured_time":time,
        }
    }
    listeinfo.append(dictionary)
    
    
    
    

    
"------------------------Generation of simulated data ------------------------"

"""
These functions return simulated measurements from real 
coordinates/angles/distance/heading (mean value) and sensor uncertainties
(standard deviations) from a normal distribution
"""

def simulated_position(X,Y,std):
    X_simulated = np.random.randn() * std + X
    Y_simulated = np.random.randn() * std + Y
    return(X_simulated,Y_simulated)

def simulated_distance(d,std):
    d_simulated = np.random.randn() * std + d
    return(d_simulated)

def simulated_angle(angle,std):
    angle_simulated = np.random.randn() * std + angle
    return(angle_simulated)
    
def simulated_cap(cap,std):
    cap_simulated = np.random.randn() * std + cap
    return(cap_simulated)



def simulated_json(filename_true,filename_simulated):
    
    """
    Generate a JSON file in the standardised format of the main program filled 
    with simulated measurements from a standardised JSON file with the exact 
    information of the agents.

    Args:
        filename_true : standardised JSON file filled with the exact information
        filename_simulated : JSON file, all the information it contains will 
        be deleted and replaced by the simulated measurements 
    """
    
    with open(filename_true, 'r') as openfile: 
        data_true = json.load(openfile) 
    N = len(data_true)
    
    for n in range(0,N):
        info = data_true[n]
        features = info['features']
        
        if info['SI_type'] == 'position':           
            (X,Y)=simulated_position(features['measured_x'],features['measured_y'],features['std'])
            data_true[n]['features']['measured_x']=round(X*100)/100
            data_true[n]['features']['measured_y']=round(Y*100)/100
            
        if info['SI_type'] == 'distance':           
            d=simulated_distance(features['measured_dist'],features['std'])
            data_true[n]['features']['measured_dist']=round(d*100)/100
            
        if info['SI_type'] == 'angle':           
            angle=simulated_angle(features['measured_angle'],features['std'])
            data_true[n]['features']['measured_angle']=round(angle)
            
        if info['SI_type'] == 'cap':           
            cap=simulated_cap(features['measured_h'],features['std'])
            data_true[n]['features']['measured_h']=round(cap*100)/100
        
    json_object = json.dumps(data_true, indent = 4) 
    with open(filename_simulated, "w") as outfile: 
        outfile.write(json_object)





"------------------------Convert JSON to coordinates--------------------------"


def json2coor(filename):
    
    """
    Generate a the list of coordinates (dictionnary) for each agent mentionned 
    in the standardised JSON file filled with information

    Args:
        filename : JSON file in the standardised format of the main program
        
    Output:
        list_coor : list of coordinates (dictionnary)
    """
    
    list_coor=[]
    with open(filename, 'r') as openfile: 
        data = json.load(openfile) 
        
    for info in data:
         if info['SI_type'] == 'position': 
             features = info['features']
             (X,Y)=(features['measured_x'],features['measured_y'])
             list_coor.append({('Agent '+str(features['idx']+1)): {'X': round(X), 'Y': round(Y)}})
             
    return(list_coor)
    
             

    
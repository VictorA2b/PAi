import json
import numpy as np
from scipy.optimize import minimize
from .utils import make_logprob_distance, make_logprob_position, make_logprob_angle, make_logprob_vitesse, make_logprob_cap, make_logprob_plan


T=[]

plan = np.load("soft_information\data\plan_nuances.npy")


def parse_scenario(file_name):
    with open(file_name, 'r') as file: #On extraie les données 
        si_list = json.load(file)
    return si_list


def json_parser(si_list): # a chaque SI on attribue une fonction make_logprob
    """Convert SI into function that return the likelihood of an estimation"""
    si_list_func = []

    for si_dict in si_list:
        SI_type = si_dict["SI_type"]
        features = si_dict["features"]
        if SI_type == 'distance':
            maker = make_logprob_distance
            logprob_func = maker(**features)
            si_list_func.append(logprob_func)
        elif SI_type == 'position':
            maker = make_logprob_position
            logprob_func = maker(**features)
            si_list_func.append(logprob_func)
        elif SI_type == 'angle':
            maker = make_logprob_angle
            logprob_func = maker(**features)
            si_list_func.append(logprob_func)
        elif SI_type == 'cap':
            maker = make_logprob_cap
            logprob_func = maker(**features)
            si_list_func.append(logprob_func)
        elif SI_type =='time':
            t= features['measured_time']
            T.append(t)            
    

    return si_list_func

def get_time():
    return T

def compute_positions(si_list, nb_points, listepos):
    """
    Return the most likely position considering the si_list and the global logprob function

    Args:
        si_list(list of dict): the soft information
        nb_points: number of points

    """
    si_list_func = json_parser(si_list)

    def global_logprob(points):
        "Returns the logprob of a given set of points under all SI"
        if listepos==[]:
             return np.sum([
            si_func(points) for si_func in si_list_func])
        else:
            S=0
            
            
            delta_t= T[-1]-T[-2]
            for i in range(len(points)):
                S+=make_logprob_vitesse(points[i],listepos[len(listepos)-1][i],delta_t) + make_logprob_plan(points[i],plan) #On ajoute la vitesse et le calque "plan" qui sont des SCI
            return np.sum([
            si_func(points) for si_func in si_list_func])+ S
            
       

    points = np.random.rand(nb_points, 3) #On initialise un point pour la minimisation, points est donc une matrice nb_points*3 car 3 coordonnées (x,y,h) où h est le cap suivi  par l'agent
    x0 = np.ravel(points)

    # since we use 'minimize', we have to take the opposite
    # of the logprob (I called it unlogprob)
    def unlogprob(x):
        # x shape is (3*nb_points,)
        points = x.reshape(nb_points, 3)
        return -global_logprob(points)

    # Finds the minima of the func 'unlogprob'
    # which is the most likely distribution of points
    estimated_x = minimize(unlogprob, x0, method='CG').x

    positions = estimated_x.reshape(nb_points, 3)

    return positions, global_logprob

# -*- coding: utf-8 -*-
"""A set of functions that make it easy to play with soft information"""

import numpy as np
from numpy import pi, exp, sqrt, log
from math import atan 
from math import atan2


#On se place dans un plan 2D, les points sont representés par leurs coordonnées (xa,ya,ha) où ha est le cap que suit cet agent 


def normal(x, mean, std):
    """
    Normal distribution

    Args:
        x: input value
        mean: the mean of the distribution
        std: standard deviation 
    """
    return 1/(std*sqrt(2*pi))*exp(-(x-mean)**2/(2*std**2)) 


def dist(xa, ya, xb, yb):
    """Return the distance between a and b"""
    a = np.array((xa, ya))
    b = np.array((xb, yb))
    return np.linalg.norm(a-b)




def log_normal(x, mean, std):
    """
    Natural logarithm of a normal distribution

    Args:
        x: input value
        mean: the mean of the distribution
        std: standard deviation 
    """
    return -log(std) - (log(2) + log(pi))/2 - (x-mean)**2/(2*std**2)

def logprob_angle(xa, ya, xb, yb,ha,measured_angle, std):
    """logprob that a, b and c are in (xa,ya),(xb,yb),(xc,yc) under the measured angle.
    
    Args:
        xa: abscissa of point a
        ya: ordinate of point a
        xb: abscissa of point b
        yb: ordinate of point b
        measured_dist: measured distance between a and b
        std: standard deviation of the measurement"""
    

    angle= atan2((yb-ya),(xb-xa))-ha #Calcul de l'angle entre un agent A et le cap d'un autre agent B
    return log_normal(angle, measured_angle, std)

def logprob_distance(xa, ya, xb, yb, measured_dist, std):
    """
    Logprob that a and b are in (xa, ya), (xb, yb) under the measured distance.

    Args:
        xa: abscissa of point a
        ya: ordinate of point a
        xb: abscissa of point b
        yb: ordinate of point b
        measured_dist: measured distance between a and b
        std: standard deviation of the measurement
    """
    points_dist = dist(xa, ya, xb, yb)
    return log_normal(points_dist, measured_dist, std)



def make_logprob_angle(idx_a, idx_b, measured_angle, std):
    """
    Make the function that return the logprob of positions under the measured distance

    Args:
        idx_a: index of point a
        idx_b: index of point b
        idx_c : index of point c
        measured_angle : measured angle between a b and c
        std: standard deviation of the measurement
    """
    def func(points):
        """
        Return the logprob of positions under the measured distance

        Args:
            points: estimated positions ([[x0, y0, h0], [x1, y1, h1], ...])
        """
        xa, ya, ha = points[idx_a] #Chaque point à un identifiant id, les coordonnées sont récuperées avec ces identifiant 
        xb, yb, hb = points[idx_b]
        return logprob_angle(xa, ya, xb, yb,ha,measured_angle, std)

    return func
    
    
def make_logprob_distance(idx_a, idx_b, measured_dist, std):
    """
    Make the function that return the logprob of positions under the measured distance

    Args:
        idx_a: index of point a
        idx_b: index of point b
        measured_dist: measured distance between a and b
        std: standard deviation of the measurement
    """
    def func(points):
        """
        Return the logprob of positions under the measured distance

        Args:
            points: estimated positions ([[x0, y0, h0], [x1, y1, h1], ...])
        """
        xa, ya, ha = points[idx_a]
        xb, yb, hb = points[idx_b]
        return logprob_distance(xa, ya, xb, yb, measured_dist, std)

    return func

def make_logprob_vitesse(pos,posprecedent,delta_t):
#    delta_t= liste_temps[-1]-liste_temps[-2]
#    print(delta_t)
    x=pos[0]
    y=pos[1]
    x_precedent=posprecedent[0]
    y_precedent=posprecedent[1]
    print(x_precedent)
    print(y_precedent)
    distance = dist(x,y,x_precedent,y_precedent)
    vitesse = distance/delta_t
    if vitesse <= 6 :
        return log(1/7)
    if vitesse > 6 and vitesse <= 12: 
        return log((1/7)*exp(-vitesse+6))
    else : 
        return -10000 # Si la vitesse est trop grande alors la probabilité est tres faible on soustrait donc 10000 car on maximise la fonction likelihood. On fait une distinction avec la condition obtenue car on obtenai des log(0) car la densité de probabilité était trop faible. -10000 est une valeur arbitraire. 
        
    


def make_logprob_position(idx, measured_x, measured_y, std):

    """
    Returns the soft position information function that can be applied to the estimated positions

    Args:
        idx: index of point
        measured_x: measured abscissa
        measured_y: measured ordinate
        std: standard deviation of the measurement

    Returns:
        (function): the logSI function that takes the estimated positions of the points as input.
    """
    def func(points):
        """
        Returns log-prob of the estimated positions under the measured position.

        Args:
            points: estimated positions ([[x0, y0, h0], [x1, y1, h1], ...])
        """
        estimated_x, estimated_y, estimated_h = points[idx]
        return logprob_distance(estimated_x, estimated_y, measured_x, measured_y, 0, std)

    return func

def make_logprob_cap(idx, measured_h, std):

    """
    Returns the soft position information function that can be applied to the estimated positions

    Args:
        idx: index of point
        measured_x: measured abscissa
        measured_y: measured ordinate
        std: standard deviation of the measurement

    Returns:
        (function): the logSI function that takes the estimated positions of the points as input.
    """
    def func(points):
        """
        Returns log-prob of the estimated positions under the measured position.

        Args:
            points: estimated positions ([[x0, y0, h0], [x1, y1, h1], ...])
        """
        estimated_x, estimated_y, estimated_h = points[idx]
        return logprob_distance(estimated_h, 0, measured_h, 0, 0, std)

    return func

def make_logprob_plan(point,plan): #On utilise un maillage, la variable plan. Le maillage est un quadrillage où aux intersections il y a la probabilité de présence. Un agent n'est pas obligé d'être sur les intersections donc on fait une distinction en fonction de la position de l'agent par rapport aux points du maillage
    x=point[0]
    y=point[1]
    partx=int(x)
    party=int(y)
#    print(partx)
#    print(party)
#    print(plan[partx][party])
    if x== partx :  # On est dans le cas où le point est sur une ligne verticale du maillage 
        if y==party: # On est sur une ligne horizontale du maillage 
            return log(plan[x][y] + 10^(-5)) #On rajoute 10^(-5) pour ne pas avoir un log(0), 10^(-5) est arbitraire 
        else : #On est entre deux lignes horizontale
            return log(((y-party)*plan[x][party] + (party+1-y)*plan[x][party+1] + (y-party)*plan[x+1][party] + (party+1-y)*plan[x+1][party+1])/2 + 10^(-5))
    else: 
        if y==party: # On est sur une ligne horizontale du maillage 
            return log(((x-partx)*plan[partx][y] + (partx+1-x)*plan[partx+1][y] + (x-partx)*plan[partx][y+1] + (partx+1-x)*plan[partx+1][y+1])/2 + 10^(-5))
        else: 
            a= (y-party)*plan[partx][party] + (party+1-y)*plan[partx][party+1]
            b= (y-party)*plan[partx+1][party] + (party+1-y)*plan[partx+1][party+1]
            c= (x-partx)*plan[partx][party] + (partx+1-x)*plan[partx+1][party]
            d= (x-partx)*plan[partx][party+1] + (partx+1-x)*plan[partx+1][party+1]
            return log((a+b+c+d)/4+ 10**(-5))
        
        
        
        
    
import soft_information
pas_temps=1


listepos=[] #initialisation de la liste des positions
listepos_temps=[] #initialisation de la liste des temps
SI_list = soft_information.parse_scenario('data_simulated.json') #extraction des données 
positions, _ = soft_information.compute_positions(SI_list, 4, listepos) #Utilisation de la fonction compute_positions dans le init avec 4 points
print(positions.round(3))



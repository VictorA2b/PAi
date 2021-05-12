#Indoor location using Soft Information fusion
 
 This algorithm was developed with the aim of producing a reliable indoor location method for the Paris fire brigade. 
 It uses soft information (from sensors with high uncertainties) compiled in a .JSON file to return the most probable positions of the different agents in the field.
 
 ## Installation
 
 Require following labraries :
 - math
 - numpy
 - PIL
 - os
 - tkinter
 
 ## Usage
 
Use 'main.py' to determine the most likely positions of agents based on the given .JSON file filled with Soft Information (position, heading, angle, distance and time). 
The plan of the intervention site (Soft Context Information) must be saved as 'soft_information\data\plan_nuances.npy' before usage.

Use 'test_with_visual.py' or 'test_without_visual.py' to generate data from a simulated test. Agents randomly move around a map. 
Measures are simulated from their position, speed and heading. Finally, new coordinates are deduces from this measures thanks to the fusion of SI. 
Differences between the real and measured data and between the real and deduced data are stored in 'distRM.txt' and 'distRD.txt'.
Following visuals can be obtained :
 
pink = real data
red  = measured data
blue = deduced from SI data 
 
![Alt text](soft_information\data\test_with_visual.gif) / ! [](soft_information\data\test_with_visual.gif)
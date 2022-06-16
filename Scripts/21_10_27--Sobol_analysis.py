import numpy as np
import pandas as pd
from SALib.sample import saltelli
from SALib.analyze import sobol

#region
problem = {
    'num_vars': 17,
    'names': ['glazing_ratio', 'wall_u_value', 'window_u_value', 'window_sghc', 'infiltration_rate', 'chiller_cop', #6
              'indoor_temp_set_point', 'equipment_load_density', 'lighting_load_density', 'occupancy_density',  #4
              'wall_albedo', 'roof_albedo', 'wall_emissivity', 'roof_emissivity',  #5
              'floor_height', 'ventilation_rate', 'roof_u_value'],  #2
              
    'bounds': [[0.235, 0.074],       #glazing_ratio
               [27.5, 11.4],       #wall_u_value
               [0.7, 0.222],    #window_u_value
               [0.59, 0.08],     #window_sghc
               [-0.43, 0.802],       #infiltration_rate
               [4.45, 0.85],      #chiller_cop
               
               [27, 1.2],    #indoor_temp_set_point
               [1.8, 0.4],    #equipment_load_density
               [1.9, 0.3],    #lighting_load_density
               [0.26, 0.1],  # occupancy_density ---- 10


               [0.5, 0.07],  # wall_albedo ----- 20
               [0.5, 0.07],  # roof_albedo
               [0.475, 0.18],  # wall_emissivity
               [0.475, 0.18],  #roof_emissivity
               
               [1.1, 0.062],  #floor_height
               [-0.03 , 0.222],   #ventilation_rate
               [74.5, 31.5]   #roof_u_value  0.118 - 0.0880
               
               ],
    
    'dists':['norm', 'norm','lognorm', 'norm', 'lognorm', 'norm', 'norm', 'lognorm', 'lognorm',
             'norm', 'norm', 'norm', 'norm', 'norm', 'lognorm', 'lognorm', 'norm' ]  
}



# sample        
param_values = saltelli.sample(problem, 2653)

#endregion
df = pd.read_csv("E:\\ARCHIVE\\BAP\\__Project\\csvexport\\sobol-building_characteristics-22-10.csv")

Y = df['temp_average']

Y = Y.values

print(Y.shape)
print(Y)

Si_Temp = sobol.analyze(problem, Y)
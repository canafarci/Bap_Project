from operator import index, le
from uwg import Material, Element, Building, BEMDef, SchDef, UWG
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import pvlib
import numpy as np
import pandas as pd

def custom_uwg(glazing_ratio, wall_u_value, window_u_value, window_sghc, infiltration_rate, chiller_cop, indoor_temp_set_point, equipment_load_density,
                lighting_load_density, occupancy_density): 
    """Generate UWG json with custom reference BEMDef and SchDef objects."""

    

    # SchDef PARAMETERS -----------------------------------------------------------------------

    default_week = [[0.15] * 24] * 3
    occ_week = [[0.3] * 24] * 3
    
    elec_week = [[0.45, 0.41, 0.39, 0.38, 0.38, 0.43, 0.54, 0.65, 0.66, 0.67, 0.69, 0.7, 0.69, 0.66, 0.65, 0.68, 0.8, 1, 1, 0.93, 0.89, 0.85, 0.71, 0.58], 
                 [0.45, 0.41, 0.39, 0.38, 0.38, 0.43, 0.54, 0.65, 0.66, 0.67, 0.69, 0.7, 0.69, 0.66, 0.65, 0.68, 0.8, 1, 1, 0.93, 0.89, 0.85, 0.71, 0.58], 
                 [0.45, 0.41, 0.39, 0.38, 0.38, 0.43, 0.54, 0.65, 0.66, 0.67, 0.69, 0.7, 0.69, 0.66, 0.65, 0.68, 0.8, 1, 1, 0.93, 0.89, 0.85, 0.71, 0.58]]
    
    light_week = [[0.067, 0.067, 0.067, 0.067, 0.187, 0.394, 0.44, 0.393, 0.172, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.206, 0.439, 0.616, 0.829, 0.986, 1, 0.692, 0.384, 0.16], 
                  [0.067, 0.067, 0.067, 0.067, 0.187, 0.394, 0.44, 0.393, 0.172, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.206, 0.439, 0.616, 0.829, 0.986, 1, 0.692, 0.384, 0.16], 
                  [0.067, 0.067, 0.067, 0.067, 0.187, 0.394, 0.44, 0.393, 0.172, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.206, 0.439, 0.616, 0.829, 0.986, 1, 0.692, 0.384, 0.16]]
    
    cool_week = [[indoor_temp_set_point] * 24] * 3
    
    heat_week = [[23] * 24] * 3
    
    
    schdef1 = SchDef(elec=elec_week, gas=default_week, light=light_week,
                     occ=occ_week, cool=cool_week, heat=heat_week,
                     q_elec=equipment_load_density, q_gas=3.2, q_light=lighting_load_density,
                     n_occ=(1 / occupancy_density), vent=0.001 * 0.2, bldtype='midriseapartment',
                     builtera='pre80')
    
    ###-----------------------------------------------------------------------------------------



    # MATERIAL PARAMETERS ------------------------------------------------------------------------------------------------
    
    wallmt3 = Material(0.73, 1360000, 'brick')

    roofmtl = Material(0.84, 1520000, 'tile')
    roofmt2 = Material(1.6, 1887000, 'concrete_floor')


    ###-------------------------------------------------------------------------------------------------------------------


    
    # ELEMENT PARAMETERS ---------------------------------------------------------------------------
    
    wall = Element(0.35, 0.90, [wall_u_value, wall_u_value],  [wallmt3, wallmt3], 0, 296, False, 'common_brick_wall_with_plaster')
    roof = Element(0.25, 0.95, [0.025, 0.025], [roofmtl, roofmtl], 0, 296, True, 'tile')
    mass = Element(0.20, 0.90, [0.15, 0.15], [roofmt2, roofmt2], 0, 296, True, 'concrete_floor')

    ### ---------------------------------------------------------------------------------------------



    # BUILDING PARAMETERS -----------------------------------------------------------------------------------------------

    bldg = Building(
        floor_height=3, int_heat_night=1, int_heat_day=1, int_heat_frad=1,
        int_heat_flat=1, infil=infiltration_rate, vent=0.001 * 0.2, glazing_ratio=glazing_ratio, u_value=window_u_value,
        shgc=window_sghc, condtype='AIR', cop=chiller_cop, coolcap=900, heateff=0.8, initial_temp=300)

    bemdef1 = BEMDef(building=bldg, mass=mass, wall=wall, roof=roof, bldtype='midriseapartment', builtera='pre80')
    
    ###------------------------------------------------------------------------------------------------------------------


    # VECTOR---------------------------------------------------------------------------------------
    
    ref_sch_vector = [schdef1]
    ref_bem_vector = [bemdef1]
    
    bld = [('midriseapartment', 'pre80', 1)  # overwrite
           ]  # extend

    epw_path = "E:\\ARCHIVE\\BAP\\__Project\\data\\izmir.epw"
    
    ###-------------------------------------------------------------------------------------------


    
    # UWG PARAMETERS ------------------------------------------------------------------------------------------------
    
    model = UWG.from_param_args(
        epw_path=epw_path, bldheight=12, blddensity=0.27, vertohor=0.7, zone='3A',
        treecover=0, grasscover=0, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector, month=7, day=10, sensanth=19.6, nday=7, dtsim=300, albroad=0.20, 
        new_epw_name="sensepw2.epw",
        charlength=250, croad=2250000,albveg=0.25,vegend=10,vegstart=3,droad=1.25,kroad=0.8,
        maxday=200, maxnight=50, h_ubl1=750, h_ubl2=75, h_mix=0.9)
    
    ###---------------------------------------------------------------------------------------------------------------

    
    model.generate()
    model.simulate()
    
    model.write_epw()

problem = {
    'num_vars': 10,
    'names': ['glazing_ratio', 'wall_u_value', 'window_u_value', 'window_sghc', 'infiltration_rate', 'chiller_cop', 
              'indoor_temp_set_point', 'equipment_load_density', 'lighting_load_density', 'occupancy_density'],
              
    'bounds': [[0.225, 0.0558333],  # glazing_ratio
               [4.105, 1.0641],  # wall_u_value
               [1.85, 0.3166],  # window_u_value
               [0.475, 0.085],  # window_sghc
               [1.0, 1.5],  # infiltration_rate
               [3.3, 0.2333],  # chiller_cop
               [22, 1.3333],  # indoor_temp_set_point
               [5, 0.8333],  # equipment_load_density
               [5, 0.8333],  # lighting_load_density
               [25, 60]],  # occupancy_density

    
    'dists': ['norm', 'norm', 'norm', 'norm', 'unif', 
              'norm', 'norm', 'norm', 'norm', 'unif']
}

# sample        
param_values = saltelli.sample(problem, 512)

max_length = len(param_values)


        
glazing_ratio_list = []
wall_u_value_list = []
window_u_value_list = []
window_sghc_list = []
infiltration_rate_list = []
chiller_cop_list = []
indoor_temp_set_point_list = []
equipment_load_density_list = []
lighting_load_density_list = []
occupancy_density_list = []
simulation_result_list = []

iteration_list = range(1, len(param_values) + 1)



# evaluate
def evaluate_epw():
    k = 0
    l = 0
    m = 0
    y = np.zeros((max_length, 24))
    for params in param_values:
        try:
            print(float(params[0]), float(params[1]), float(params[2]), float(params[3]), float(params[4]), 
                  float(params[5]), float(params[6]) , float(params[7]), float(params[8]), float(params[9]) )
            
            glazing_ratio_list.append(float(params[0]))
            wall_u_value_list.append(float(params[1]))
            window_u_value_list.append(float(params[2]))
            window_sghc_list.append(float(params[3]))
            infiltration_rate_list.append(float(params[4]))
            chiller_cop_list.append(float(params[5]))
            indoor_temp_set_point_list.append(float(params[6]))
            equipment_load_density_list.append(float(params[7]))
            lighting_load_density_list.append(float(params[8]))
            occupancy_density_list.append(float(params[9]))
            
            custom_uwg(float(params[0]), float(params[1]), float(params[2]), float(params[3]), float(params[4]), 
                       float(params[5]), float(params[6]), float(params[7]), float(params[8]), float(params[9]))
            pd_epw_sens, _ = pvlib.iotools.read_epw(
                "E:\\ARCHIVE\\BAP\\__Project\\data\\sensepw2.epw")
                
            indexes =  range(4561, 4729)
            
            temp_list = temp_list = np.zeros((7, 24))
            
            j = 0
            n = 0
            for i in indexes:
                if (n > 6):
                    n = 0
                    
                temp_list[n][j % 24] = pd_epw_sens['temp_air'].values[i]
                j+= 1
                n+=1
            
            column_means = temp_list.mean(axis=0)
            
            for i in range(0, 24):
                y[k][i] = column_means[i]
            
            print(np.average(temp_list))
            k += 1
            m +=1
            print("************ CURRENT ITERATION: " + str(int(m)) + " / " + str(max_length) +  " EXCEPTIONS: " + str(l) + " ************")
        except Exception as e:
            print("EXCEPTION OCCURED")
            print(e)
            y[k] = 24
            k += 1
            l += 1
            m +=1
            print("************ CURRENT ITERATION: " + str(int(m)) + " / " + str(max_length) +  " EXCEPTIONS: " + str(l) + " ************")
            pass
    
    print(y)
    return y

y = evaluate_epw()



#y = np.loadtxt("E:\\ARCHIVE\\BAP\\uwg\\txtexport\\weeklytry.txt")
np.savetxt("E:\\ARCHIVE\\BAP\\__Project\\txtexport\\weeklytry.txt", y)

#sobol_indices = [sobol.analyze(problem, Y) for Y in y.T]
sobol_indices = []

for i in range(0, 24):
    sobol_indices.append(sobol.analyze(problem, y.T[i]))
    
print(sobol_indices)

lines = [str(sobol_indices)]
with open('E:\\ARCHIVE\\BAP\\__Project\\txtexport\\weektry.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')

            
"""        
                


# analyse
Si = sobol.analyze(problem, Y)

print(Y.size)
print(Y)

print(Si['S1'])

print(Si['S2'])

print(Si['ST'])            
            
print(Si)

print(str(len(equipment_load_density_list)) + " " + str(len(simulation_result_list)) + " " + str(len(iteration_list)))


data = {'Iteration': iteration_list, 'glazing_ratio': glazing_ratio_list, 'wall_u_value': wall_u_value_list, 'window_u_value': window_u_value_list,
        'window_sghc': window_sghc_list, 'infiltration_rate': infiltration_rate_list, 'chiller_cop': chiller_cop_list, 'indoor_temp_set_point': indoor_temp_set_point_list,
        'equipment_load_density': equipment_load_density_list, 'lighting_load_density': lighting_load_density_list, 'occupancy_density': occupancy_density_list} 
 
df = pd.DataFrame(data) 

df.to_csv("E:\\ARCHIVE\\BAP\\uwg\\csvexport\\izmir_weekly_3a.csv") 

lines = [str(Si)]
with open('E:\\ARCHIVE\\BAP\\uwg\\txtexport\\readme.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')
        
"""



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
    elec_week = [[7] * 24] * 3
    light_week = [[16] * 24] * 3
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

    epw_path = "E:\\ARCHIVE\\BAP\\uwg\\data\\TUR_Ankara.171280_IWEC_UWG.epw"
    
    ###-------------------------------------------------------------------------------------------


    
    # UWG PARAMETERS ------------------------------------------------------------------------------------------------
    
    model = UWG.from_param_args(
        epw_path=epw_path, bldheight=12, blddensity=0.27, vertohor=0.7, zone='5A',
        treecover=0, grasscover=0, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector, month=7, day=10, sensanth=19.6, nday=7, dtsim=150, albroad=0.20, 
        new_epw_name="sensepw.epw",
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
    'bounds': [[0.1, 0.2],       #glazing_ratio
               [0.1, 0.24],       #wall_u_value
               [2.25, 4.25],    #window_u_value
               [0.45, 0.75],     #window_sghc
               [0.1, 0.7],       #infiltration_rate
               [2, 4],      #chiller_cop
               [20, 24],    #indoor_temp_set_point
               [10, 16],    #equipment_load_density
               [7, 13],    #lighting_load_density
               [15, 25]]    #occupancy_density
}

# sample        
param_values = saltelli.sample(problem, 1024)
print(param_values)
print(len(param_values))
max_length = len(param_values)




# evaluate
def evaluate_epw():
    k = 0
    l = 0
    m = 0
    y = np.zeros([max_length])
    for params in param_values:
        try:
            print(float(params[0]), float(params[1]), float(params[2]), float(params[3]), float(params[4]), float(params[5]), float(params[6]) , float(params[7]), float(params[8]), float(params[9]) )
            custom_uwg(float(params[0]), float(params[1]), float(params[2]), float(params[3]), float(params[4]), float(params[5]), float(params[6]), float(params[7]), float(params[8]), float(params[9]))
            pd_epw_sens, _ = pvlib.iotools.read_epw("E:\\ARCHIVE\\BAP\\uwg\\data\\sensepw.epw")
                
            indexes =  range(4561, 4729)
            temp_list = np.zeros([len(indexes)])
            j = 0
            for i in indexes:
                temp_list[j] = pd_epw_sens['temp_air'].values[i]
                j+= 1
                
            y[k] = np.average(temp_list)
            print(np.average(temp_list))
            k += 1
            m +=1
            print("************ CURRENT ITERATION: " + str(int(m)) + " / " + str(max_length) +  " EXCEPTIONS: " + str(l) + " ************")
        except Exception:
            print("EXCEPTION OCCURED")
            y[k] = 24
            k += 1
            l += 1
            m +=1
            print("************ CURRENT ITERATION: " + str(int(m)) + " / " + str(max_length) +  " EXCEPTIONS: " + str(l) + " ************")
            pass
        
    return y
            
            
        
                
Y = evaluate_epw()

# analyse
Si = sobol.analyze(problem, Y)

print(Y.size)
print(Y)

print(Si['S1'])

print(Si['S2'])

print(Si['ST'])            
            
print(Si)  
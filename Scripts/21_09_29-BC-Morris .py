from operator import index, le
from uwg import Material, Element, Building, BEMDef, SchDef, UWG
import SALib
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
from SALib.sample import morris as _morris
from SALib.analyze import morris
import pvlib
import numpy as np
import pandas as pd



base_path = "E:\\ARCHIVE\\BAP\\__Project\\"

def custom_uwg(glazing_ratio, wall_u_value, window_u_value, window_sghc, infiltration_rate, chiller_cop, indoor_temp_set_point, equipment_load_density,
                lighting_load_density, occupancy_density,

                bld_height, ver_to_hor, bld_density, urban_road_volumetric_heat_capacity, urban_area_length, road_albedo, sensible_anthropogenic_heat,
                
                urban_road_thermal_conductivity, urban_road_thickness,
               
               wall_albedo, roof_albedo, wall_emissivity, roof_emissivity, roof_vegetation_coverage,
               
               floor_height, ventilation_rate):
              
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
    
    wall_material = Material(0.73, 1360000, 'brick')

    roof_material = Material(0.84, 1520000, 'tile')
    roofmt2 = Material(1.6, 1887000, 'concrete_floor')


    ###-------------------------------------------------------------------------------------------------------------------


    
    # ELEMENT PARAMETERS ---------------------------------------------------------------------------
    
    wall = Element(wall_albedo, wall_emissivity, [wall_u_value, wall_u_value],  [wall_material, wall_material], 0, 296, False, 'common_brick_wall_with_plaster')
    roof = Element(roof_albedo, roof_emissivity, [0.025, 0.025], [roof_material, roof_material], roof_vegetation_coverage, 296, True, 'tile')
    mass = Element(0.20, 0.90, [0.15, 0.15], [roofmt2, roofmt2], 0, 296, True, 'concrete_floor')

    ### ---------------------------------------------------------------------------------------------



    # BUILDING PARAMETERS -----------------------------------------------------------------------------------------------

    bldg = Building(
        floor_height=floor_height, int_heat_night=1, int_heat_day=1, int_heat_frad=1,
        int_heat_flat=1, infil=infiltration_rate, vent=ventilation_rate, glazing_ratio=glazing_ratio, u_value=window_u_value,
        shgc=window_sghc, condtype='AIR', cop=chiller_cop, coolcap=900, heateff=0.8, initial_temp=300)

    bemdef1 = BEMDef(building=bldg, mass=mass, wall=wall, roof=roof, bldtype='midriseapartment', builtera='pre80')
    
    ###------------------------------------------------------------------------------------------------------------------


    # VECTOR---------------------------------------------------------------------------------------
    
    ref_sch_vector = [schdef1]
    ref_bem_vector = [bemdef1]
    
    bld = [('midriseapartment', 'pre80', 1)  # overwrite
           ]  # extend

    epw_path = base_path + "data\\izmir.epw"
    
    ###-------------------------------------------------------------------------------------------


    
    # UWG PARAMETERS ------------------------------------------------------------------------------------------------
    
    model = UWG.from_param_args(
        epw_path=epw_path, bldheight=bld_height, blddensity=bld_density, vertohor=ver_to_hor, zone='3A',
        treecover=0, grasscover=0, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector, month=7, day=10, sensanth=sensible_anthropogenic_heat, nday=7, dtsim=120, albroad=road_albedo,
        new_epw_name="sensepw.epw",
        charlength=urban_area_length,  albveg=0.3, vegend=10, vegstart=3, droad=urban_road_thickness, kroad=urban_road_thermal_conductivity,
        croad=urban_road_volumetric_heat_capacity
        )
    
    ###---------------------------------------------------------------------------------------------------------------

    
    model.generate()
    model.simulate()
    
    model.write_epw()

problem = {
    'num_vars': 26,
    'names': ['glazing_ratio', 'wall_u_value', 'window_u_value', 'window_sghc', 'infiltration_rate', 'chiller_cop', #6
              
              'indoor_temp_set_point', 'equipment_load_density', 'lighting_load_density', 'occupancy_density',  #4

              'bld_height', 'ver_to_hor', 'bld_density', 'urban_road_volumetric_heat_capacity', 'urban_area_length', 'road_albedo', 'sensible_anthropogenic_heat',#7

              'urban_road_thermal_conductivity', 'urban_road_thickness', #2
              
              'wall_albedo', 'roof_albedo', 'wall_emissivity', 'roof_emissivity', 'roof_vegetation_coverage', #5
              'floor_height', 'ventilation_rate'],  #2
              
    'bounds': [[0.05, 0.4],       #glazing_ratio
               [0.9125, 7.3],       #wall_u_value
               [0.6, 2.9],    #window_u_value
               [0.39, 0.75],     #window_sghc
               [0.1, 0.7],       #infiltration_rate
               [2.6, 4],      #chiller_cop
               [18, 26],    #indoor_temp_set_point
               [2.5, 7.5],    #equipment_load_density
               [2.5, 7.5],    #lighting_load_density
               [25, 60],  # occupancy_density

               [10, 60],  # bld_height
               [0.48, 1.55],  # ver_to_hor
               [0.15, 0.35],  # bld_density --------
               [1200000, 2250000],  # urban_road_volumetric_heat_capacity ----
               [800, 1200],  # urban_area_length
               [0.085, 0.245],  # road_albedo
               [15, 25],  # sensible_anthropogenic_heat

               [0.8, 2],  # urban_road_thermal_conductivity
               [0.25, 0.75],  # urban_road_thickness


               [0, 1],  # wall_albedo
               [0, 1],  # roof_albedo
               [0, 1],  # wall_emissivity
               [0, 1],  #roof_emissivity
               [0, 1],   #roof_vegetation_coverage
               
               [2.5, 4],  #floor_height
               [0.001 , 0.010]   #ventilation_rate
               
               ]  
}

# sample        
X = _morris.sample(problem, 256, num_levels=4)


max_length = len(X)


        
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

iteration_list = range(1, len(X) + 1)



# evaluate
def evaluate_epw():
    k = 0
    l = 0
    m = 0
    y = np.zeros([max_length])
    for params in X:
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
                       float(params[5]), float(params[6]), float(params[7]), float(params[8]), float(params[9]), 
                       #urban characteristics
                       float(params[10]), float(params[11]), float(params[12]), float(params[13]), float(params[14]),float(params[15]), float(params[16]),
                       #meteorological factors
                       float(params[17]), float(params[18]), float(params[19]), float(params[20]), float(params[21]), float(params[22]),
                       
                       float(params[23]), float(params[24]), float(params[25])
                       
                       
                        )
            pd_epw_sens, _ = pvlib.iotools.read_epw(
                base_path + "data\\sensepw.epw")
                
            indexes =  range(4561, 4729)
            temp_list = np.zeros([len(indexes)])
            j = 0
            for i in indexes:
                temp_list[j] = pd_epw_sens['temp_air'].values[i]
                j+= 1
                
            y[k] = np.average(temp_list)
            
            simulation_result_list.append(np.average(temp_list))
            print(np.average(temp_list))
            k += 1
            m +=1
            print("************ CURRENT ITERATION: " + str(int(m)) + " / " + str(max_length) +  " EXCEPTIONS: " + str(l) + " ************")
        except Exception as e:
            print("EXCEPTION OCCURED")
            print(e)
            y[k] = y[k-1]
            k += 1
            l += 1
            m +=1
            print("************ CURRENT ITERATION: " + str(int(m)) + " / " + str(max_length) +  " EXCEPTIONS: " + str(l) + " ************")
            pass
        
    return y
            

Y = evaluate_epw()

#Y = np.loadtxt(base_path + "txtexport\\izmir_morris.txt")

                        #"txtexport\\izmir_morris.txt"
                        #_izmir_morris_9-29
np.savetxt(base_path + "txtexport\\128_izmir_morris_9-29.txt", Y)

# analyse
Si = morris.analyze(
    problem, X, Y, conf_level=0.95, print_to_console=True, num_levels=4)


print(str(len(equipment_load_density_list)) + " " + str(len(simulation_result_list)) + " " + str(len(iteration_list)))


""" data = {'Iteration': iteration_list, 'glazing_ratio': glazing_ratio_list, 'wall_u_value': wall_u_value_list, 'window_u_value': window_u_value_list,
        'window_sghc': window_sghc_list, 'infiltration_rate': infiltration_rate_list, 'chiller_cop': chiller_cop_list, 'indoor_temp_set_point': indoor_temp_set_point_list,
        'equipment_load_density': equipment_load_density_list, 'lighting_load_density': lighting_load_density_list, 'occupancy_density': occupancy_density_list, 'simulation_result': simulation_result_list} 
 
df = pd.DataFrame(data) 


df.to_csv(base_path + "csvexport\\izmir_morris_9-29.csv") """


lines = [str(Si)]
with open(base_path + 'txtexport\\128_izmir_morris_9-29.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')

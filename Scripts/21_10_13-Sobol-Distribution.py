from operator import index, le
from uwg import Material, Element, Building, BEMDef, SchDef, UWG
import SALib
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import pvlib
import numpy as np
import pandas as pd



base_path = "E:\\ARCHIVE\\BAP\\__Project\\"

def custom_uwg(glazing_ratio, wall_u_value, window_u_value, window_sghc, infiltration_rate, chiller_cop, indoor_temp_set_point, equipment_load_density,
                lighting_load_density, occupancy_density,

                bld_height, ver_to_hor, bld_density, urban_road_volumetric_heat_capacity, urban_area_length, road_albedo, sensible_anthropogenic_heat,
                
                urban_road_thermal_conductivity, urban_road_thickness,
               
               wall_albedo, roof_albedo, wall_emissivity, roof_emissivity, roof_vegetation_coverage,
               
               floor_height, ventilation_rate, roof_u_value):
              
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
                     n_occ=(occupancy_density), vent=0.001 * 0.2, bldtype='midriseapartment',
                     builtera='pre80')
    
    ###-----------------------------------------------------------------------------------------



    # MATERIAL PARAMETERS ------------------------------------------------------------------------------------------------
    
    mineral_plaster = Material(0.54, 1300 * 900, 'mineral_plaster')
    
    
    cement_plaster = Material(0.721, 1762 * 840, 'cement_plaster') # 1.1116299705    - 0.21 --- 0.132045 ||| 0.5 ---0.561214
    eps = Material(0.035, 22 * 1400, 'eps')
    brick_wall = Material(0.33, 900 * 600, 'brick_wall') 
    
    gypsum_plaster = Material(0.51, 1200 * 840, 'gypsum_plaster')
    
    
    
    
    
    glasswool = Material(0.04, 18 * 670, 'glasswool')
    
    gravel = Material(0.36, 840 * 1840, 'gravel')
    waterproofing = Material(0.19, 780 * 3000, 'waterproofing')
    
    reinforced_concrete = Material(2.5, 840 * 2400, 'reinforced_concrete')


    ###-------------------------------------------------------------------------------------------------------------------

    if roof_u_value < 0.01:
        roof_u_value = 0.01
    if wall_u_value < 0.01:
        wall_u_value = 0.01
    
    # ELEMENT PARAMETERS ---------------------------------------------------------------------------
    
    wall = Element(wall_albedo, wall_emissivity, [0.002, 0.03, wall_u_value, 0.135, 0.02],  [mineral_plaster, cement_plaster, eps, brick_wall, gypsum_plaster], 0, 296, False, 'common_brick_wall_with_plaster')
    roof = Element(roof_albedo, roof_emissivity, [roof_u_value, 0.12, 0.02], [glasswool, reinforced_concrete, gypsum_plaster], roof_vegetation_coverage, 296, True, 'tile')
    mass = Element(0.20, 0.90, [0.15, 0.15], [reinforced_concrete, reinforced_concrete], 0, 296, True, 'concrete_floor')

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
        ref_sch_vector=ref_sch_vector, month=7, day=10, sensanth=sensible_anthropogenic_heat, nday=7, dtsim=150, albroad=road_albedo,
        new_epw_name="sensepw.epw",
        charlength=urban_area_length,  albveg=0.3, vegend=10, vegstart=3, droad=urban_road_thickness, kroad=urban_road_thermal_conductivity,
        croad=urban_road_volumetric_heat_capacity
        )
    
    ###---------------------------------------------------------------------------------------------------------------

    
    model.generate()
    model.simulate()
    
    model.write_epw()

problem = {
    'num_vars': 27,
    'names': ['glazing_ratio', 'wall_u_value', 'window_u_value', 'window_sghc', 'infiltration_rate', 'chiller_cop', #6
              
              'indoor_temp_set_point', 'equipment_load_density', 'lighting_load_density', 'occupancy_density',  #4

              'bld_height', 'ver_to_hor', 'bld_density', 'urban_road_volumetric_heat_capacity', 'urban_area_length', 'road_albedo', 'sensible_anthropogenic_heat',#7

              'urban_road_thermal_conductivity', 'urban_road_thickness', #2
              
              'wall_albedo', 'roof_albedo', 'wall_emissivity', 'roof_emissivity', 'roof_vegetation_coverage', #5
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

               [2.5, 0.7],  # bld_height
               [0.62, 0.5],  # ver_to_hor
               [0.45, 0.105],  # bld_density --------
               [1960371 , 300000],  # urban_road_volumetric_heat_capacity ----
               [1000, 100],  # urban_area_length  ---- 15
               [0.1776, 0.024],  # road_albedo
               [7, 1.2],  # sensible_anthropogenic_heat

               [1.955, 0.4],  # urban_road_thermal_conductivity
               [0.3302, 0.05175],  # urban_road_thickness


               [0.5, 0.07],  # wall_albedo ----- 20
               [0.5, 0.07],  # roof_albedo
               [0.475, 0.18],  # wall_emissivity
               [0.475, 0.18],  #roof_emissivity
               [0.5, 0.18],   #roof_vegetation_coverage
               
               [1.1, 0.062],  #floor_height
               [-0.03 , 0.222],   #ventilation_rate
               [74.5, 31.5]   #roof_u_value  0.118 - 0.0880
               
               ],
    
    'dists':['norm', 'norm', 'lognorm', 'norm', 'lognorm', 'norm', 'norm', 'lognorm', 'lognorm', 'norm',
             'lognorm', 'lognorm', 'norm', 'norm', 'norm', 'norm', 'norm', 'norm', 'norm', 'norm',
             'norm', 'norm', 'norm', 'norm', 'norm', 'lognorm', 'norm' ]  
}

# sample        
param_values = saltelli.sample(problem, 1024)


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
    y = np.zeros([max_length])
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
                       float(params[5]), float(params[6]), float(params[7]), float(params[8]), float(params[9]), 
                       #urban characteristics
                       float(params[10]), float(params[11]), float(params[12]), float(params[13]), float(params[14]),float(params[15]), float(params[16]),
                       #meteorological factors
                       float(params[17]), float(params[18]), float(params[19]), float(params[20]), float(params[21]), float(params[22]),
                       
                       float(params[23]), float(params[24]), float(params[25]), float(params[26])
                       
                       
                        )
            pd_epw_sens, _ = pvlib.iotools.read_epw(
                base_path + "data\\sensepw.epw")
                
            indexes =  range(4561, 4729)
            temp_list = np.zeros([len(indexes)])
            j = 0
            for i in indexes:
                temp_list[j] = pd_epw_sens['temp_air'].values[i]
                j+= 1
                
                #HDD = if temperature is lesser than 18.3C ,  max(0, 18.3 - t)
                #CDD =if temperature is bigger than 23.3 ,  max (0, t-23.3)
                #use hourly instead of daily method
                
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
np.savetxt(base_path + "txtexport\\sobol-dists-27.txt", Y)

# analyse
Si = sobol.analyze(problem, Y)


print(str(len(equipment_load_density_list)) + " " + str(len(simulation_result_list)) + " " + str(len(iteration_list)))


""" data = {'Iteration': iteration_list, 'glazing_ratio': glazing_ratio_list, 'wall_u_value': wall_u_value_list, 'window_u_value': window_u_value_list,
        'window_sghc': window_sghc_list, 'infiltration_rate': infiltration_rate_list, 'chiller_cop': chiller_cop_list, 'indoor_temp_set_point': indoor_temp_set_point_list,
        'equipment_load_density': equipment_load_density_list, 'lighting_load_density': lighting_load_density_list, 'occupancy_density': occupancy_density_list, 'simulation_result': simulation_result_list} 
 
df = pd.DataFrame(data) 


df.to_csv(base_path + "csvexport\\izmir_morris_9-29.csv") """


lines = [str(Si)]
with open(base_path + 'txtexport\\sobol-dists-27-results.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')

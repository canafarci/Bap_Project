from math import nan
from operator import index, le
from numpy.lib.function_base import average
from uwg import Material, Element, Building, BEMDef, SchDef, UWG
import SALib
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import pvlib
import numpy as np
import pandas as pd

base_path = "E:\\ARCHIVE\\BAP\\__Project\\"

def custom_uwg(bld_height, ver_to_hor, bld_density, urban_road_volumetric_heat_capacity, road_albedo, 
              sensible_anthropogenic_heat, urban_road_thermal_conductivity, 
              
              glazing_ratio, wall_u_value, window_u_value, window_sghc, infiltration_rate, 
              chiller_cop, indoor_temp_set_point, equipment_load_density, lighting_load_density, occupancy_density,
               wall_albedo, roof_albedo, wall_emissivity, roof_emissivity, floor_height,
                roof_u_value):
              
    """Generate UWG json with custom reference BEMDef and SchDef objects."""
    
    global epw_name_index

#region ERROR CHECKS  ------------------------------------------------------------------------------------------------------------
    if bld_height < 2.39:
        bld_height = 2.30
    elif bld_height > 62:
        bld_height = 62
        
    if ver_to_hor < 0.58:
        ver_to_hor = 0.58
    elif ver_to_hor > 5.94:
        ver_to_hor = 5.94
        
    if bld_density < 0.2057:
        bld_density = 0.2057
    elif bld_density > 0.6942:
        bld_density = 0.6942
        
    if urban_road_volumetric_heat_capacity < 1264700:
        urban_road_volumetric_heat_capacity = 1264700
    elif urban_road_volumetric_heat_capacity > 2658280:
        urban_road_volumetric_heat_capacity = 2658280
        
    if road_albedo < 0.1217:
        road_albedo = 0.1217
    elif road_albedo > 0.2334:
        road_albedo = 0.2334
        
    if sensible_anthropogenic_heat < 8.36:
        sensible_anthropogenic_heat = 8.36
    elif sensible_anthropogenic_heat > 31.63:
        sensible_anthropogenic_heat = 31.63
        
    if urban_road_thermal_conductivity < 1.02:
        urban_road_thermal_conductivity = 1.02
    elif urban_road_thermal_conductivity > 2.885:
        urban_road_thermal_conductivity = 2.885
        
    if glazing_ratio < 0.09:
        glazing_ratio= 0.09
    elif glazing_ratio > 0.58:
        glazing_ratio = 0.58
        
    if wall_u_value < 0.18:
        wall_u_value = 0.18
    elif wall_u_value > 2.93:
        wall_u_value = 2.93
        
    if window_u_value < 1.69:
        window_u_value = 1.69
    elif window_u_value > 4.059:
        window_u_value = 4.059
        
    if window_sghc < 0.42:
        window_sghc = 0.42
    elif window_sghc > 0.83:
        window_sghc = 0.83
        
    if infiltration_rate < 0.1:
        infiltration_rate = 0.1
    elif infiltration_rate > 4.18:
        infiltration_rate = 4.18
        
    if chiller_cop < 2.4726:
        chiller_cop = 2.4726
    elif chiller_cop > 6.4274:
        chiller_cop = 6.4274
        
    if indoor_temp_set_point < 20:
        indoor_temp_set_point = 20
    elif indoor_temp_set_point > 24:
        indoor_temp_set_point = 24
        
    if equipment_load_density < 3.48:
        equipment_load_density = 3.48   
    elif equipment_load_density > 5.71:
        equipment_load_density = 5.71
        
    if lighting_load_density < 3.19:
        lighting_load_density = 3.19
    elif lighting_load_density > 5.6:
        lighting_load_density = 5.6
        
    if occupancy_density < 0.02:
        occupancy_density = 0.02
    elif occupancy_density > 0.03333:
        occupancy_density = 0.03333
        
    if wall_albedo < 0.3371:
        wall_albedo = 0.3371
    elif wall_albedo > 0.6628:
        wall_albedo = 0.6628
        
    if roof_albedo < 0.3371:
        roof_albedo = 0.3371
    elif roof_albedo > 0.6628:
        roof_albedo = 0.6628
        
    if wall_emissivity < 0.0562:
        wall_emissivity = 0.0562
    elif wall_emissivity > 0.8937:
        wall_emissivity = 0.8937
        
    if roof_emissivity < 0.0562:
        roof_emissivity = 0.0562
    elif roof_emissivity > 0.8937:
        roof_emissivity = 0.8937
        
    if floor_height < 2.62:
        floor_height = 2.62
    elif floor_height > 3.17:
        floor_height = 3.17
        
    if roof_u_value < 0.157:
        roof_u_value = 0.157
    elif roof_u_value > 1.362:
        roof_u_value = 1.362
        
    
        
#endregion  

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
                     q_elec=equipment_load_density, q_gas=lighting_load_density, q_light=7.5,
                     n_occ=occupancy_density, vent=0.001 * 0.2, bldtype='midriseapartment',
                     builtera='pre80')
    
    ###-----------------------------------------------------------------------------------------



    # MATERIAL PARAMETERS ------------------------------------------------------------------------------------------------
    
    wallmt3 = Material(0.73, 1360000, 'brick')

    roofmtl = Material(0.84, 1520000, 'tile')
    roofmt2 = Material(1.6, 1887000, 'concrete_floor')


    ###-------------------------------------------------------------------------------------------------------------------

    
    wall_thickness = 0.73 / wall_u_value
    roof_thickness = 1.6 / roof_u_value
    
    # ELEMENT PARAMETERS ---------------------------------------------------------------------------
    
    wall = Element(wall_albedo, wall_emissivity, [wall_thickness, 0.01],  [wallmt3, wallmt3], 0, 296, False, 'common_brick_wall_with_plaster')
    roof = Element(roof_albedo, roof_emissivity, [roof_thickness, 0.025], [roofmtl, roofmtl], 0, 296, True, 'tile')
    mass = Element(0.20, 0.90, [0.15, 0.15], [roofmt2, roofmt2], 0, 296, True, 'concrete_floor')

    ### ---------------------------------------------------------------------------------------------



    # BUILDING PARAMETERS -----------------------------------------------------------------------------------------------

    bldg = Building(
        floor_height=floor_height, int_heat_night=1, int_heat_day=1, int_heat_frad=1,
        int_heat_flat=1, infil=infiltration_rate, vent=0.98, glazing_ratio=glazing_ratio, u_value=window_u_value,
        shgc=window_sghc, condtype='AIR', cop=chiller_cop, coolcap=900, heateff=0.8, initial_temp=300)

    bemdef1 = BEMDef(building=bldg, mass=mass, wall=wall, roof=roof, bldtype='midriseapartment', builtera='pre80')
    
    ###------------------------------------------------------------------------------------------------------------------


    # VECTOR---------------------------------------------------------------------------------------
    
    ref_sch_vector = [schdef1]
    ref_bem_vector = [bemdef1]
    
    bld = [('midriseapartment', 'pre80', 1)  # overwrite
           ]  # extend

    epw_path = base_path + "data\\TUR_Ankara.171280_IWEC.epw"
    
    ###-------------------------------------------------------------------------------------------


    
    # UWG PARAMETERS ------------------------------------------------------------------------------------------------
    
    model = UWG.from_param_args(
        epw_path=epw_path, bldheight=bld_height, blddensity=bld_density, vertohor=ver_to_hor, zone='4B',
        treecover=0, grasscover=0, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector, month=8, day=17, sensanth=sensible_anthropogenic_heat, nday=7, dtsim=180, albroad=road_albedo,
        new_epw_name="SIMULATION.epw",
        charlength=250,  albveg=0.3, vegend=10, vegstart=3, kroad=urban_road_thermal_conductivity,
        croad=urban_road_volumetric_heat_capacity
        )
    
    ###---------------------------------------------------------------------------------------------------------------
   
    
    model.generate()
    model.simulate()
    
    model.write_epw()
    
#region Parameter Definition ------------------------------
problem = {
    'num_vars': 23,
    'names': ['bld_height', 'ver_to_hor', 'bld_density', 'urban_road_volumetric_heat_capacity', 'road_albedo', #5
              'sensible_anthropogenic_heat', 'urban_road_thermal_conductivity', #7
              
              'glazing_ratio', 'wall_u_value', 'window_u_value', 'window_sghc', 'infiltration_rate', 'chiller_cop', #13
              'indoor_temp_set_point', 'equipment_load_density', 'lighting_load_density', 'occupancy_density',  #17
              'wall_albedo', 'roof_albedo', 'wall_emissivity', 'roof_emissivity',  #21
              'floor_height',  'roof_u_value' #23
              ],  #2
              
    'bounds': [[2.716, 0.349],       #bld_height
               [0.62, 0.5],       #ver_to_hor
               [0.45, 0.105],    #bld_density
               [1960371, 300000],     #urban_road_volumetric_heat_capacity
               [0.1776, 0.024],      #road_albedo
               
               [20, 5],    #sensible_anthropogenic_heat
               [1.955, 0.4],    #urban_road_thermal_conductivity
               
               [-1.462, 0.400],       #glazing_ratio
               [-0.301, 0.592],       #wall_u_value
               [0.965, 0.187],    #window_u_value
               [-0.519, 0.143],     #window_sghc
               [-0.43, 0.802],       #infiltration_rate
               [4.45, 0.85],      #chiller_cop
               
               [20, 24],    #indoor_temp_set_point
               [4.6, 0.48],    #equipment_load_density
               [4.4, 0.42],    #lighting_load_density
               [0.02665, 0.00443],  # occupancy_density ---- 10


               [0.5, 0.07],  # wall_albedo ----- 20
               [0.5, 0.07],  # roof_albedo
               [0.475, 0.18],  # wall_emissivity
               [0.475, 0.18],  #roof_emissivity
               
               [1.059, 0.041],  #floor_height
               [-0.771, 0.464]   #roof_u_value
            
               ],
    
    'dists':['lognorm', 'lognorm','norm', 'norm',  'norm', #5
             'norm', 'norm',  #7
             
             'lognorm', 'lognorm','lognorm', 'lognorm', 'lognorm', 'norm', #13
             
             'unif', 'norm', 'norm', 'norm', #17
             
             'norm', 'norm', 'norm', 'norm', #21
             
             'lognorm', 'lognorm' #23
             
             
              ]  
}

#endregion

param_values = saltelli.sample(problem, 1024) #1400

#region CSV index lists definition -------------------------
max_length = len(param_values)

bld_height_list = []
ver_to_hor_list = []
bld_density_list = []
urban_road_volumetric_heat_capacity_list = []
road_albedo_list = []
sensible_anthropogenic_heat_list = []
urban_road_thermal_conductivity_list = []

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
wall_albedo_list = []
roof_albedo_list = []
wall_emissivity_list = []
roof_emissivity_list = []
floor_height_list = []
roof_u_value_list = []

temp_result_list = []
hdd_result_list = []
cdd_result_list = []
hdd_10C_result_list = []

day_max_temp_list = []
day_min_temp_list = []

#endregion

def evaluate_epw():
    k = 0
    l = 0
    m = 0
    y = np.zeros([max_length])
    hdd_y = np.zeros([max_length])
    cdd_y = np.zeros([max_length])
    hdd_10_y = np.zeros([max_length])
    for params in param_values:
        try:
            print("************ CURRENT ITERATION: " + str(int(m + 1)) + " / " + str(max_length) +  " EXCEPTIONS: " + str(l) + " ************")
                
            bld_height_list.append(float(params[0]))
            ver_to_hor_list.append(float(params[1]))
            bld_density_list.append(float(params[2]))
            urban_road_volumetric_heat_capacity_list.append(float(params[3]))
            road_albedo_list.append(float(params[4]))
            sensible_anthropogenic_heat_list.append(float(params[5]))
            urban_road_thermal_conductivity_list.append(float(params[6]))
            
            glazing_ratio_list.append(float(params[7]))
            wall_u_value_list.append(float(params[8]))
            window_u_value_list.append(float(params[9]))
            window_sghc_list.append(float(params[10]))
            infiltration_rate_list.append(float(params[11]))
            chiller_cop_list.append(float(params[12]))
            indoor_temp_set_point_list.append(float(params[13]))
            equipment_load_density_list.append(float(params[14]))
            lighting_load_density_list.append(float(params[15]))
            occupancy_density_list.append(float(params[16]))
            wall_albedo_list.append(float(params[17]))
            roof_albedo_list.append(float(params[18]))
            wall_emissivity_list.append(float(params[19]))
            roof_emissivity_list.append(float(params[20]))
            floor_height_list.append(float(params[21]))
            roof_u_value_list.append(float(params[22]))
            
            
            ventilation_rate_list = []

                
            custom_uwg(float(params[0]), float(params[1]), float(params[2]), float(params[3]), float(params[4]), 
                        float(params[5]), float(params[6]), float(params[7]), float(params[8]), float(params[9]),
                        float(params[10]), float(params[11]), float(params[12]), float(params[13]), float(params[14]),
                        float(params[15]), float(params[16]), float(params[17]), float(params[18]), float(params[19]),
                        float(params[20]), float(params[21]), float(params[22])
                                  
                        )
            pd_epw_sens, _ = pvlib.iotools.read_epw(
                    base_path + "data\\SIMULATION.epw")
                    
            indexes =  range(5473, 5642)
            
            day_1_indexes = range(5473, 5473 + 25)
            day_2_indexes = range(5473 + 24, 5473 + 49)
            day_3_indexes = range(5473 + 48, 5473 + 73)
            day_4_indexes = range(5473 + 72, 5473 + 97)
            day_5_indexes = range(5473 + 96, 5473 + 121)
            day_6_indexes = range(5473 + 120, 5473 + 145)
            day_7_indexes = range(5473 + 144, 5473 + 169)
            
            all_day_indexes = [day_1_indexes, day_2_indexes, day_3_indexes, day_4_indexes, day_5_indexes, day_6_indexes, day_7_indexes]
            
            temp_list = np.zeros([len(indexes)])
            hdd_list = np.zeros([len(indexes)])
            cdd_list = np.zeros([len(indexes)])
            hdd_10_list = np.zeros([len(indexes)])
                
            j = 0
            for i in indexes:
                hourly_temperature = pd_epw_sens['temp_air'].values[i]
                temp_list[j] = hourly_temperature
                    
                #toplanacak    -------------
                if hourly_temperature < 18.3:
                    hdd_list[j] = 18.3 - hourly_temperature
                else:
                    hdd_list[j] = 0
                    
                if hourly_temperature < 10:
                    hdd_10_list[j] = 10 - hourly_temperature
                else:
                    hdd_10_list[j] = 0
                        
                if hourly_temperature < 23.3:
                    cdd_list[j] = 0
                else:
                    cdd_list[j] = hourly_temperature - 23.3
                j+= 1
            
                
            temperature_max_list = []
            temperature_min_list = []
                
            n = 0
            o = 0
            for n in range(0,7):
                temporary_temperature_list = []
                
                for o in all_day_indexes[n]:
                    hourly_temperature = pd_epw_sens['temp_air'].values[o].astype(float).item()
                    temporary_temperature_list.append(hourly_temperature)
                    o += 1
                    
                daily_max_temperature = max(temporary_temperature_list)
                daily_min_temperature = min(temporary_temperature_list)
                
                temperature_max_list.append(daily_max_temperature)
                temperature_min_list.append(daily_min_temperature)
                
                n += 1
                o = 0
                
            print(temperature_max_list)
            print(temperature_min_list)
                    
            y[k] = np.average(temp_list)
            hdd_y[k] = np.sum(hdd_list)
            cdd_y[k] = np.sum(cdd_list)
            hdd_10_y[k] = np.sum(hdd_10_list)
                
            temp_result_list.append(np.average(temp_list))
            hdd_result_list.append(np.sum(hdd_list))
            cdd_result_list.append(np.sum(cdd_list))
            hdd_10C_result_list.append(np.sum(hdd_10_list))
            
            day_max_temp_list.append(average(temperature_max_list))
            day_min_temp_list.append(average(temperature_min_list))
                
            print(np.average(temp_list))
            k += 1
            m +=1
            
        except Exception as e:
            print("EXCEPTION OCCURED")
            print(e)
            y[k] = y[k-1]
            hdd_y[k] = hdd_y[k-1]
            cdd_y[k] = cdd_y[k-1]
            
            temp_result_list.append(nan)
            hdd_result_list.append(nan)
            cdd_result_list.append(nan)
            day_max_temp_list.append(nan)
            day_min_temp_list.append(nan)
            
            bld_height_list.append(float(params[0]))
            ver_to_hor_list.append(float(params[1]))
            bld_density_list.append(float(params[2]))
            urban_road_volumetric_heat_capacity_list.append(float(params[3]))
            road_albedo_list.append(float(params[4]))
            sensible_anthropogenic_heat_list.append(float(params[5]))
            urban_road_thermal_conductivity_list.append(float(params[6]))
            
            glazing_ratio_list.append(float(params[7]))
            wall_u_value_list.append(float(params[8]))
            window_u_value_list.append(float(params[9]))
            window_sghc_list.append(float(params[10]))
            infiltration_rate_list.append(float(params[11]))
            chiller_cop_list.append(float(params[12]))
            indoor_temp_set_point_list.append(float(params[13]))
            equipment_load_density_list.append(float(params[14]))
            lighting_load_density_list.append(float(params[15]))
            occupancy_density_list.append(float(params[16]))
            wall_albedo_list.append(float(params[17]))
            roof_albedo_list.append(float(params[18]))
            wall_emissivity_list.append(float(params[19]))
            roof_emissivity_list.append(float(params[20]))
            floor_height_list.append(float(params[21]))
            roof_u_value_list.append(float(params[22]))
            
            k += 1
            l += 1
            m +=1
            print("************ CURRENT ITERATION: " + str(int(m)) + " / " + str(max_length) +  " EXCEPTIONS: " + str(l) + " ************")
            print(str(float(params[0])), str(float(params[1])), str(float(params[2])), str(float(params[3])), str(float(params[4])),
                 str(float(params[5])), str(float(params[6])), str(float(params[7])), str(float(params[8])), str(float(params[9])),
                 str(float(params[10])), str(float(params[11])), str(float(params[12])), str(float(params[13])), str(float(params[14])),
                 str(float(params[15])), str(float(params[16])), str(float(params[17])), str(float(params[18])), str(float(params[19])),
                 str(float(params[20])), str(float(params[21])), str(float(params[22]))                                                                                                                  
                 )
            
                
    return y, hdd_y, cdd_y, hdd_10_y

Y, HDD_Y, CDD_Y, HDD_10_Y = evaluate_epw()

#Y = np.loadtxt(base_path + "txtexport\\izmir_morris.txt")

                        #"txtexport\\izmir_morris.txt"
                        #_izmir_morris_9-29
np.savetxt(base_path + "txtexport\\sobol-urban_characteristics-12-5-NUMPY.txt", Y)

Si_Temp = sobol.analyze(problem, Y)
Si_CDD = sobol.analyze(problem, CDD_Y)
Si_HDD = sobol.analyze(problem, HDD_Y)
Si_HDD10 = sobol.analyze(problem, HDD_10_Y)

print(str(Si_Temp), str(Si_CDD), str(Si_HDD), str(Si_HDD10))

lines = [str(Si_Temp), str(Si_CDD), str(Si_HDD), str(Si_HDD10)]
with open(base_path + 'txtexport\\sobol-urban_characteristics-12-5.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')
        f.write('------------')
        f.write('\n')
        
data = {    
            'bld_height': bld_height_list,
            'ver_to_hor' : ver_to_hor_list,
            'bld_density' : bld_density_list,
            'urban_road_volumetric_heat_capacity' : urban_road_volumetric_heat_capacity_list,
            'road_albedo' : road_albedo_list,
            'sensible_anthropogenic_heat': sensible_anthropogenic_heat_list,
            'urban_road_thermal_conductivity': urban_road_thermal_conductivity_list,
            
            'glazing_ratio': glazing_ratio_list,
            'wall_u_value' : wall_u_value_list,
            'window_u_value' : window_u_value_list,
            'window_sghc' : window_sghc_list,
            'infiltration_rate' : infiltration_rate_list,
            'chiller_cop' : chiller_cop_list,
            'indoor_temp_set_point': indoor_temp_set_point_list,
            'equipment_load_density': equipment_load_density_list,
            'lighting_load_density': lighting_load_density_list,
            'occupancy_density': occupancy_density_list,
            'wall_albedo': wall_albedo_list,
            'roof_albedo': roof_albedo_list,
            'wall_emissivity': wall_emissivity_list,
            'roof_emissivity': roof_emissivity_list,
            'floor_height': floor_height_list,
            'roof_u_value': roof_u_value_list,
            
            
            'temp_average': temp_result_list,
            'hdd_results': hdd_result_list,
            'hdd_10C_results': hdd_10C_result_list,
            'cdd_results': cdd_result_list,
            'daily_average_max_temperature': day_max_temp_list,
            'daily_average_min_temperature': day_min_temp_list
            } 
 
df = pd.DataFrame(data) 


df.to_csv(base_path + "csvexport\\sobol-urban_characteristics-12-5.csv")
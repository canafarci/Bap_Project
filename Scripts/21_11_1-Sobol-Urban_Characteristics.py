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

#region Custom UWG ---------------------------

def custom_uwg(bld_height, ver_to_hor, bld_density, urban_road_volumetric_heat_capacity, urban_area_length, road_albedo, 
              sensible_anthropogenic_heat, urban_road_thermal_conductivity, urban_road_thickness):
              
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
        
    if urban_area_length < 767:
        urban_area_length = 767
    elif urban_area_length > 1232:
        urban_area_length = 1232
        
    if road_albedo < 0.1217:
        road_albedo = 0.1217
    elif road_albedo > 0.2334:
        road_albedo = 0.2334
        
    if sensible_anthropogenic_heat < 4.2:
        sensible_anthropogenic_heat = 4.2
    elif sensible_anthropogenic_heat > 9.79:
        sensible_anthropogenic_heat = 9.79
        
    if urban_road_thermal_conductivity < 1.02:
        urban_road_thermal_conductivity = 1.02
    elif urban_road_thermal_conductivity > 2.885:
        urban_road_thermal_conductivity = 2.885
        
    if urban_road_thickness < 0.2098:
        urban_road_thickness = 0.2098
    elif urban_road_thickness > 0.4505:
        urban_road_thickness = 0.4505
        
    
        
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
    
    cool_week = [[25] * 24] * 3
    
    heat_week = [[23] * 24] * 3
    
    
    schdef1 = SchDef(elec=elec_week, gas=default_week, light=light_week,
                     occ=occ_week, cool=cool_week, heat=heat_week,
                     q_elec=7.5, q_gas=3.2, q_light=7.5,
                     n_occ=(0.26), vent=0.001 * 0.2, bldtype='midriseapartment',
                     builtera='pre80')
    
    ###-----------------------------------------------------------------------------------------



    # MATERIAL PARAMETERS ------------------------------------------------------------------------------------------------
    
    mineral_plaster = Material(0.54, 1300 * 900, 'mineral_plaster')
    
    
    cement_plaster = Material(0.721, 1762 * 840, 'cement_plaster') # 1.1116299705    - 0.21 --- 0.132045 ||| 0.5 ---0.561214
    eps = Material(0.035, 22 * 1400, 'eps')
    brick_wall = Material(0.33, 900 * 600, 'brick_wall') 
    gypsum_plaster = Material(0.51, 1200 * 840, 'gypsum_plaster')
    glasswool = Material(0.04, 18 * 670, 'glasswool')
    reinforced_concrete = Material(2.5, 840 * 2400, 'reinforced_concrete')


    
    
    # ELEMENT PARAMETERS ---------------------------------------------------------------------------
    
    wall = Element(0.5, 0.4527, [0.002, 0.03, 5, 0.135, 0.02],  [mineral_plaster, cement_plaster, eps, brick_wall, gypsum_plaster], 0, 296, False, 'common_brick_wall_with_plaster')
    roof = Element(0.5, 0.4527, [20, 0.12, 0.02], [glasswool, reinforced_concrete, gypsum_plaster], 0, 296, True, 'tile')
    mass = Element(0.20, 0.90, [0.15, 0.15], [reinforced_concrete, reinforced_concrete], 0, 296, True, 'concrete_floor')

    ### ---------------------------------------------------------------------------------------------



    # BUILDING PARAMETERS -----------------------------------------------------------------------------------------------

    bldg = Building(
        floor_height=3, int_heat_night=1, int_heat_day=1, int_heat_frad=1,
        int_heat_flat=1, infil=0.65, vent=0.98, glazing_ratio=0.235, u_value=1.95,
        shgc=0.59, condtype='AIR', cop=4.45, coolcap=900, heateff=0.8, initial_temp=300)

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
        charlength=urban_area_length,  albveg=0.3, vegend=10, vegstart=3, droad=urban_road_thickness, kroad=urban_road_thermal_conductivity,
        croad=urban_road_volumetric_heat_capacity
        )
    
    ###---------------------------------------------------------------------------------------------------------------
   
    
    model.generate()
    model.simulate()
    
    model.write_epw()
    
#endregion

#region Parameter Definition ------------------------------
problem = {
    'num_vars': 9,
    'names': ['bld_height', 'ver_to_hor', 'bld_density', 'urban_road_volumetric_heat_capacity', 'urban_area_length', 'road_albedo', #6
              'sensible_anthropogenic_heat', 'urban_road_thermal_conductivity', 'urban_road_thickness'],  #2
              
    'bounds': [[2.5, 0.7],       #bld_height
               [0.62, 0.5],       #ver_to_hor
               [0.45, 0.105],    #bld_density
               [1960371, 300000],     #urban_road_volumetric_heat_capacity
               [1000, 100],       #urban_area_length
               [0.1776, 0.024],      #road_albedo
               
               [7, 1.2],    #sensible_anthropogenic_heat
               [1.955, 0.4],    #urban_road_thermal_conductivity
               [0.3302, 0.0517]    #urban_road_thickness
            
               ],
    
    'dists':['lognorm', 'lognorm','norm', 'norm', 'norm', 'norm', 'norm', 'norm', 'norm'
              ]  
}

#endregion

# sample        
param_values = saltelli.sample(problem, 1400) #1400

#region CSV index lists definition -------------------------
max_length = len(param_values)

bld_height_list = []
ver_to_hor_list = []
bld_density_list = []
urban_road_volumetric_heat_capacity_list = []
urban_area_length_list = []
road_albedo_list = []
sensible_anthropogenic_heat_list = []
urban_road_thermal_conductivity_list = []
urban_road_thickness_list = []

temp_result_list = []
hdd_result_list = []
cdd_result_list = []
day_max_temp_list = []
day_min_temp_list = []


exception_list = []
#endregion

# evaluate
def evaluate_epw():
    k = 0
    l = 0
    m = 0
    y = np.zeros([max_length])
    hdd_y = np.zeros([max_length])
    cdd_y = np.zeros([max_length])
    for params in param_values:
        try:
            print("************ CURRENT ITERATION: " + str(int(m + 1)) + " / " + str(max_length) +  " EXCEPTIONS: " + str(l) + " ************")
                
            bld_height_list.append(float(params[0]))
            ver_to_hor_list.append(float(params[1]))
            bld_density_list.append(float(params[2]))
            urban_road_volumetric_heat_capacity_list.append(float(params[3]))
            urban_area_length_list.append(float(params[4]))
            road_albedo_list.append(float(params[5]))
            sensible_anthropogenic_heat_list.append(float(params[6]))
            urban_road_thermal_conductivity_list.append(float(params[7]))
            urban_road_thickness_list.append(float(params[8]))
                
            custom_uwg(float(params[0]), float(params[1]), float(params[2]), float(params[3]), float(params[4]), 
                        float(params[5]), float(params[6]), float(params[7]), float(params[8])                
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
                
            j = 0
            for i in indexes:
                hourly_temperature = pd_epw_sens['temp_air'].values[i]
                temp_list[j] = hourly_temperature
                    
                #toplanacak    -------------
                if hourly_temperature < 18.3:
                    hdd_list[j] = 18.3 - hourly_temperature
                #elif hourly_temperature >= 18.3:
                #    hdd_list[j] = 0
                else:
                    hdd_list[j] = 0
                        
                if hourly_temperature < 23.3:
                    cdd_list[j] = 0
                #elif hourly_temperature >= 23.3:
                    #cdd_list[j] = hourly_temperature - 23.3
                else:
                    cdd_list[j] = hourly_temperature - 23.3
                    
                #hdd base - 10, hdd list 18.3
                    
                #toplanacak  ----------------
                #add daily max and min temp -- averageını al -- daily max average daily min average
                #typical summer week 8-17
                #extreme 13-7
                #5A ashrae climate zone
                #koppen DFB
                
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
            hdd_y[k] = np.average(hdd_list)
            cdd_y[k] = np.average(cdd_list)
                
            temp_result_list.append(np.average(temp_list))
            hdd_result_list.append(np.sum(hdd_list))
            cdd_result_list.append(np.sum(cdd_list))
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
            urban_area_length_list.append(float(params[4]))
            road_albedo_list.append(float(params[5]))
            sensible_anthropogenic_heat_list.append(float(params[6]))
            urban_road_thermal_conductivity_list.append(float(params[7]))
            urban_road_thickness_list.append(float(params[8]))
            
            k += 1
            l += 1
            m +=1
            print("************ CURRENT ITERATION: " + str(int(m)) + " / " + str(max_length) +  " EXCEPTIONS: " + str(l) + " ************")
            print(str(float(params[0])), str(float(params[1])), str(float(params[2])), str(float(params[3])), str(float(params[4])),
                 str(float(params[5])), str(float(params[6])), str(float(params[7])), str(float(params[8]))
            )
            
                
    return y, hdd_y, cdd_y
            

Y, HDD_Y, CDD_Y = evaluate_epw()

#Y = np.loadtxt(base_path + "txtexport\\izmir_morris.txt")

                        #"txtexport\\izmir_morris.txt"
                        #_izmir_morris_9-29
np.savetxt(base_path + "txtexport\\sobol-urban_characteristics-11-4-NUMPY.txt", Y)

# analyse
Si_Temp = sobol.analyze(problem, Y)
Si_CDD = sobol.analyze(problem, CDD_Y)
Si_HDD = sobol.analyze(problem, HDD_Y)

print(str(Si_Temp), str(Si_CDD), str(Si_HDD))

lines = [str(Si_Temp), str(Si_CDD), str(Si_HDD)]
with open(base_path + 'txtexport\\sobol-urban_characteristics-11-4', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')
        f.write('------------')
        f.write('\n')

              
data = {    'bld_height': bld_height_list,
            'ver_to_hor' : ver_to_hor_list,
            'bld_density' : bld_density_list,
            'urban_road_volumetric_heat_capacity' : urban_road_volumetric_heat_capacity_list,
            'urban_area_length' : urban_area_length_list,
            'road_albedo' : road_albedo_list,
            'sensible_anthropogenic_heat': sensible_anthropogenic_heat_list,
            'urban_road_thermal_conductivity': urban_road_thermal_conductivity_list,
            'urban_road_thickness': urban_road_thickness_list,
            
            
            'temp_average': temp_result_list,
            'hdd_results': hdd_result_list,
            'cdd_results': cdd_result_list,
            'daily_average_max_temperature': day_max_temp_list,
            'daily_average_min_temperature': day_min_temp_list
            } 
 
df = pd.DataFrame(data) 


df.to_csv(base_path + "csvexport\\sobol-urban_characteristics-11-4.csv")




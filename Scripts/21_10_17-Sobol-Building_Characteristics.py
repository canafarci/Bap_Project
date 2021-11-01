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

def custom_uwg(glazing_ratio, wall_u_value, window_u_value, window_sghc, infiltration_rate, 
               chiller_cop, indoor_temp_set_point, equipment_load_density, lighting_load_density, occupancy_density,
               wall_albedo, roof_albedo, wall_emissivity, roof_emissivity, floor_height,
               ventilation_rate, roof_u_value):
              
    """Generate UWG json with custom reference BEMDef and SchDef objects."""
    
    global epw_name_index

#region ERROR CHECKS  ------------------------------------------------------------------------------------------------------------

    if roof_u_value < 1:
        roof_u_value = 1
    elif roof_u_value >148:
        roof_u_value = 148
        
    if wall_u_value < 1:
        wall_u_value = 1
    elif wall_u_value > 64:
        wall_u_value = 64
    
    if glazing_ratio < 0.0628:
        glazing_ratio= 0.0628
    elif glazing_ratio > 0.4071:
        glazing_ratio = 0.4071
        
    if window_u_value < 1.16:
        window_u_value = 1.16
    elif window_u_value > 3.29:
        window_u_value = 3.29
        
    if window_sghc < 0.4038:
        window_sghc = 0.4038
    elif window_sghc > 0.7761:
        window_sghc = 0.7761
        
    if infiltration_rate < 0.1:
        infiltration_rate = 4.18
    elif infiltration_rate > 4.18:
        infiltration_rate = 4.18
        
    if chiller_cop < 2.4726:
        chiller_cop = 2.4726
    elif chiller_cop > 6.4274:
        chiller_cop = 6.4274
        
    if indoor_temp_set_point < 24.7:
        indoor_temp_set_point = 24.7
    elif indoor_temp_set_point > 29.3:
        indoor_temp_set_point = 29.3
        
    if equipment_load_density < 2.38:
        equipment_load_density = 2.38
    elif equipment_load_density > 15.34:
        equipment_load_density = 15.34
        
    if lighting_load_density < 3.32:
        lighting_load_density = 3.32
    elif lighting_load_density > 13.43:
        lighting_load_density = 13.43
        
    if occupancy_density < 0.02:
        occupancy_density = 0.02
    elif occupancy_density > 0.49:
        occupancy_density = 0.49
        
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
        
    if floor_height < 2.6:
        floor_height = 2.6
    elif floor_height > 3.5:
        floor_height = 3.5
        
    if ventilation_rate < 0.58:
        ventilation_rate = 0.58
    elif ventilation_rate > 1.64:
        ventilation_rate = 1.64  
        
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
    reinforced_concrete = Material(2.5, 840 * 2400, 'reinforced_concrete')


    
    
    # ELEMENT PARAMETERS ---------------------------------------------------------------------------
    
    wall = Element(wall_albedo, wall_emissivity, [0.002, 0.03, wall_u_value, 0.135, 0.02],  [mineral_plaster, cement_plaster, eps, brick_wall, gypsum_plaster], 0, 296, False, 'common_brick_wall_with_plaster')
    roof = Element(roof_albedo, roof_emissivity, [roof_u_value, 0.12, 0.02], [glasswool, reinforced_concrete, gypsum_plaster], 0, 296, True, 'tile')
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

    epw_path = base_path + "data\\TUR_Ankara.171280_IWEC.epw"
    
    ###-------------------------------------------------------------------------------------------


    
    # UWG PARAMETERS ------------------------------------------------------------------------------------------------
    
    model = UWG.from_param_args(
        epw_path=epw_path, bldheight=12, blddensity=0.27, vertohor=0.7, zone='4B',
        treecover=0, grasscover=0, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector, month=8, day=17, sensanth=2, nday=7, dtsim=200, albroad=0.20,
        new_epw_name="SIMULATION.epw",
        charlength=500,  albveg=0.3, vegend=10, vegstart=3, droad=1.25, kroad=0.8
        )
    
    ###---------------------------------------------------------------------------------------------------------------
    print(glazing_ratio, wall_u_value, window_u_value, window_sghc, infiltration_rate, 
               chiller_cop, indoor_temp_set_point, equipment_load_density, lighting_load_density, occupancy_density,
               wall_albedo, roof_albedo, wall_emissivity, roof_emissivity, floor_height,
               ventilation_rate, roof_u_value
               )
    
    model.generate()
    model.simulate()
    
    model.write_epw()
    
#endregion

#region Parameter Definition ------------------------------
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

#endregion

# sample        
param_values = saltelli.sample(problem, 2653) #2653

#region CSV index lists definition -------------------------
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
wall_albedo_list = []
roof_albedo_list = []
wall_emissivity_list = []
roof_emissivity_list = []
floor_height_list = []
ventilation_rate_list = []
roof_u_value_list = []
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
            wall_albedo_list.append(float(params[10]))
            roof_albedo_list.append(float(params[11]))
            wall_emissivity_list.append(float(params[12]))
            roof_emissivity_list.append(float(params[13]))
            floor_height_list.append(float(params[14]))
            ventilation_rate_list.append(float(params[15]))
            roof_u_value_list.append(float(params[16]))
                
            custom_uwg(float(params[0]), float(params[1]), float(params[2]), float(params[3]), float(params[4]), 
                        float(params[5]), float(params[6]), float(params[7]), float(params[8]), float(params[9]), 
                        float(params[10]), float(params[11]), float(params[12]), float(params[13]), float(params[14]),
                        float(params[15]), float(params[16])                     
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
                if hourly_temperature > 18.3:
                    hdd_list[j] = hourly_temperature - 18.3
                elif hourly_temperature <= 18.3:
                    hdd_list[j] = 0
                        
                if hourly_temperature > 23.3:
                    cdd_list[j] = 0
                elif hourly_temperature <= 23.3:
                    cdd_list[j] = 23.3 - hourly_temperature
                    
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
            k += 1
            l += 1
            m +=1
            print("************ CURRENT ITERATION: " + str(int(m)) + " / " + str(max_length) +  " EXCEPTIONS: " + str(l) + " ************")
            print(str(float(params[0])), str(float(params[1])), str(float(params[2])), str(float(params[3])), str(float(params[4])),
                 str(float(params[5])), str(float(params[6])), str(float(params[7])), str(float(params[8])), str(float(params[9])),
                  str(float(params[10])), str(float(params[11])), str(float(params[12])), str(float(params[13])), str(float(params[14])),
                  str(float(params[15])), str(float(params[16]))
                  )
            
                
    return y, hdd_y, cdd_y
            

Y, HDD_Y, CDD_Y = evaluate_epw()

#Y = np.loadtxt(base_path + "txtexport\\izmir_morris.txt")

                        #"txtexport\\izmir_morris.txt"
                        #_izmir_morris_9-29
np.savetxt(base_path + "txtexport\\sobol-building_characteristics-27-10-NUMPY.txt", Y)

# analyse
Si_Temp = sobol.analyze(problem, Y)
Si_CDD = sobol.analyze(problem, CDD_Y)
Si_HDD = sobol.analyze(problem, HDD_Y)

print(str(Si_Temp), str(Si_CDD), str(Si_HDD))

data = {    'glazing_ratio': glazing_ratio_list,
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
            'ventilation_rate': ventilation_rate_list,
            'roof_u_value': roof_u_value_list,
            'temp_average': temp_result_list,
            'hdd_results': hdd_result_list,
            'cdd_results': cdd_result_list,
            'daily_average_max_temperature': day_max_temp_list,
            'daily_average_min_temperature': day_min_temp_list
            } 
 
df = pd.DataFrame(data) 


df.to_csv(base_path + "csvexport\\sobol-building_characteristics-27-10.csv")


lines = [str(Si_Temp), str(Si_CDD), str(Si_HDD)]
with open(base_path + 'txtexport\\sobol-building_characteristics-27-10.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')
        f.write('------------')
        f.write('\n')

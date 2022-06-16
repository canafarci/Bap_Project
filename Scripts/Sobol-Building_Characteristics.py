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

# region Custom UWG ---------------------------


def custom_uwg(glazing_ratio, wall_u_value, window_u_value, window_sghc, infiltration_rate,
               chiller_cop, indoor_temp_set_point, equipment_load_density, lighting_load_density, occupancy_density,
               wall_albedo, roof_albedo, wall_emissivity, roof_emissivity, floor_height,
               roof_u_value):
    """Generate UWG json with custom reference BEMDef and SchDef objects."""

    global epw_name_index

# region ERROR CHECKS  ------------------------------------------------------------------------------------------------------------

    if roof_u_value < 0.157:
        roof_u_value = 0.157
    elif roof_u_value > 1.362:
        roof_u_value = 1.362

    if wall_u_value < 0.221:
        wall_u_value = 0.221
    elif wall_u_value > 1.524:
        wall_u_value = 1.524

    if glazing_ratio < 0.129:
        glazing_ratio = 0.129
    elif glazing_ratio > 0.414:
        glazing_ratio = 0.414

    if window_u_value < 1.69:
        window_u_value = 1.69
    elif window_u_value > 4.059:
        window_u_value = 4.059

    if window_sghc < 0.42:
        window_sghc = 0.42
    elif window_sghc > 0.83:
        window_sghc = 0.83

    if infiltration_rate < 0.286:
        infiltration_rate = 0.286
    elif infiltration_rate > 1.263:
        infiltration_rate = 1.263

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

    if wall_albedo < 0.318:
        wall_albedo = 0.318
    elif wall_albedo > 0.528:
        wall_albedo = 0.528

    if roof_albedo < 0.318:
        roof_albedo = 0.318
    elif roof_albedo > 0.528:
        roof_albedo = 0.528

    if wall_emissivity < 0.791:
        wall_emissivity = 0.791
    elif wall_emissivity > 0.908:
        wall_emissivity = 0.908

    if roof_emissivity < 0.791:
        roof_emissivity = 0.791
    elif roof_emissivity > 0.908:
        roof_emissivity = 0.908

    if floor_height < 2.62:
        floor_height = 2.62
    elif floor_height > 3.17:
        floor_height = 3.17

    glazing_ratio_list.append(glazing_ratio)
    wall_u_value_list.append(wall_u_value)
    window_u_value_list.append(window_u_value)
    window_sghc_list.append(window_sghc)
    infiltration_rate_list.append(infiltration_rate)
    chiller_cop_list.append(chiller_cop)
    indoor_temp_set_point_list.append(indoor_temp_set_point)
    equipment_load_density_list.append(equipment_load_density)
    lighting_load_density_list.append(lighting_load_density)
    occupancy_density_list.append(occupancy_density)
    wall_albedo_list.append(wall_albedo)
    roof_albedo_list.append(roof_albedo)
    wall_emissivity_list.append(wall_emissivity)
    roof_emissivity_list.append(roof_emissivity)
    floor_height_list.append(floor_height)
    roof_u_value_list.append(roof_u_value)


# endregion

    # SchDef PARAMETERS -----------------------------------------------------------------------

    default_week = [[0.15] * 24] * 3
    occ_week = [1,	1,	1,	1,	1, 1,	1,	0.85,	0.39,	0.25,	0.25,	0.25,
                0.25,	0.25,	0.25,	0.25,	0.3,	0.52,	0.87,	0.87,	0.87,	1,	1,	1] * 3

    elec_week = [[0.45, 0.41, 0.39, 0.38, 0.38, 0.43, 0.54, 0.65, 0.66, 0.67, 0.69, 0.7, 0.69, 0.66, 0.65, 0.68, 0.8, 1, 1, 0.93, 0.89, 0.85, 0.71, 0.58],
                 [0.45, 0.41, 0.39, 0.38, 0.38, 0.43, 0.54, 0.65, 0.66, 0.67, 0.69, 0.7,
                     0.69, 0.66, 0.65, 0.68, 0.8, 1, 1, 0.93, 0.89, 0.85, 0.71, 0.58],
                 [0.45, 0.41, 0.39, 0.38, 0.38, 0.43, 0.54, 0.65, 0.66, 0.67, 0.69, 0.7, 0.69, 0.66, 0.65, 0.68, 0.8, 1, 1, 0.93, 0.89, 0.85, 0.71, 0.58]]

    light_week = [[0.067, 0.067, 0.067, 0.067, 0.187, 0.394, 0.44, 0.393, 0.172, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.206, 0.439, 0.616, 0.829, 0.986, 1, 0.692, 0.384, 0.16],
                  [0.067, 0.067, 0.067, 0.067, 0.187, 0.394, 0.44, 0.393, 0.172, 0.119, 0.119, 0.119,
                      0.119, 0.119, 0.119, 0.206, 0.439, 0.616, 0.829, 0.986, 1, 0.692, 0.384, 0.16],
                  [0.067, 0.067, 0.067, 0.067, 0.187, 0.394, 0.44, 0.393, 0.172, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.206, 0.439, 0.616, 0.829, 0.986, 1, 0.692, 0.384, 0.16]]

    cool_week = [[indoor_temp_set_point] * 24] * 3

    heat_week = [[23] * 24] * 3

    schdef1 = SchDef(elec=elec_week, gas=default_week, light=light_week,
                     occ=occ_week, cool=cool_week, heat=heat_week,
                     q_elec=equipment_load_density, q_gas=3.2, q_light=lighting_load_density,
                     n_occ=(occupancy_density), vent=0.001 * 0.2, bldtype='midriseapartment',
                     builtera='pre80')

    # -----------------------------------------------------------------------------------------

    # MATERIAL PARAMETERS ------------------------------------------------------------------------------------------------
    brick = Material(0.33, 585000, 'brick')
    xps = Material(0.035,  30000, "XPS")
    plaster = Material(0.51,  1308000, "plaster")

    mineral_wool = Material(0.04, 16600, "mineral_wool")
    concrete_slab = Material(2.5, 2016000, 'concrete_slab')

    Rsi = 0.13
    Rse = 0.04
    Rsi_roof = 0.13
    Rse_roof = 0.08
    mineral_wool_lambda = 0.04
    concrete_slab_lambda = 2.5
    xps_lambda = 0.035
    brick_lambda = 0.33
    plaster_lambda = 0.51

    mineral_wool_thickness = ((1 / roof_u_value) - (0.2 / concrete_slab_lambda) - (
        0.025 / plaster_lambda) - (Rsi_roof + Rse_roof)) * mineral_wool_lambda

    xps_thickness = ((1 / wall_u_value) - (0.135 / brick_lambda) -
                     (0.025 / plaster_lambda) - (Rsi + Rse)) * xps_lambda

    print("XPS  " + str(xps_thickness))
    print("WOOL  " + str(mineral_wool_thickness))
    # ELEMENT PARAMETERS -----------------------------------------------------------------------------------------------

    wall = Element(wall_albedo, wall_emissivity, [0.025, xps_thickness, 0.135],  [
                   plaster, xps, brick], 0, 296, False, 'common_brick_wall_with_xps')
    roof = Element(roof_albedo, roof_emissivity, [0.025, mineral_wool_thickness, 0.2], [
                   plaster, mineral_wool, concrete_slab], 0, 296, True, 'roof_concrete_slab_with_mineral_wool')
    mass = Element(0.20, 0.90, [0.05, 0.4], [
                   plaster, concrete_slab], 0, 296, True, 'concrete_floor')

    # ----------------------------------------------------------------------------------------------------------------

    # BUILDING PARAMETERS -----------------------------------------------------------------------------------------------

    bldg = Building(
        floor_height=floor_height, int_heat_night=1, int_heat_day=1, int_heat_frad=1,
        int_heat_flat=1, infil=infiltration_rate, vent=(0.001 * 0.2), glazing_ratio=glazing_ratio, u_value=window_u_value,
        shgc=window_sghc, condtype='AIR', cop=chiller_cop, coolcap=900, heateff=0.8, initial_temp=300)

    bemdef1 = BEMDef(building=bldg, mass=mass, wall=wall,
                     roof=roof, bldtype='midriseapartment', builtera='pre80')

    # ------------------------------------------------------------------------------------------------------------------

    # VECTOR---------------------------------------------------------------------------------------

    ref_sch_vector = [schdef1]
    ref_bem_vector = [bemdef1]

    bld = [('midriseapartment', 'pre80', 1)  # overwrite
           ]  # extend

    epw_path = base_path + "data\\TUR_Ankara.171280_IWEC.epw"

    # -------------------------------------------------------------------------------------------

    # UWG PARAMETERS ------------------------------------------------------------------------------------------------

    model = UWG.from_param_args(
        epw_path=epw_path, bldheight=13.385, blddensity=0.385, vertohor=1.302, zone='4B',
        treecover=0, grasscover=0, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector, month=8, day=17,  nday=7, dtsim=180,
        new_epw_name="SIMULATION1.epw",
        charlength=1000, vegend=10, vegstart=3, droad=1.25, croad=1960371, albroad=0.233, sensanth=20, kroad=1.955,
        c_exch=0.5, h_mix=0.5, h_ubl1=750, h_ubl2=75, c_circ=1, maxday=200, maxnight=50
    )

    # ---------------------------------------------------------------------------------------------------------------
    print(glazing_ratio, wall_u_value, window_u_value, window_sghc, infiltration_rate,
          chiller_cop, indoor_temp_set_point, equipment_load_density, lighting_load_density, occupancy_density,
          wall_albedo, roof_albedo, wall_emissivity, roof_emissivity, floor_height,
          roof_u_value
          )

    model.generate()
    model.simulate()

    model.write_epw()

# endregion


# region Parameter Definition ------------------------------
problem = {
    'num_vars': 16,
    'names': ['glazing_ratio', 'wall_u_value', 'window_u_value', 'window_sghc', 'infiltration_rate', 'chiller_cop',  # 6
              'indoor_temp_set_point', 'equipment_load_density', 'lighting_load_density', 'occupancy_density',  # 4
              'wall_albedo', 'roof_albedo', 'wall_emissivity', 'roof_emissivity',  # 5
              'floor_height', 'roof_u_value'],  # 2

    'bounds': [[-1.462, 0.250],  # glazing_ratio
               [-0.542, 0.414],  # wall_u_value
               [0.965, 0.187],  # window_u_value
               [-0.519, 0.143],  # window_sghc
               [0.775, 0.21],  # infiltration_rate
               [4.45, 0.85],  # chiller_cop

               [20, 24],  # indoor_temp_set_point
               [4.6, 0.48],  # equipment_load_density
               [4.4, 0.42],  # lighting_load_density
               [0.02665, 0.00443],  # occupancy_density ---- 10


               [0.4235, 0.045],  # wall_albedo ----- 20
               [0.4235, 0.045],  # roof_albedo
               [0.85, 0.025],  # wall_emissivity
               [0.85, 0.025],  # roof_emissivity

               [1.059, 0.041],  # floor_height
               [-0.771, 0.464]  # roof_u_value
               ],

    'dists': ['lognorm', 'lognorm', 'lognorm', 'lognorm', 'norm', 'norm',
              'unif', 'norm', 'norm', 'norm',
              'norm', 'norm', 'norm', 'norm',
              'lognorm', 'lognorm']



}

# endregion

# sample
param_values = saltelli.sample(problem, 1024)  # 2300

# region CSV index lists definition -------------------------
max_length = len(param_values)


temp_result_list = []
hdd_result_list = []
hdd_10C_result_list = []
cdd_result_list = []
day_max_temp_list = []
day_min_temp_list = []


exception_list = []
# endregion

# evaluate


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
            print("************ CURRENT ITERATION: " + str(int(m + 1)) + " / " +
                  str(max_length) + " EXCEPTIONS: " + str(l) + " ************")

            custom_uwg(float(params[0]), float(params[1]), float(params[2]), float(params[3]), float(params[4]),
                       float(params[5]), float(params[6]), float(
                           params[7]), float(params[8]), float(params[9]),
                       float(params[10]), float(params[11]), float(
                           params[12]), float(params[13]), float(params[14]),
                       float(params[15])
                       )
            pd_epw_sens, _ = pvlib.iotools.read_epw(
                base_path + "data\\SIMULATION1.epw")

            indexes = range(5473, 5473 + (7 * 24))

            day_1_indexes = range(5473, 5473 + 24)
            day_2_indexes = range(5473 + 24, 5473 + 48)
            day_3_indexes = range(5473 + 48, 5473 + 72)
            day_4_indexes = range(5473 + 72, 5473 + 96)
            day_5_indexes = range(5473 + 96, 5473 + 120)
            day_6_indexes = range(5473 + 120, 5473 + 144)
            day_7_indexes = range(5473 + 144, 5473 + 168)

            all_day_indexes = [day_1_indexes, day_2_indexes, day_3_indexes,
                               day_4_indexes, day_5_indexes, day_6_indexes, day_7_indexes]

            temp_list = np.zeros([len(indexes)])
            hdd_list = np.zeros([len(indexes)])
            cdd_list = np.zeros([len(indexes)])
            hdd_10_list = np.zeros([len(indexes)])

            j = 0
            for i in indexes:
                hourly_temperature = pd_epw_sens['temp_air'].values[i]
                temp_list[j] = hourly_temperature

                # toplanacak    -------------
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

                # toplanacak  ----------------
                # add daily max and min temp -- averageını al -- daily max average daily min average
                # typical summer week 8-17
                # extreme 13-7
                # 5A ashrae climate zone
                # koppen DFB

                j += 1

            temperature_max_list = []
            temperature_min_list = []

            n = 0
            o = 0
            for n in range(0, 7):
                temporary_temperature_list = []

                for o in all_day_indexes[n]:
                    hourly_temperature = pd_epw_sens['temp_air'].values[o].astype(
                        float).item()
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
            hdd_10_y[k] = np.sum(hdd_10_list)

            temp_result_list.append(np.average(temp_list))
            hdd_result_list.append(np.sum(hdd_list))
            cdd_result_list.append(np.sum(cdd_list))
            hdd_10C_result_list.append(np.sum(hdd_10_list))

            day_max_temp_list.append(average(temperature_max_list))
            day_min_temp_list.append(average(temperature_min_list))

            print(np.average(temp_list))
            k += 1
            m += 1

        except Exception as e:
            print("EXCEPTION OCCURED")
            print(e)
            y[k] = y[k-1]
            k += 1
            l += 1
            m += 1
            print("************ CURRENT ITERATION: " + str(int(m)) + " / " +
                  str(max_length) + " EXCEPTIONS: " + str(l) + " ************")
            print(str(float(params[0])), str(float(params[1])), str(float(params[2])), str(float(params[3])), str(float(params[4])),
                  str(float(params[5])), str(float(params[6])), str(
                      float(params[7])), str(float(params[8])), str(float(params[9])),
                  str(float(params[10])), str(float(params[11])), str(
                      float(params[12])), str(float(params[13])), str(float(params[14])),
                  str(float(params[15]))
                  )

    return y, hdd_y, cdd_y, hdd_10_y


Y, HDD_Y, CDD_Y, HDD_10_Y = evaluate_epw()
# analyse
Si_Temp = sobol.analyze(problem, Y)
Si_CDD = sobol.analyze(problem, CDD_Y)
Si_HDD = sobol.analyze(problem, HDD_Y)
Si_HDD10 = sobol.analyze(problem, HDD_10_Y)

print(str(Si_Temp), str(Si_CDD), str(Si_HDD))

lines = [str(Si_Temp), str(Si_CDD), str(Si_HDD)]
with open(base_path + 'txtexport\\sobol-weekly-4-15-bc-s.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')
        f.write('------------')
        f.write('\n')


data = {'glazing_ratio': glazing_ratio_list,
        'wall_u_value': wall_u_value_list,
        'window_u_value': window_u_value_list,
        'window_sghc': window_sghc_list,
        'infiltration_rate': infiltration_rate_list,
        'chiller_cop': chiller_cop_list,
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


df.to_csv(base_path + "csvexport\\sobol-weekly-4-15-bc-s.csv")

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
import os

base_path = os.getcwd()
base_path = "E:\\ARCHIVE\\BAP\\__Project\\"

folder_path = "data/TUR_Ankara.171280_IWEC.epw"
intermediate_epw_path = "data/simulation1h.epw"
epw_path = os.path.join(base_path, folder_path)

bld_height_list = []
ver_to_hor_list = []
bld_density_list = []
urban_road_volumetric_heat_capacity_list = []
road_albedo_list = []
sensible_anthropogenic_heat_list = []
urban_road_thermal_conductivity_list = []


def custom_uwg(bld_height, ver_to_hor, bld_density, urban_road_volumetric_heat_capacity, road_albedo,
               sensible_anthropogenic_heat, urban_road_thermal_conductivity):
    """Generate UWG json with custom reference BEMDef and SchDef objects."""

    global epw_name_index

# region ERROR CHECKS  ------------------------------------------------------------------------------------------------------------
    if bld_height < 6.7:
        bld_height = 6.7
    elif bld_height > 34.114:
        bld_height = 34.114

    if ver_to_hor < 0.521045:
        ver_to_hor = 0.521045
    elif ver_to_hor > 2.074:
        ver_to_hor = 2.074

    if bld_density < 0.308:
        bld_density = 0.308
    elif bld_density > 0.462:
        bld_density = 0.462

    if urban_road_volumetric_heat_capacity < 1264700:
        urban_road_volumetric_heat_capacity = 1264700
    elif urban_road_volumetric_heat_capacity > 2658280:
        urban_road_volumetric_heat_capacity = 2658280

    if road_albedo < 0.1217:
        road_albedo = 0.1217
    elif road_albedo > 0.345:
        road_albedo = 0.345

    if sensible_anthropogenic_heat < 8.36:
        sensible_anthropogenic_heat = 8.36
    elif sensible_anthropogenic_heat > 31.63:
        sensible_anthropogenic_heat = 31.63

    if urban_road_thermal_conductivity < 1.02:
        urban_road_thermal_conductivity = 1.02
    elif urban_road_thermal_conductivity > 2.885:
        urban_road_thermal_conductivity = 2.885

    bld_height_list.append(bld_height)
    ver_to_hor_list.append(ver_to_hor)
    bld_density_list.append(bld_height)
    urban_road_volumetric_heat_capacity_list.append(
        urban_road_volumetric_heat_capacity)
    road_albedo_list.append(road_albedo)
    sensible_anthropogenic_heat_list.append(sensible_anthropogenic_heat)
    urban_road_thermal_conductivity_list.append(
        urban_road_thermal_conductivity)


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

    cool_week = [[22] * 24] * 3

    heat_week = [[22] * 24] * 3

    schdef1 = SchDef(elec=elec_week, gas=default_week, light=light_week,
                     occ=occ_week, cool=cool_week, heat=heat_week,
                     q_elec=4.6, q_gas=3.2, q_light=4.4,
                     n_occ=(0.026665), vent=0.001 * 0.2, bldtype='midriseapartment',
                     builtera='pre80')

    # -----------------------------------------------------------------------------------------

    # MATERIAL PARAMETERS ------------------------------------------------------------------------------------------------
    brick = Material(0.33, 585000, 'brick')
    xps = Material(0.035,  30000, "XPS")
    plaster = Material(0.51,  1308000, "plaster")

    mineral_wool = Material(0.04, 16600, "mineral_wool")
    concrete_slab = Material(2.5, 2016000, 'concrete_slab')

    # ELEMENT PARAMETERS -----------------------------------------------------------------------------------------------

    wall = Element(0.5, 0.475, [0.025, 0.04959, 0.135],  [
                   plaster, xps, brick], 0, 296, False, 'common_brick_wall_with_xps')
    roof = Element(0.5, 0.475, [0.025, 0.09396, 0.2], [
                   plaster, mineral_wool, concrete_slab], 0, 296, True, 'roof_concrete_slab_with_mineral_wool')
    mass = Element(0.20, 0.90, [0.05, 0.4], [
                   plaster, concrete_slab], 0, 296, True, 'concrete_floor')

    # ----------------------------------------------------------------------------------------------------------------

    # BUILDING PARAMETERS -----------------------------------------------------------------------------------------------

    bldg = Building(
        floor_height=2.878, int_heat_night=1, int_heat_day=1, int_heat_frad=1,
        int_heat_flat=1, infil=0.775, vent=0.98, glazing_ratio=0.217, u_value=2.534,
        shgc=0.583, condtype='AIR', cop=4.45, coolcap=900, heateff=0.8, initial_temp=300)

    bemdef1 = BEMDef(building=bldg, mass=mass, wall=wall,
                     roof=roof, bldtype='midriseapartment', builtera='pre80')

    # ------------------------------------------------------------------------------------------------------------------

    # VECTOR---------------------------------------------------------------------------------------

    ref_sch_vector = [schdef1]
    ref_bem_vector = [bemdef1]

    bld = [('midriseapartment', 'pre80', 1)  # overwrite
           ]  # extend

    # -------------------------------------------------------------------------------------------

    # UWG PARAMETERS ------------------------------------------------------------------------------------------------

    model = UWG.from_param_args(
        epw_path=epw_path, bldheight=bld_height, blddensity=bld_density, vertohor=ver_to_hor, zone='4B',
        treecover=0, grasscover=0, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector, month=8, day=17, sensanth=sensible_anthropogenic_heat, nday=7, dtsim=180, albroad=road_albedo,
        new_epw_name="simulation1h.epw",
        charlength=1000,  albveg=0.3, vegend=10, vegstart=3, kroad=urban_road_thermal_conductivity,
        croad=urban_road_volumetric_heat_capacity,
        c_exch=0.5, h_mix=0.5, h_ubl1=750, h_ubl2=75, c_circ=1, maxday=200, maxnight=50
    )

    # ---------------------------------------------------------------------------------------------------------------

    model.generate()
    model.simulate()

    model.write_epw()


# region Parameter Definition ------------------------------
problem = {
    'num_vars': 7,
    'names': ['bld_height', 'ver_to_hor', 'bld_density', 'urban_road_volumetric_heat_capacity', 'road_albedo',  # 6
              'sensible_anthropogenic_heat', 'urban_road_thermal_conductivity'],  # 2

    'bounds': [[2.716, 0.349],  # bld_height
               [1.302, 0.332],  # ver_to_hor
               [0.385508, 0.0375508],  # bld_density
               [1960371, 300000],  # urban_road_volumetric_heat_capacity
               # [1000, 100],       #urban_area_length
               [0.23345, 0.048025],  # road_albedo

               [20, 5],  # sensible_anthropogenic_heat
               [1.955, 0.4],  # urban_road_thermal_conductivity
               # [0.3302, 0.0517]    #urban_road_thickness

               ],

    'dists': ['lognorm', 'norm', 'norm', 'norm',  'norm',
              'norm', 'norm'
              ]
}

# endregion

param_values = saltelli.sample(problem, 1400)  # 1400

# region CSV index lists definition -------------------------
max_length = len(param_values)

temp_result_list = []
hdd_result_list = []
cdd_result_list = []
hdd_10C_result_list = []
day_max_temp_list = []
day_min_temp_list = []

bld_height_index = []
ver_to_hor_index = []
bld_density_index = []
urban_road_volumetric_heat_capacity_index = []
road_albedo_index = []
sensible_anthropogenic_heat_index = []
urban_road_thermal_conductivity_index = []


all_sensivity_indexes = [bld_height_index, ver_to_hor_index, bld_density_index, urban_road_volumetric_heat_capacity_index, road_albedo_index,
                         sensible_anthropogenic_heat_index, urban_road_thermal_conductivity_index]
# endregion


def evaluate_epw():
    k = 0
    l = 0
    m = 0
    y_1 = np.zeros((max_length, 7))
    y_2 = np.zeros((max_length, 7))
    y_3 = np.zeros((max_length, 7))
    y_4 = np.zeros((max_length, 7))
    y_5 = np.zeros((max_length, 7))
    y_6 = np.zeros((max_length, 7))
    y_7 = np.zeros((max_length, 7))
    y_8 = np.zeros((max_length, 7))
    y_9 = np.zeros((max_length, 7))
    y_10 = np.zeros((max_length, 7))
    y_11 = np.zeros((max_length, 7))
    y_12 = np.zeros((max_length, 7))
    y_13 = np.zeros((max_length, 7))
    y_14 = np.zeros((max_length, 7))
    y_15 = np.zeros((max_length, 7))
    y_16 = np.zeros((max_length, 7))
    y_17 = np.zeros((max_length, 7))
    y_18 = np.zeros((max_length, 7))
    y_19 = np.zeros((max_length, 7))
    y_20 = np.zeros((max_length, 7))
    y_21 = np.zeros((max_length, 7))
    y_22 = np.zeros((max_length, 7))
    y_23 = np.zeros((max_length, 7))
    y_24 = np.zeros((max_length, 7))

    all_y_indexes = [y_1, y_2, y_3, y_4, y_5, y_6, y_7, y_8, y_9, y_10, y_11,
                     y_12, y_13, y_14, y_15, y_16, y_17, y_18, y_19, y_20, y_21, y_22, y_23, y_24]
    hdd_y = np.zeros([max_length])
    cdd_y = np.zeros([max_length])
    hdd_10_y = np.zeros([max_length])
    for params in param_values:
        try:
            print("************ CURRENT ITERATION: " + str(int(m + 1)) + " / " +
                  str(max_length) + " EXCEPTIONS: " + str(l) + " ************")

            custom_uwg(float(params[0]), float(params[1]), float(params[2]), float(params[3]), float(params[4]),
                       float(params[5]), float(params[6])
                       )

            pd_epw_sens, _ = pvlib.iotools.read_epw(
                os.path.join(base_path, intermediate_epw_path))
            base_epw, _ = pvlib.iotools.read_epw(epw_path)

            indexes = range(5473, 5473 + 168)

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

            for h in range(0, 7):
                for b in range(0, 24):
                    hourly_temperature = pd_epw_sens['temp_air'].values[(
                        24 * h) + b + 5473]
                    hourly_base_temperature = base_epw['temp_air'].values[(
                        24 * h) + b + 5473]

                    if (hourly_temperature > hourly_base_temperature):
                        all_y_indexes[b][k][h] = hourly_temperature - \
                            hourly_base_temperature
                    else:
                        all_y_indexes[b][k][h] = 0

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
            m += 1

        except Exception as e:
            raise(e)
            print("EXCEPTION OCCURED")
            print(e)
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

            k += 1
            l += 1
            m += 1
            print("************ CURRENT ITERATION: " + str(int(m)) + " / " +
                  str(max_length) + " EXCEPTIONS: " + str(l) + " ************")
            print(str(float(params[0])), str(float(params[1])), str(float(params[2])), str(float(params[3])), str(float(params[4])),
                  str(float(params[5])), str(float(params[6]))
                  )

    #print(str(all_y_indexes[0]), str(all_y_indexes[2]))

    for b in range(0, 24):
        all_y_indexes[b] = np.transpose(all_y_indexes[b])
        all_y_indexes[b] = np.average(all_y_indexes[b], axis=0)

    return all_y_indexes, hdd_y, cdd_y, hdd_10_y


Y, HDD_Y, CDD_Y, HDD_10_Y = evaluate_epw()

Si_Temp = []
c = 0
for _ in Y:
    print(c)
    print(_)
    print(len(Y))
    print(sobol.analyze(problem, _))
    Si_Temp.append(sobol.analyze(problem, _))
    c = c + 1

for k in range(0, 24):
    for l in range(0, 7):
        all_sensivity_indexes[l].append(Si_Temp[k]["S1"][l])

data = {
    'bld_height': bld_height_index,
    'ver_to_hor': ver_to_hor_index,
    'bld_density': bld_density_index,
    'urban_road_volumetric_heat_capacity': urban_road_volumetric_heat_capacity_index,
    'road_albedo': road_albedo_index,
    'sensible_anthropogenic_heat': sensible_anthropogenic_heat_index,
    'urban_road_thermal_conductivity': urban_road_thermal_conductivity_index,
}

df = pd.DataFrame(data)
df.to_csv(base_path + "\\csvexport\\sobol-hourly-5-29-uc-s-S1.csv")

for k in range(0, 24):
    for l in range(0, 7):
        all_sensivity_indexes[l][k] = Si_Temp[k]["ST"][l]

data = {
    'bld_height': bld_height_index,
    'ver_to_hor': ver_to_hor_index,
    'bld_density': bld_density_index,
    'urban_road_volumetric_heat_capacity': urban_road_volumetric_heat_capacity_index,
    'road_albedo': road_albedo_index,
    'sensible_anthropogenic_heat': sensible_anthropogenic_heat_index,
    'urban_road_thermal_conductivity': urban_road_thermal_conductivity_index,
}

df = pd.DataFrame(data)
df.to_csv(base_path + "\\csvexport\\sobol-hourly-5-29-uc-s-ST.csv")


Si_CDD = sobol.analyze(problem, CDD_Y)
Si_HDD = sobol.analyze(problem, HDD_Y)
Si_HDD10 = sobol.analyze(problem, HDD_10_Y)

# print(str(Si_Temp))

lines = [str(Si_Temp), str(Si_CDD), str(Si_HDD), str(Si_HDD10)]
with open(base_path + '\\txtexport\\sobol-hourly-5-29-uc-s.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')
        f.write('------------')
        f.write('\n')

data = {
    'bld_height': bld_height_list,
    'ver_to_hor': ver_to_hor_list,
    'bld_density': bld_density_list,
    'urban_road_volumetric_heat_capacity': urban_road_volumetric_heat_capacity_list,
    'road_albedo': road_albedo_list,
    'sensible_anthropogenic_heat': sensible_anthropogenic_heat_list,
    'urban_road_thermal_conductivity': urban_road_thermal_conductivity_list,

    'temp_average': temp_result_list,
    'hdd_results': hdd_result_list,
    'hdd_10C_results': hdd_10C_result_list,
    'cdd_results': cdd_result_list,
    'daily_average_max_temperature': day_max_temp_list,
    'daily_average_min_temperature': day_min_temp_list
}

df = pd.DataFrame(data)
df.to_csv(base_path + "\\csvexport\\sobol-hourly-5-29-uc-s.csv")

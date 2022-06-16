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

default_week = [[0.15] * 24] * 3
occ_week = [[1,	1,	1,	1,	1, 1,	1,	0.85,	0.39,	0.25,	0.25,	0.25,
             0.25,	0.25,	0.25,	0.25,	0.3,	0.52,	0.87,	0.87,	0.87,	1,	1,	1],
            [1,	1,	1,	1,	1, 1,	1,	0.85,	0.39,	0.25,	0.25,	0.25,
             0.25,	0.25,	0.25,	0.25,	0.3,	0.52,	0.87,	0.87,	0.87,	1,	1,	1],
            [1,	1,	1,	1,	1, 1,	1,	0.85,	0.39,	0.25,	0.25,	0.25,
             0.25,	0.25,	0.25,	0.25,	0.3,	0.52,	0.87,	0.87,	0.87,	1,	1,	1]]

elec_week = [[0.45, 0.41, 0.39, 0.38, 0.38, 0.43, 0.54, 0.65, 0.66, 0.67, 0.69, 0.7, 0.69, 0.66, 0.65, 0.68, 0.8, 1, 1, 0.93, 0.89, 0.85, 0.71, 0.58],
             [0.45, 0.41, 0.39, 0.38, 0.38, 0.43, 0.54, 0.65, 0.66, 0.67, 0.69, 0.7,
                 0.69, 0.66, 0.65, 0.68, 0.8, 1, 1, 0.93, 0.89, 0.85, 0.71, 0.58],
             [0.45, 0.41, 0.39, 0.38, 0.38, 0.43, 0.54, 0.65, 0.66, 0.67, 0.69, 0.7, 0.69, 0.66, 0.65, 0.68, 0.8, 1, 1, 0.93, 0.89, 0.85, 0.71, 0.58]]

light_week = [[0.067, 0.067, 0.067, 0.067, 0.187, 0.394, 0.44, 0.393, 0.172, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.206, 0.439, 0.616, 0.829, 0.986, 1, 0.692, 0.384, 0.16],
              [0.067, 0.067, 0.067, 0.067, 0.187, 0.394, 0.44, 0.393, 0.172, 0.119, 0.119, 0.119,
                  0.119, 0.119, 0.119, 0.206, 0.439, 0.616, 0.829, 0.986, 1, 0.692, 0.384, 0.16],
              [0.067, 0.067, 0.067, 0.067, 0.187, 0.394, 0.44, 0.393, 0.172, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.206, 0.439, 0.616, 0.829, 0.986, 1, 0.692, 0.384, 0.16]]

cool_week = [[20] * 24] * 3

heat_week = [[20] * 24] * 3


schdef1 = SchDef(elec=elec_week, gas=default_week, light=light_week,
                 occ=occ_week, cool=cool_week, heat=heat_week,
                 q_elec=4.032759728, q_gas=3.2, q_light=4.563940577,
                 n_occ=(0.0296448), vent=0.001 * 0.2, bldtype='midriseapartment',
                 builtera='pre80')

# -----------------------------------------------------------------------------------------


# MATERIAL PARAMETERS ------------------------------------------------------------------------------------------------
brick = Material(0.33, 585000, 'brick')
xps = Material(0.035,  30000, "XPS")
plaster = Material(0.51,  1308000, "plaster")

mineral_wool = Material(0.04, 16600, "mineral_wool")
concrete_slab = Material(2.5, 2016000, 'concrete_slab')

# ELEMENT PARAMETERS -----------------------------------------------------------------------------------------------

roof_u_value = 0.290854924
wall_u_value = 0.315524164

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


wall = Element(0.5, 0.791, [0.025, xps_thickness, 0.135],  [
               plaster, xps, brick], 0, 296, False, 'common_brick_wall_with_xps')
roof = Element(0.5, 0.791, [0.025, mineral_wool_thickness, 0.2], [
               plaster, mineral_wool, concrete_slab], 0, 296, True, 'roof_concrete_slab_with_mineral_wool')
mass = Element(0.20, 0.90, [0.05, 0.4], [
               plaster, concrete_slab], 0, 296, True, 'concrete_floor')

# ----------------------------------------------------------------------------------------------------------------


# BUILDING PARAMETERS -----------------------------------------------------------------------------------------------

bldg = Building(
    floor_height=2.857198352, int_heat_night=1, int_heat_day=1, int_heat_frad=1,
    int_heat_flat=1, infil=0.286, vent=0.98, glazing_ratio=0.146229537, u_value=2.583612693,
    shgc=0.67863912, condtype='AIR', cop=5.166267931, coolcap=900, heateff=0.8, initial_temp=300)

bemdef1 = BEMDef(building=bldg, mass=mass, wall=wall, roof=roof,
                 bldtype='midriseapartment', builtera='pre80')

ref_sch_vector = [schdef1]
ref_bem_vector = [bemdef1]

bld = [('midriseapartment', 'pre80', 1)  # overwrite
       ]  # extend


epw_path = base_path + "data\\TUR_Ankara.171280_IWEC.epw"

model = UWG.from_param_args(
    epw_path=epw_path, bldheight=6.7, blddensity=0.285, vertohor=0.56, zone='4B',
    treecover=0, grasscover=0, bld=bld, ref_bem_vector=ref_bem_vector,
    ref_sch_vector=ref_sch_vector, month=1, day=1, sensanth=2.000, nday=365, dtsim=180, albroad=0.18,
    new_epw_name="winter-min-uhi.epw",
    charlength=1000,  albveg=0.3, vegend=10, vegstart=3, kroad=1.555463082,
    croad=1869595,
    c_exch=0.5, h_mix=0.5, h_ubl1=750, h_ubl2=75, c_circ=1, maxday=200, maxnight=50
)

# ---------------------------------------------------------------------------------------------------------------


model.generate()
model.simulate()

model.write_epw()

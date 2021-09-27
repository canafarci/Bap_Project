from operator import index, le
from uwg import Material, Element, Building, BEMDef, SchDef, UWG
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import pvlib
import numpy as np
import pandas as pd

def custom_uwg(urban_grass_coverage, urban_tree_coverage, vegetation_albedo): #'urban_grass_coverage', 'urban_tree_coverage', 'vegetation_albedo'
    """Generate UWG json with custom reference BEMDef and SchDef objects."""

    

    # SchDef PARAMETERS -----------------------------------------------------------------------

    default_week = [[0.15] * 24] * 3
    occ_week = [[0.3] * 24] * 3
    elec_week = [[7] * 24] * 3
    light_week = [[16] * 24] * 3
    cool_week = [[20] * 24] * 3
    heat_week = [[23] * 24] * 3
    
    schdef1 = SchDef(elec=elec_week, gas=default_week, light=light_week,
                     occ=occ_week, cool=cool_week, heat=heat_week,
                     q_elec=18.9, q_gas=3.2, q_light=18.9,
                     n_occ=0.03, vent=0.001 * 0.2, bldtype='midriseapartment',
                     builtera='pre80')
    
    ###-----------------------------------------------------------------------------------------



    # MATERIAL PARAMETERS ------------------------------------------------------------------------------------------------
    
    wallmtl = Material(0.5, 1300000, 'gypsum plaster')
    wallmt2 = Material(0.035, 25000, 'mineral fibre insulation')
    wallmt3 = Material(0.73, 1360000, 'brick')
    wallmt4 = Material(0.5, 1300000, 'gypsum plaster')

    roofmtl = Material(0.84, 1520000, 'tile')
    roofmt2 = Material(1.6, 1887000, 'concrete_floor')


    ###-------------------------------------------------------------------------------------------------------------------


    
    # ELEMENT PARAMETERS ---------------------------------------------------------------------------
    
    wall = Element(0.35, 0.90, [0.02, 0.15, 0.2, 0.01], [wallmtl, wallmt2, wallmt3,wallmt4], 0, 296, False, 'common_brick_wall_with_plaster')
    roof = Element(0.25, 0.95, [0.025, 0.025], [roofmtl, roofmtl], 0, 296, True, 'tile')
    mass = Element(0.20, 0.90, [0.15, 0.15], [roofmt2, roofmt2], 0, 296, True, 'concrete_floor')

    ### ---------------------------------------------------------------------------------------------



    # BUILDING PARAMETERS -----------------------------------------------------------------------------------------------

    bldg = Building(
        floor_height=3, int_heat_night=1, int_heat_day=1, int_heat_frad=1,
        int_heat_flat=1, infil=0.4, vent=0.001 * 0.2, glazing_ratio=0.25, u_value=2.4,
        shgc=0.3, condtype='AIR', cop=3, coolcap=900, heateff=0.8, initial_temp=300)

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
        treecover=urban_grass_coverage, grasscover=urban_grass_coverage, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector, month=7, day=1, sensanth=19.6, nday=31, dtsim=150, albroad=0.20, 
        new_epw_name="sensepw.epw",
        charlength=250, croad=2250000,albveg=vegetation_albedo, vegend=10,vegstart=3,droad=1.25,kroad=0.8,
        maxday=200, maxnight=50, h_ubl1=200, h_ubl2=75, h_mix=0.9,
        c_circ=1, c_exch=0.5)
    #'daytime_urban_boundary_height', 'nighttime_urban_boundary_height', 'circulation_coefficient', 'UCM_UBL_exchange_coefficient', 'day_heatflux_treshold', 'night_heatflux_treshold'
    ###---------------------------------------------------------------------------------------------------------------

    
    model.generate()
    model.simulate()
    
    model.write_epw()

problem = {
    'num_vars': 3,
    'names': ['urban_grass_coverage', 'urban_tree_coverage', 'vegetation_albedo'],
    'bounds': [[0, 0.1],     #urban_grass_coverage
               [0, 0.1],       #urban_tree_coverage
               [0.2, 0.3]]      #vegetation_albedo            
        }

# sample        
param_values = saltelli.sample(problem, 256)

print(param_values)
print(len(param_values))
max_length = len(param_values)


#custom_uwg(500, 50, 0.8, 0.1, 150, 40)

# evaluate
def evaluate_epw():
    k = 0
    l = 0
    m = 0
    y = np.zeros([max_length])
    for params in param_values:
        try:
            print(float(params[0]), float(params[1]), float(params[2]))
            custom_uwg(float(params[0]), float(params[1]), float(params[2]))
            pd_epw_sens, _ = pvlib.iotools.read_epw("E:\\ARCHIVE\\BAP\\uwg\\data\\sensepw.epw")
                
            indexes =  range(4345, 5089)
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
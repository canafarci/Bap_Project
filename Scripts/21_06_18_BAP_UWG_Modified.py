from uwg import Material, Element, Building, BEMDef, SchDef, UWG
import os
import json

""" # Define the .epw, .uwg paths to create an uwg object.
epw_path = "E:\\ARCHIVE\\BAP\\uwg\\data\\input.epw"
  

# Initialize the UWG model by passing parameters as arguments, or relying on defaults
model = UWG.from_param_args(bldheight=10, blddensity=0.5, vertohor=0.8, grasscover=0.1, treecover=0.1, zone='1A', epw_path=epw_path)

# Uncomment these lines to initialize the UWG model using a .uwg parameter file
# param_path = "initialize_singapore.uwg"  # available in the resources directory.
# model = UWG.from_param_file(param_path, epw_path=epw_path)

model.generate()
model.simulate()

# Write the simulation result to a file.
model.write_epw() """

def custom_uwg(directory):
    """Generate UWG json with custom reference BEMDef and SchDef objects."""

    # override at 5,2 and add at 18,2

    # SchDef
    default_week = [[0.15] * 24] * 3
    
    schdef1 = SchDef(elec=default_week, gas=default_week, light=default_week,
                     occ=default_week, cool=default_week, heat=default_week,
                     swh=default_week, q_elec=18.9, q_gas=3.2, q_light=18.9,
                     n_occ=0.12, vent=0.0013, v_swh=0.2846, bldtype='midriseapartment',
                     builtera='new')
    

    # BEMDedf

    # materials
    insulation = Material(0.049, 836.8 * 265.0, 'insulation')
    gypsum = Material(0.16, 830.0 * 784.9, 'gypsum')
    wood = Material(0.11, 1210.0 * 544.62, 'wood')

    # elements
    wall = Element(0.22, 0.92, [0.01, 0.01, 0.0127], [wood, insulation, gypsum], 0, 293,
                   False, 'wood_frame_wall')
    roof = Element(0.22, 0.92, [0.01, 0.01, 0.0127], [wood, insulation, gypsum], 0, 293,
                   True, 'wood_frame_roof')
    mass = Element(0.2, 0.9, [0.05, 0.05], [
                   wood, wood], 0, 293, True, 'wood_floor')

    # building
    bldg = Building(
        floor_height=3.0, int_heat_night=1, int_heat_day=1, int_heat_frad=0.1,
        int_heat_flat=0.1, infil=0.171, vent=0.00045, glazing_ratio=0.4, u_value=3.0,
        shgc=0.3, condtype='AIR', cop=3, coolcap=41, heateff=0.8, initial_temp=293)

    bemdef1 = BEMDef(building=bldg, mass=mass, wall=wall, roof=roof,
                     bldtype='midriseapartment', builtera='new')
    

    # vectors
    ref_sch_vector = [schdef1]
    ref_bem_vector = [bemdef1]
    bld = [('midriseapartment', 'new', 1.0)  # overwrite
           ]  # extend

    epw_path = "C:\\Users\\ZXEON\\Desktop\\BAP\\3-Agenda\\2021.06.16\\UWG_Python\\TUR_Ankara.171280_IWEC.epw"
    
    # URBAN AREA PARAMETERS START ------------------------------------------------------------------------------------------------------------------------

    model = UWG.from_param_args(
        epw_path=epw_path, bldheight=24.0, blddensity=0.60, vertohor=10, zone='5A',
        treecover=0.14, grasscover=0.16, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector,sensanth=10)

    # URBAN AREA PARAMETERS END ------------------------------------------------------------------------------------------------------------------------

    model.generate()
    model.simulate()
    
    model.write_epw()

    dest_file = os.path.join(directory, 'custom_uwg.json')
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(include_refDOE=True), fp, indent=4)
        

sample_directory = "C:\\Users\\ZXEON\\Desktop\\BAP\\3-Agenda\\2021.06.16\\UWG_School_Outputs"
custom_uwg(sample_directory)
        

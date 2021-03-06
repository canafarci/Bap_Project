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
    brick = Material(0.47, 1000000 * 2.018, 'wood')

    # elements
    wall = Element(0.5, 0.92, [0.1, 0.1, 0.0127], [brick, insulation, gypsum], 0, 293, False, 'wood_frame_wall')
    
    roof = Element(0.7, 0.92, [0.1, 0.1, 0.0127], [brick, insulation, gypsum], 1, 293, True, 'wood_frame_roof')
    
    mass = Element(0.20, 0.9, [0.5, 0.5], [brick, brick], 0, 293, True, 'wood_floor')

    # building
    bldg = Building(
        floor_height=3.0, int_heat_night=1, int_heat_day=1, int_heat_frad=0.1,
        int_heat_flat=0.1, infil=0.171, vent=0.00045, glazing_ratio=0.4, u_value=3.0,
        shgc=0.3, condtype='AIR', cop=3, coolcap=41, heateff=0.8, initial_temp=293)

    bemdef1 = BEMDef(building=bldg, mass=mass, wall=wall, roof=roof, bldtype='midriseapartment', builtera='new')
    

    # vectors
    
    ref_sch_vector = [schdef1]
    ref_bem_vector = [bemdef1]
    
    bld = [('midriseapartment', 'new', 1)  # overwrite
           ]  # extend

    epw_path = "E:\\ARCHIVE\\BAP\\uwg-BAP-Modified\\data\\ankara.epw"
    
    model = UWG.from_param_args(
        epw_path=epw_path, bldheight=17.5, blddensity=0.55, vertohor=1.8, zone='5A',
        treecover=0.2, grasscover=0.249, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector, month=1, day=1, sensanth=10, nday=365, dtsim=200, albroad=0.2)
    
    model.generate()
    model.simulate()
    
    model.write_epw()

    dest_file = os.path.join(directory, 'custom_uwg.json')
    
    with open(dest_file, 'w') as fp:
        json.dump(model.to_dict(include_refDOE=True), fp, indent=4)
        

sample_directory = "E:\ARCHIVE\BAP\deneme"

custom_uwg(sample_directory)
        

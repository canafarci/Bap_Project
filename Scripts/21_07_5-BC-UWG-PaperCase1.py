from uwg import Material, Element, Building, BEMDef, SchDef, UWG

def custom_uwg():
    """Generate UWG json with custom reference BEMDef and SchDef objects."""

    # override at 5,2 and add at 18,2

    # SchDef
    default_week = [[0.15] * 24] * 3
    elec_week = [[7] * 24] * 3
    light_week = [[16] * 24] * 3
    cool_week = [[22] * 24] * 3
    heat_week = [[23] * 24] * 3
    
    schdef1 = SchDef(elec=elec_week, gas=default_week, light=light_week,
                     occ=default_week, cool=cool_week, heat=heat_week,
                     q_elec=18.9, q_gas=3.2, q_light=18.9,
                     n_occ=0.03, vent=0.001 * 0.2, bldtype='midriseapartment',
                     builtera='new')
    
    # BEMDedf

    # materials
    wallmtl = Material(0.1122, 1210.0 * 544.62, 'wall')
    roofmtl = Material(0.1051, 1210.0 * 544.62, 'roof')

    # elements
    wall = Element(0.1, 0.92, [0.23, 0.1], [wallmtl, wallmtl], 0, 296, False, 'frame_wall')
    roof = Element(0.1, 0.92, [0.25, 0.1], [roofmtl, roofmtl], 0, 296, True, 'frame_roof')
    mass = Element(0.20, 0.9, [0.5, 0.5], [roofmtl, roofmtl], 0, 296, True, 'brick_floor')

    # building
    bldg = Building(
        floor_height=2.6, int_heat_night=1, int_heat_day=1, int_heat_frad=1,
        int_heat_flat=1, infil=0.5, vent=0.001 * 0.2, glazing_ratio=0.6, u_value=2,
        shgc=0.3, condtype='AIR', cop=3, coolcap=999, heateff=0.8, initial_temp=300)

    bemdef1 = BEMDef(building=bldg, mass=mass, wall=wall, roof=roof, bldtype='midriseapartment', builtera='new')
    

    # vectors
    
    ref_sch_vector = [schdef1]
    ref_bem_vector = [bemdef1]
    
    bld = [('midriseapartment', 'new', 1)  # overwrite
           ]  # extend

    epw_path = "E:\\ARCHIVE\\BAP\\uwg\\data\\TUR_Ankara.171280_IWEC.epw"
    
    model = UWG.from_param_args(
        epw_path=epw_path, bldheight=12, blddensity=0.749, vertohor=3, zone='5A',
        treecover=0, grasscover=0, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector, month=3, day=25, sensanth=100, nday=31, dtsim=100, albroad=0.05, new_epw_name="papercase1_dt.epw")
    
    model.generate()
    model.simulate()
    
    model.write_epw()
        

custom_uwg()
        

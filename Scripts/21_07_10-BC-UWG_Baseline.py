from uwg import Material, Element, Building, BEMDef, SchDef, UWG

def custom_uwg():
    """Generate UWG json with custom reference BEMDef and SchDef objects."""

    

    # SchDef PARAMETERS -----------------------------------------------------------------------

    default_week = [[0.15] * 24] * 3
    elec_week = [[7] * 24] * 3
    light_week = [[16] * 24] * 3
    cool_week = [[22] * 24] * 3
    heat_week = [[23] * 24] * 3
    
    schdef1 = SchDef(elec=elec_week, gas=default_week, light=light_week,
                     occ=default_week, cool=cool_week, heat=heat_week,
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
    
    wall = Element(0.35, 0.90, [0.02, 9, 0.2, 0.01], [wallmtl, wallmt2, wallmt3,wallmt4], 0, 296, False, 'common_brick_wall_with_plaster')
    roof = Element(0.25, 0.95, [0.025, 20], [roofmtl, roofmtl], 0, 296, True, 'tile')
    mass = Element(0.20, 0.90, [0.15, 0.15], [roofmt2, roofmt2], 0, 296, True, 'concrete_floor')

    ### ---------------------------------------------------------------------------------------------



    # BUILDING PARAMETERS -----------------------------------------------------------------------------------------------

    bldg = Building(
        floor_height=3, int_heat_night=1, int_heat_day=1, int_heat_frad=1,
        int_heat_flat=1, infil=0.75, vent=0.001 * 0.2, glazing_ratio=0.25, u_value=2.4,
        shgc=0.3, condtype='AIR', cop=3, coolcap=999, heateff=0.8, initial_temp=300)

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
        treecover=0.15, grasscover=0.04, bld=bld, ref_bem_vector=ref_bem_vector,
        ref_sch_vector=ref_sch_vector, month=7, day=1, sensanth=19.6, nday=31, dtsim=100, albroad=0.20, 
        new_epw_name="baseline_uwg.epw",
        charlength=250, croad=2250000,albveg=0.25,vegend=10,vegstart=3,droad=1.25,kroad=0.8)
    
    ###---------------------------------------------------------------------------------------------------------------

    
    model.generate()
    model.simulate()
    
    model.write_epw()
        

custom_uwg()
        

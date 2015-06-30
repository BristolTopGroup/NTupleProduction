def setup_electronID(process, cms):
    print '=' * 60
    print "Setting up electron ID (VID framework"
    print '=' * 60
    ###############################
    ###### Electron ID ############
    ###############################

    from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
    # turn on VID producer, indicate data format  to be
    # DataFormat.AOD or DataFormat.MiniAOD, as appropriate 
    dataFormat = DataFormat.MiniAOD

    switchOnVIDElectronIdProducer(process, dataFormat)

    # define which IDs we want to produce
    my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_PHYS14_PU20bx25_V2_cff',
                     'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV51_cff']

    #add them to the VID producer
    for idmod in my_id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)

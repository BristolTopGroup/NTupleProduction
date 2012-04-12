def setup_electronID(process, cms):
    print '=' * 60
    print "Setting up electron ID"
    print '=' * 60
    ###############################
    ###### Electron ID ############
    ###############################
    print 'Including Cuts in Categories Electron ID'
    process.load('RecoEgamma.ElectronIdentification.cutsInCategoriesElectronIdentificationV06_cfi')
    process.load('RecoEgamma.ElectronIdentification.cutsInCategoriesElectronIdentification_cfi')
    
    process.eidCiCSequence = cms.Sequence(
        process.eidVeryLoose * 
        process.eidLoose * 
        process.eidMedium * 
        process.eidTight * 
        process.eidSuperTight * 
        process.eidHyperTight1 * 
        process.eidHyperTight2 * 
        process.eidHyperTight3 * 
        process.eidHyperTight4 * 
        process.eidVeryLooseMC * 
        process.eidLooseMC * 
        process.eidMediumMC * 
        process.eidTightMC * 
        process.eidSuperTightMC * 
        process.eidHyperTight1MC * 
        process.eidHyperTight2MC * 
        process.eidHyperTight3MC * 
        process.eidHyperTight4MC
        )
    
    for iele in [ process.patElectrons,
                  process.patElectronsPFlow,
                  process.patElectronsLoosePFlow ] :
            iele.electronIDSources = cms.PSet(
                eidVeryLooseMC=cms.InputTag("eidVeryLooseMC"),
                eidLooseMC=cms.InputTag("eidLooseMC"),
                eidMediumMC=cms.InputTag("eidMediumMC"),
                eidTightMC=cms.InputTag("eidTightMC"),
                eidSuperTightMC=cms.InputTag("eidSuperTightMC"),
                eidHyperTight1MC=cms.InputTag("eidHyperTight1MC"),
                eidHyperTight2MC=cms.InputTag("eidHyperTight2MC"),
                eidHyperTight3MC=cms.InputTag("eidHyperTight3MC"),
                eidHyperTight4MC=cms.InputTag("eidHyperTight4MC"),
                #other ID
                eidVeryLoose=cms.InputTag("eidVeryLoose"),
                eidLoose=cms.InputTag("eidLoose"),
                eidMedium=cms.InputTag("eidMedium"),
                eidTight=cms.InputTag("eidTight"),
                eidSuperTight=cms.InputTag("eidSuperTight"),
                eidHyperTight1=cms.InputTag("eidHyperTight1"),
                eidHyperTight2=cms.InputTag("eidHyperTight2"),
                eidHyperTight3=cms.InputTag("eidHyperTight3"),
                eidHyperTight4=cms.InputTag("eidHyperTight4")               
    
    
                )
            
    # LikelihoodEle
    print 'Including EGammaID likelihood'
    process.load('RecoEgamma.ElectronIdentification.electronIdLikelihoodExt_cfi')
    process.egammaIDLikelihood = process.eidLikelihoodExt.clone()

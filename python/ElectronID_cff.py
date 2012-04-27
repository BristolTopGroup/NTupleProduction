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
    process.load('EGamma.EGammaAnalysisTools.electronIdMVAProducer_cfi') 

    process.mvaTrigV0.mvaWeightFile = mvaWeightFile = cms.vstring(
                                  "BristolAnalysis/NTupleTools/data/ElectronMVA/Electrons_BDTG_TrigV0_Cat1.weights.xml",
                                  "BristolAnalysis/NTupleTools/data/ElectronMVA/Electrons_BDTG_TrigV0_Cat2.weights.xml",
                                  "BristolAnalysis/NTupleTools/data/ElectronMVA/Electrons_BDTG_TrigV0_Cat3.weights.xml",
                                  "BristolAnalysis/NTupleTools/data/ElectronMVA/Electrons_BDTG_TrigV0_Cat4.weights.xml",
                                  "BristolAnalysis/NTupleTools/data/ElectronMVA/Electrons_BDTG_TrigV0_Cat5.weights.xml",
                                  "BristolAnalysis/NTupleTools/data/ElectronMVA/Electrons_BDTG_TrigV0_Cat6.weights.xml",
                            )

    process.mvaNonTrigV0.mvaWeightFile = mvaWeightFile = cms.vstring(
                                  "BristolAnalysis/NTupleTools/data/ElectronMVA/Electrons_BDTG_NonTrigV0_Cat1.weights.xml",
                                  "BristolAnalysis/NTupleTools/data/ElectronMVA/Electrons_BDTG_NonTrigV0_Cat2.weights.xml",
                                  "BristolAnalysis/NTupleTools/data/ElectronMVA/Electrons_BDTG_NonTrigV0_Cat3.weights.xml",
                                  "BristolAnalysis/NTupleTools/data/ElectronMVA/Electrons_BDTG_NonTrigV0_Cat4.weights.xml",
                                  "BristolAnalysis/NTupleTools/data/ElectronMVA/Electrons_BDTG_NonTrigV0_Cat5.weights.xml",
                                  "BristolAnalysis/NTupleTools/data/ElectronMVA/Electrons_BDTG_NonTrigV0_Cat6.weights.xml",
                            )
    process.eidMVASequence = cms.Sequence(  process.mvaTrigV0 + process.mvaNonTrigV0 )

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
        process.eidHyperTight4MC *
	process.eidMVASequence
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
                eidHyperTight4=cms.InputTag("eidHyperTight4"),
		mvaTrigV0    = cms.InputTag("mvaTrigV0"),
		mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0")     
                )
            
    # LikelihoodEle
    print 'Including EGammaID likelihood'
    process.load('RecoEgamma.ElectronIdentification.electronIdLikelihoodExt_cfi')
    process.egammaIDLikelihood = process.eidLikelihoodExt.clone()

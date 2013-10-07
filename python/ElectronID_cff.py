def setup_electronID(process, cms):
    print '=' * 60
    print "Setting up electron ID"
    print '=' * 60
    ###############################
    ###### Electron ID ############
    ###############################
    print 'Including Electron MVA ID'
    process.load('EgammaAnalysis.ElectronTools.electronIdMVAProducer_cfi') 

    process.eidMVASequence = cms.Sequence(  process.mvaTrigV0 + process.mvaNonTrigV0 )

    for iele in [ process.patElectrons,
                  process.patElectronsPFlow,
                  process.patElectronsLoosePFlow ] :
            iele.electronIDSources = cms.PSet(
                mvaTrigV0    = cms.InputTag("mvaTrigV0"),
                mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0")     
                )
            
    # LikelihoodEle
    print 'Including EGammaID likelihood'
    process.load('RecoEgamma.ElectronIdentification.electronIdLikelihoodExt_cfi')
    process.egammaIDLikelihood = process.eidLikelihoodExt.clone()

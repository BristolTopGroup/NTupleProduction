import FWCore.ParameterSet.Config as cms

electronUserData = cms.EDProducer(
    'ElectronUserData',
    vertexCollection=cms.InputTag('offlineSlimmedPrimaryVertices'),
    electronCollection=cms.InputTag("slimmedElectrons"),
    beamSpotCollection=cms.InputTag('offlineBeamSpot'),
    conversionInput=cms.InputTag('reducedEgamma', 'reducedConversions'),
    electronVetoIdMap=cms.InputTag(
        "egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto"),
    electronLooseIdMap=cms.InputTag(
        "egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose"),
    electronMediumIdMap=cms.InputTag(
        "egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium"),
    electronTightIdMap=cms.InputTag(
        "egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight"),
    electronHEEPIdMap=cms.InputTag("egmGsfElectronIDs:heepElectronID-HEEPV60"),
    # Top Object Definitions
    minLooseElectronPt=cms.double(15.),
    maxLooseElectronEta=cms.double(2.4),
    minSignalElectronPt=cms.double(23.),
    maxSignalElectronEta=cms.double(2.4),
    #     mediumElectronIDMap_bitmap=cms.InputTag(
    #         'egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-mediumBitmap'),

    #     rho        = cms.InputTag(rhoLabel),
    #     triggerResults = cms.InputTag(triggerResultsLabel),
    #     triggerSummary = cms.InputTag(triggerSummaryLabel),
    #     hltElectronFilter  = cms.InputTag(hltElectronFilterLabel),  ##trigger matching code to be fixed!
    #     hltPath             = cms.string("HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL"),
    #     eleIdVerbose=cms.bool(False)
)
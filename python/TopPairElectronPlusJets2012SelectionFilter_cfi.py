import FWCore.ParameterSet.Config as cms

EventFilter = cms.EDFilter('TopPairElectronPlusJets2012SelectionFilter',
    # Specify input collections
    jetInput=cms.InputTag("selectedPatJetsPFlow"),
    electronInput=cms.InputTag("selectedPatElectronsLoosePFlow"),
    muonInput=cms.InputTag("selectedPatMuonsLoosePFlow"),
    HLTInputTag=cms.InputTag('TriggerResults', '', 'HLT'),
    VertexInput=cms.InputTag('goodOfflinePrimaryVertices'),
    #event cleaning filters
    scrapingFilterInput=cms.InputTag('scrapingFilter'),
    HCALNoiseFilterInput=cms.InputTag('HBHENoiseFilterResultProducer', 'HBHENoiseFilterResult'),
    HCALLaserFilterInput=cms.InputTag('HcalLaserEventFilter'),
    ECALDeadCellFilterInput=cms.InputTag('EcalDeadCellBoundaryEnergyFilter'),
    TrackingFailureFilterInput=cms.InputTag('trackingFailureFilter'),
    BadEESupercrystalFilterInput=cms.InputTag('BadEESupercrystalFilter'),

#jet cuts
    min1JetPt=cms.double(45.),
    min2JetPt=cms.double(45.),
    min3JetPt=cms.double(45.),
    min4JetPt=cms.double(20.),
#lepton isolation
    tightElectronIsolation=cms.double(0.1),
    looseElectronIsolation=cms.double(0.15),
    looseMuonIsolation=cms.double(0.2),
    useDeltaBetaCorrections = cms.bool(False),
    useRhoActiveAreaCorrections = cms.bool(True),
    useMETFilters = cms.bool(True),
    useEEBadScFilter = cms.bool(False),
    
    prefix=cms.untracked.string('TopPairElectronPlusJets2012Selection.'),
    #flags
    debug=cms.untracked.bool(False),
    taggingMode=cms.untracked.bool(False),
)


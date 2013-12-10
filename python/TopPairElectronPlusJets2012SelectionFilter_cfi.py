import FWCore.ParameterSet.Config as cms

topPairEPlusJetsSelection = cms.EDFilter('TopPairElectronPlusJets2012SelectionFilter',
    # Specify input collections
    jetInput=cms.InputTag("selectedPatJetsPFlow"),
    electronInput=cms.InputTag("selectedPatElectronsLoosePFlow"),
    muonInput=cms.InputTag("selectedPatMuonsLoosePFlow"),
    HLTInput=cms.InputTag('TriggerResults', '', 'HLT'),
    VertexInput=cms.InputTag('goodOfflinePrimaryVertices'),
    #event cleaning filters
    trkInput=cms.InputTag('generalTracks'),#track input for scraping filter
    HcalNoiseInput=cms.InputTag('HBHENoiseFilterResultProducer', 'HBHENoiseFilterResult'),
    HCALLaserFilterInput=cms.InputTag('HcalLaserEventFilter'),
    ECALDeadCellFilterInput=cms.InputTag('EcalDeadCellBoundaryEnergyFilter'),
    TrackingFailureFilterInput=cms.InputTag('trackingFailureFilter'),
    BadEESupercrystalFilterInput=cms.InputTag('BadEESupercrystalFilter'),
    ECALLaserCorrFilterInput=cms.InputTag('ecalLaserCorrFilter'),
    #trackingPOGfilters
    ManyStripClus53XInput=cms.InputTag('manystripclus53X'),
    TooManyStripClus53XInput=cms.InputTag('toomanystripclus53X'),
    #LogErrorTooManyClusters=cms.InputTag('logErrorTooManyClusters'),

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
    MCSampleTag = cms.string('Summer12'),#Fall11 or Summer12
    #flags
    debug=cms.untracked.bool(False),
    taggingMode=cms.untracked.bool(False),
)


import FWCore.ParameterSet.Config as cms

EventFilter = cms.EDFilter(
    'EventFilter',
    #event filters
    HBHENoiseFilterInput=cms.InputTag('HBHENoiseFilterResultProducer', 'HBHENoiseFilterResult'),
    #optional MET filters
    HCALLaserFilterInput=cms.InputTag('HcalLaserEventFilter'),
    ECALDeadCellFilterInput=cms.InputTag('EcalDeadCellBoundaryEnergyFilter'),
    ECALDeadCellTriggerPrimitiveFilterInput = cms.InputTag('EcalDeadCellTriggerPrimitiveFilter'),
    TrackingFailureFilterInput=cms.InputTag('trackingFailureFilter'),
    EEBadSCFilterInput = cms.InputTag('eeBadScFilter'),
    useOptionalMETFilters=cms.bool(False),
    useTrackingFailureFilter=cms.bool(False),

    #track input for scraping filter
    TracksInput=cms.InputTag('generalTracks'),
    
    # Specify input collections
    electronInput=cms.InputTag("gsfElectrons"),
    muonInput=cms.InputTag("cleanPatMuons"),
    jetInput=cms.InputTag("ak5CaloJets"),

    # Specifiy number of jets
    minNJets=cms.int32(-1),
    maxNJets=cms.int32(-1),
    minJetPt=cms.double(30.),
    maxAbsJetEta=cms.double(100.),

    # Specify number of electrons
    minNElectrons=cms.int32(-1),
    maxNElectrons=cms.int32(-1),
    minElectronPt=cms.double(25.),
    maxAbsElectronEta=cms.double(100.),
    
    # Specify number of muons
    minNMuons=cms.int32(-1),
    maxNMuons=cms.int32(-1),
    minMuonPt=cms.double(15.),
    maxAbsMuonEta=cms.double(100.),
    #flags
    debug=cms.bool(False),
    counteitherleptontype=cms.bool(True),
    VertexInput=cms.InputTag('offlinePrimaryVertices'),
)


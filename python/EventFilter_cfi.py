import FWCore.ParameterSet.Config as cms

EventFilter = cms.EDFilter('EventFilter',
    # Specify input collections
    electronInput = cms.InputTag("gsfElectrons"),
    jetInput = cms.InputTag("ak5CaloJets"),

    # Specifiy number of jets
    minNJets = cms.int32(-1),
    maxNJets = cms.int32(-1),
    minJetPt   = cms.double(30.),
    maxAbsJetEta  = cms.double(100.),

    # Specify number of electrons
    minNElectrons = cms.int32(-1),
    maxNElectrons = cms.int32(-1),
    minElectronPt       = cms.double(25.),
    maxAbsElectronEta      = cms.double(100.),
    debug    = cms.untracked.bool(False),
    #Primary Vertex filtering
    VertexInput = cms.InputTag('offlinePrimaryVertices'),
    VertexMinimumNDOF = cms.uint32(7),
    VertexMaxAbsZ = cms.double(24.0),
    VertexMaxAbsRho = cms.double(2.),
    #ScrapingVeto
    TracksInput = cms.InputTag('generalTracks'),
    NumTracks = cms.uint32(10),
    HPTrackThreshold = cms.double(0.25),
    
    HcalNoiseInput = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResult'),
)


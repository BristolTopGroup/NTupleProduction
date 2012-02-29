import FWCore.ParameterSet.Config as cms

EventFilter = cms.EDFilter('TopSemiLeptonicEventFilter',
    # Specify input collections
    electronInput = cms.InputTag("selectedPatElectronsLoosePFlow"),
    muonInput = cms.InputTag("selectedPatMuonsLoosePFlow"),
    jetInput = cms.InputTag("selectedPatJetsPFlow"),

    # Specifiy number of jets
#    minNJets = cms.int32(-1),
#    maxNJets = cms.int32(-1),
    minJetPt   = cms.double(30.),
    maxAbsJetEta  = cms.double(2.4),

    # Specify number of electrons
#    minNElectrons = cms.int32(-1),
#    maxNElectrons = cms.int32(-1),
    minElectronPt       = cms.double(35.),
    maxAbsElectronEta      = cms.double(2.5),
    
    # Specify number of muons
#    minNMuons = cms.int32(-1),
#    maxNMuons = cms.int32(-1),
    minMuonPt       = cms.double(20.),
    maxAbsMuonEta      = cms.double(2.1),
    #flags
    debug    = cms.untracked.bool(False),
    useCiCElectronID = cms.untracked.bool(True),
#    counteitherleptontype    = cms.untracked.bool(True),
    #Primary Vertex filtering
    VertexInput = cms.InputTag('offlinePrimaryVertices'),
    VertexMinimumNDOF = cms.uint32(4),
    VertexMaxAbsZ = cms.double(24.0),
    VertexMaxAbsRho = cms.double(2.),
    #ScrapingVeto
    TracksInput = cms.InputTag('generalTracks'),
    NumTracks = cms.uint32(10),
    HPTrackThreshold = cms.double(0.25),
    
    HcalNoiseInput = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResult'),
)


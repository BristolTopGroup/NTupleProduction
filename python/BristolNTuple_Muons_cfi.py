import FWCore.ParameterSet.Config as cms

nTupleMuons = cms.EDProducer("BristolNTuple_Muons",
    InputTag = cms.InputTag('slimmedMuons'),
    Prefix = cms.string('Muons.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    minPtToStore = cms.double(10.),
    MuonID = cms.string('GlobalMuonPromptTight'),
    BeamSpotCorr = cms.bool(True),
    VertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
    BeamSpotInputTag = cms.InputTag('offlineBeamSpot'),
    storePFIsolation = cms.bool(True)
)

import FWCore.ParameterSet.Config as cms

nTupleMuons = cms.EDProducer("BristolNTuple_Muons",
    InputTag = cms.InputTag('slimmedMuons'),
    Prefix = cms.string('Muons.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    MuonID = cms.string('GlobalMuonPromptTight'),
    BeamSpotCorr = cms.bool(True),
    VertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
    storePFIsolation = cms.bool(True)
)

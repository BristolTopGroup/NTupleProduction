import FWCore.ParameterSet.Config as cms

nTupleMuons = cms.EDProducer("BristolNTuple_Muons",
    InputTag = cms.InputTag('cleanPatMuons'),
    Prefix = cms.string('Muon.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    VertexInputTag = cms.InputTag('offlinePrimaryVertices'),
    storePFIsolation = cms.bool(False)
)

nTuplePFMuons = nTupleMuons.clone(
    InputTag = cms.InputTag('selectedPatMuonsPF'),
    Prefix = cms.string('PFMuon.'),
    storePFIsolation = cms.bool(True)
)


nTupleMuonSequence =  cms.Sequence( nTupleMuons + nTuplePFMuons)
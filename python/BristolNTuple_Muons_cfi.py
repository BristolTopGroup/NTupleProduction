import FWCore.ParameterSet.Config as cms

nTupleMuons = cms.EDProducer("BristolNTuple_Muons",
    InputTag = cms.InputTag('cleanPatMuons'),
    Prefix = cms.string('Muon.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
     MuonID = cms.string('GlobalMuonPromptTight'),
    BeamSpotCorr = cms.bool(True),
    UseCocktailRefits = cms.bool(True),
    VertexInputTag = cms.InputTag('goodOfflinePrimaryVertices'),
    storePFIsolation = cms.bool(False)
)

nTuplePFLooseMuons = nTupleMuons.clone(
    InputTag = cms.InputTag('selectedPatMuonsPF'),
    Prefix = cms.string('PFLooseMuon.'),
    storePFIsolation = cms.bool(True)
)

nTuplePFMuons = nTupleMuons.clone(
    InputTag = cms.InputTag('selectedPatMuonsPF'),
    Prefix = cms.string('PFMuon.'),
    storePFIsolation = cms.bool(True)
)


nTupleMuonSequence =  cms.Sequence( nTupleMuons + nTuplePFMuons)
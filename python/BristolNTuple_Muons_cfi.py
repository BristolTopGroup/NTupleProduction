import FWCore.ParameterSet.Config as cms

nTupleMuons = cms.EDProducer("BristolNTuple_Muons",
    InputTag = cms.InputTag('cleanPatMuons'),
    Prefix = cms.string('Muon.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
#    MuonIso = cms.double(0.05),
#    MuonID = cms.string('GlobalMuonPromptTight'),
#    BeamSpotCorr = cms.bool(False),
    VertexInputTag = cms.InputTag('offlinePrimaryVertices'),
    storePFIsolation = cms.bool(False)
)

nTuplePFMuons = nTupleMuons.clone(
    InputTag = cms.InputTag('selectedPatMuonsPF'),
    Prefix = cms.string('PFMuon.'),
    storePFIsolation = cms.bool(True)
)

#rootTupleMuonsExtra = cms.EDProducer("BristolNTuple_Muons_Extra",
#    InputTag = cms.InputTag('cleanPatMuons'),
##    InputTagPVWithBS = cms.InputTag('cleanPatMu2'),
##    InputTagBS = cms.InputTag('cleanPatMu3'),
#    Prefix = cms.string('Muon.'),
#    Suffix = cms.string(''),
#    MaxSize = cms.uint32(99),
#    storePFIsolation = cms.bool(False)
#)
#
#rootTuplePFMuonsExtra = rootTupleMuonsExtra.clone(
#    InputTag = cms.InputTag('selectedPatMuonsPF'),
#    Prefix = cms.string('PFMuon.'),
#    storePFIsolation = cms.bool(True)
#)

nTupleMuonSequence =  cms.Sequence( nTupleMuons + nTuplePFMuons)# +  rootTupleMuonsExtra + rootTuplePFMuonsExtra)
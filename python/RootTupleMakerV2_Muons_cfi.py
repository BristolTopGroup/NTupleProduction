import FWCore.ParameterSet.Config as cms

rootTupleMuons = cms.EDProducer("RootTupleMakerV2_Muons",
    InputTag = cms.InputTag('cleanPatMuons'),
    Prefix = cms.string('Muon.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(10),
    MuonIso = cms.double(0.05),
    MuonID = cms.string('GlobalMuonPromptTight'),
    BeamSpotCorr = cms.bool(False),
    VertexInputTag = cms.InputTag('offlinePrimaryVertices')
)

rootTuplePFMuons = rootTupleMuons.clone(
    InputTag = cms.InputTag('selectedPatMuonsPF'),
    Prefix = cms.string('PFMuon.'),
)

rootTupleMuonsExtra = cms.EDProducer("RootTupleMakerV2_Muons_Extra",
    InputTag = cms.InputTag('cleanPatMuons'),
#    InputTagPVWithBS = cms.InputTag('cleanPatMu2'),
#    InputTagBS = cms.InputTag('cleanPatMu3'),
    Prefix = cms.string('Muon.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(10),
    storePFIsolation = cms.bool(False)
)

rootTuplePFMuonsExtra = rootTupleMuonsExtra.clone(
    InputTag = cms.InputTag('selectedPatMuonsPF'),
    Prefix = cms.string('PFMuon.'),
    storePFIsolation = cms.bool(True)
)

rootTupleMuonSequence =  cms.Sequence( rootTupleMuons + rootTuplePFMuons +  rootTupleMuonsExtra + rootTuplePFMuonsExtra)
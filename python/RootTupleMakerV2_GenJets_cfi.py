import FWCore.ParameterSet.Config as cms

rootTupleGenJets = cms.EDProducer("RootTupleMakerV2_GenJets",
    InputTag = cms.InputTag('ak5GenJets'),
    Prefix = cms.string('GenJet.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99)
)

rootTupleGenJetsExtra = cms.EDProducer("RootTupleMakerV2_GenJets_Extra",
    InputTag = cms.InputTag('ak5GenJets'),
    Prefix = cms.string('GenJet.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99)
)

rootTupleGenJetSequence = cms.Sequence(rootTupleGenJets + rootTupleGenJetsExtra)


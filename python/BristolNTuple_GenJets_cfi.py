import FWCore.ParameterSet.Config as cms

rootTupleGenJets = cms.EDProducer("BristolNTuple_GenJets",
    InputTag = cms.InputTag('ak5GenJetsNoNu'),
    Prefix = cms.string('GenJet.'),
    Suffix = cms.string(''),
    minPt = cms.double(-1),
    maxAbsoluteEta = cms.double(999),
    MaxSize = cms.uint32(99)
)

rootTupleGenJetSequence = cms.Sequence(rootTupleGenJets)


import FWCore.ParameterSet.Config as cms

rootTupleGenJets = cms.EDProducer("BristolNTuple_GenJets",
    InputTag = cms.InputTag('ak5GenJets'),
    Prefix = cms.string('GenJet.'),
    Suffix = cms.string(''),
    minPt = cms.double(15.),
    maxAbsoluteEta = cms.double(2.6),
    MaxSize = cms.uint32(99)
)

rootTupleGenJetSequence = cms.Sequence(rootTupleGenJets)


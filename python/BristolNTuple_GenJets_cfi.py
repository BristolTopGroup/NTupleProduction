import FWCore.ParameterSet.Config as cms

nTupleGenJets = cms.EDProducer("BristolNTuple_GenJets",
    InputTag = cms.InputTag('slimmedGenJets'),
    Prefix = cms.string('GenJet.'),
    Suffix = cms.string(''),
    minPt = cms.double(30),
    maxAbsoluteEta = cms.double(999),
    MaxSize = cms.uint32(99)
)


import FWCore.ParameterSet.Config as cms

rootTupleGenParticles = cms.EDProducer("BristolNTuple_GenParticles",
    InputTag = cms.InputTag('genParticles'),
    Prefix = cms.string('GenParticle.'),
    Suffix = cms.string(''),
    minPt = cms.double(10.),
    maxAbsoluteEta = cms.double(2.6),
    MaxSize = cms.uint32(25)
)


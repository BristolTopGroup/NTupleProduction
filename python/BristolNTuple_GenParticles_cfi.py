import FWCore.ParameterSet.Config as cms

nTupleGenParticles = cms.EDProducer("BristolNTuple_GenParticles",
    InputTag = cms.InputTag('prunedGenParticles'),
    Prefix = cms.string('GenParticle.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(25)
)


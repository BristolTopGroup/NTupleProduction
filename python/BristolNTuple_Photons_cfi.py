import FWCore.ParameterSet.Config as cms

rootTuplePhotons = cms.EDProducer("BristolNTuple_Photons",
    InputTag = cms.InputTag('cleanPatPhotons'),
    Prefix = cms.string('Photon'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(25),
)

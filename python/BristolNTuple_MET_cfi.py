import FWCore.ParameterSet.Config as cms

nTupleMET = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('slimmedMETs'),
    Prefix=cms.string('MET.'),
    Suffix=cms.string(''),
)

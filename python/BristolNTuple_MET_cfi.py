import FWCore.ParameterSet.Config as cms

nTupleMET = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('slimmedMETs'),
    storeMETUncertainties=cms.bool(True),
    nMETUncertainties=cms.uint32(12),
    Prefix=cms.string('MET.'),
    Suffix=cms.string(''),
)

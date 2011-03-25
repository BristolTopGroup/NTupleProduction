import FWCore.ParameterSet.Config as cms

rootTupleBeamSpot = cms.EDProducer("BristolNTuple_BeamSpot",
    Prefix = cms.string('BeamSpot.'),
    Suffix = cms.string(''),
)


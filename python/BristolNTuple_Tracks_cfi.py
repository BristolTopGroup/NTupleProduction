import FWCore.ParameterSet.Config as cms

rootTupleTracks = cms.EDProducer("BristolNTuple_Tracks",
    Prefix = cms.string('Track.'),
    Suffix = cms.string(''),
)


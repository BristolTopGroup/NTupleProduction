import FWCore.ParameterSet.Config as cms

rootTupleBeamSpot = cms.EDProducer("RootTupleMakerV2_BeamSpot",
    Prefix = cms.string('BeamSpot.'),
    Suffix = cms.string(''),
)


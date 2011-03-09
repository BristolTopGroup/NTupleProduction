import FWCore.ParameterSet.Config as cms

rootTupleTracks = cms.EDProducer("RootTupleMakerV2_Tracks",
    Prefix = cms.string('Track.'),
    Suffix = cms.string(''),
)


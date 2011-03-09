import FWCore.ParameterSet.Config as cms
rootTupleEvent = cms.EDProducer("RootTupleMakerV2_Event")

rootTupleEventExtra = cms.EDProducer("RootTupleMakerV2_Event_Extra",
    DCSInputTag = cms.InputTag('scalersRawToDigi')
)

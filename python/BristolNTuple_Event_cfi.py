import FWCore.ParameterSet.Config as cms
nTupleEvent = cms.EDProducer(
        "BristolNTuple_Event",
        recoVertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
        Prefix=cms.string('Event.'),
        Suffix=cms.string('')
)

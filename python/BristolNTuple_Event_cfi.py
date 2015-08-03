import FWCore.ParameterSet.Config as cms
nTupleEvent = cms.EDProducer(
        "BristolNTuple_Event",
        recoVertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
	    metFiltersInputTag = cms.InputTag('TriggerResults','','RECO'),
        Prefix=cms.string('Event.'),
        Suffix=cms.string('')
)

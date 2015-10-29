import FWCore.ParameterSet.Config as cms
nTupleEvent = cms.EDProducer(
        "BristolNTuple_Event",
        recoVertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
	    # metFiltersInputTag = cms.InputTag('TriggerResults','','RECO'),
	    # metFiltersOfInterest = cms.vstring('Flag_CSCTightHaloFilter', 'Flag_eeBadScFilter'),
        Prefix=cms.string('Event.'),
        Suffix=cms.string('')
)

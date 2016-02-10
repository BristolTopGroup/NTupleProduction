import FWCore.ParameterSet.Config as cms
nTupleEvent = cms.EDProducer( "BristolNTuple_Event",
        recoVertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
	    metFiltersToken = cms.InputTag('TriggerResults','','RECO'),
	    metFiltersOfInterest = cms.vstring(
			'Flag_HBHENoiseFilter', 
			'Flag_HBHENoiseIsoFilter', 
			'Flag_CSCTightHalo2015Filter', 
			'Flag_EcalDeadCellTriggerPrimitiveFilter', 
			'Flag_goodVertices', 
			'Flag_eeBadScFilter', 
			'Flag_chargedHadronTrackResolutionFilter', 
			'Flag_muonBadTrackFilter',
	    ),
        Prefix=cms.string('Event.'),
        Suffix=cms.string('')
)

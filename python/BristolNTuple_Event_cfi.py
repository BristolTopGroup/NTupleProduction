import FWCore.ParameterSet.Config as cms
from BristolAnalysis.NTupleTools.options import is2016

nTupleEvent = cms.EDProducer( "BristolNTuple_Event",
        recoVertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
	    metFiltersToken = cms.InputTag('TriggerResults','','RECO'),
	    metFiltersOfInterest = cms.vstring(
			'Flag_HBHENoiseFilter',
			'Flag_HBHENoiseIsoFilter',
			'Flag_globalTightHalo2016Filter',
			'Flag_EcalDeadCellTriggerPrimitiveFilter',
			'Flag_goodVertices',
			'Flag_eeBadScFilter',
	    ),
	    badChargedCandidateFilter = cms.InputTag("BadChargedCandidateFilter"),
	    badPFMuonFilter = cms.InputTag("BadPFMuonFilter"),
        is2016Regime=cms.bool(is2016),
        Prefix=cms.string('Event.'),
        Suffix=cms.string('')
)

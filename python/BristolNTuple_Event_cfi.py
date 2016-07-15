import FWCore.ParameterSet.Config as cms
from BristolAnalysis.NTupleTools.options import is2016

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
			# 'Flag_chargedHadronTrackResolutionFilter',
			# 'Flag_muonBadTrackFilter',
	    ),
        is2016Regime=cms.bool(is2016),
        Prefix=cms.string('Event.'),
        Suffix=cms.string('')
)

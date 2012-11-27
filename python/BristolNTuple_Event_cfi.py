import FWCore.ParameterSet.Config as cms
rootTupleEvent = cms.EDProducer(
        "BristolNTuple_Event",
        DCSInputTag=cms.InputTag('scalersRawToDigi'),
        HCALLaserFilterInput=cms.InputTag('HcalLaserEventFilter'),
        ECALDeadCellFilterInput=cms.InputTag('EcalDeadCellBoundaryEnergyFilter'),
	ECALDeadCellTriggerPrimitiveFilterInput=cms.InputTag('EcalDeadCellTriggerPrimitiveFilter'),
        TrackingFailureFilterInput=cms.InputTag('trackingFailureFilter'),
        METInputForSumET=cms.InputTag('patMETsPFlow'),
        Prefix=cms.string('Event.'),
        Suffix=cms.string('')
)

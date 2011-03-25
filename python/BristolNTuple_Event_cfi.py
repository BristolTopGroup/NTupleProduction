import FWCore.ParameterSet.Config as cms
rootTupleEvent = cms.EDProducer("BristolNTuple_Event",
                                DCSInputTag = cms.InputTag('scalersRawToDigi'))

#rootTupleEventExtra = cms.EDProducer("BristolNTuple_Event_Extra",
#    DCSInputTag = cms.InputTag('scalersRawToDigi')
#)

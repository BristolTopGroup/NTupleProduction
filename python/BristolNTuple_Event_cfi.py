import FWCore.ParameterSet.Config as cms
rootTupleEvent = cms.EDProducer("BristolNTuple_Event",
                                DCSInputTag=cms.InputTag('scalersRawToDigi'),
                                Prefix=cms.string('Event.'),
                                Suffix=cms.string('')
)

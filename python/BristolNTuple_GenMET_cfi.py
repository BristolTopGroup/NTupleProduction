import FWCore.ParameterSet.Config as cms

nTupleGenMET = cms.EDProducer( "BristolNTuple_GenMET",
    InputTag = cms.InputTag( 'slimmedMETs' ),
    Prefix = cms.string( 'GenMET.' ),
    Suffix = cms.string( '' )
 )


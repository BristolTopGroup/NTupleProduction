import FWCore.ParameterSet.Config as cms

rootTupleGenMETTrue = cms.EDProducer( "BristolNTuple_GenMET",
    InputTag = cms.InputTag( 'genMetTrue' ),
    Prefix = cms.string( 'GenMET.' ),
    Suffix = cms.string( '' )
 )

rootTupleGenMETCalo = cms.EDProducer( "BristolNTuple_GenMET",
    InputTag = cms.InputTag( 'genMetCalo' ),
    Prefix = cms.string( 'GenMET.' ),
    Suffix = cms.string( 'Calo' )
 )

import FWCore.ParameterSet.Config as cms

rootTupleGenMETTrue = cms.EDProducer( "BristolNTuple_GenMET",
    InputTag = cms.InputTag( 'genMetTrue' ),
    Prefix = cms.string( 'Gen' ),
    Suffix = cms.string( 'True' )
 )

rootTupleGenMETCalo = cms.EDProducer( "BristolNTuple_GenMET",
    InputTag = cms.InputTag( 'genMetCalo' ),
    Prefix = cms.string( 'Gen' ),
    Suffix = cms.string( 'Calo' )
 )

#rootTupleGenMETTrueExtra = cms.EDProducer( "BristolNTuple_GenMET_Extra",
#    InputTag = cms.InputTag( 'genMetTrue' ),
#    Prefix = cms.string( 'Gen' ),
#    Suffix = cms.string( 'True' )
# )
#
#rootTupleGenMETCaloExtra = cms.EDProducer( "BristolNTuple_GenMET_Extra",
#    InputTag = cms.InputTag( 'genMetCalo' ),
#    Prefix = cms.string( 'Gen' ),
#    Suffix = cms.string( 'Calo' )
# )
rootTupleGenMETSequence = cms.Sequence( rootTupleGenMETTrue)# + rootTupleGenMETTrueExtra )


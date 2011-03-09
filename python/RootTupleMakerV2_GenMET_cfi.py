import FWCore.ParameterSet.Config as cms

rootTupleGenMETTrue = cms.EDProducer( "RootTupleMakerV2_GenMET",
    InputTag = cms.InputTag( 'genMetTrue' ),
    Prefix = cms.string( 'Gen' ),
    Suffix = cms.string( 'True' )
 )

rootTupleGenMETCalo = cms.EDProducer( "RootTupleMakerV2_GenMET",
    InputTag = cms.InputTag( 'genMetCalo' ),
    Prefix = cms.string( 'Gen' ),
    Suffix = cms.string( 'Calo' )
 )

rootTupleGenMETTrueExtra = cms.EDProducer( "RootTupleMakerV2_GenMET_Extra",
    InputTag = cms.InputTag( 'genMetTrue' ),
    Prefix = cms.string( 'Gen' ),
    Suffix = cms.string( 'True' )
 )

rootTupleGenMETCaloExtra = cms.EDProducer( "RootTupleMakerV2_GenMET_Extra",
    InputTag = cms.InputTag( 'genMetCalo' ),
    Prefix = cms.string( 'Gen' ),
    Suffix = cms.string( 'Calo' )
 )
rootTupleGenMETSequence = cms.Sequence( rootTupleGenMETTrue + rootTupleGenMETTrueExtra )


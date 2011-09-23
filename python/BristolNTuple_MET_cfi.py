import FWCore.ParameterSet.Config as cms

rootTupleCaloMET = cms.EDProducer( "BristolNTuple_MET",
    InputTag = cms.InputTag( 'patMETs' ),
    Prefix = cms.string( 'patMETs.' ),
    Suffix = cms.string( '' ),
    StoreUncorrectedMET = cms.bool( True )
 )

rootTupleTCMET = cms.EDProducer( "BristolNTuple_MET",
    InputTag = cms.InputTag( 'patMETsTC' ),
    Prefix = cms.string( 'TCMET.' ),
    Suffix = cms.string( '' ),
    StoreUncorrectedMET = cms.bool( True )
 )

rootTuplePFMET = cms.EDProducer( "BristolNTuple_MET",
    InputTag = cms.InputTag( 'patMETsPFlow' ),
    Prefix = cms.string( 'patMETsPFlow.' ),
    Suffix = cms.string( '' ),
    StoreUncorrectedMET = cms.bool( True )
 )

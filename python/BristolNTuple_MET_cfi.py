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

rootTuplePFType1CorrectedMET = cms.EDProducer( "BristolNTuple_MET",
    InputTag = cms.InputTag( 'patType1CorrectedPFMet' ),
    Prefix = cms.string( 'patType1CorrectedPFMet.' ),
    Suffix = cms.string( '' ),
    StoreUncorrectedMET = cms.bool( False )
 )

rootTuplePFType1p2CorrectedMET = cms.EDProducer( "BristolNTuple_MET",
    InputTag = cms.InputTag( 'patType1p2CorrectedPFMet' ),
    Prefix = cms.string( 'patType1p2CorrectedPFMet.' ),
    Suffix = cms.string( '' ),
    StoreUncorrectedMET = cms.bool( False )
 )

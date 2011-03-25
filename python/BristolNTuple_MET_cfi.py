import FWCore.ParameterSet.Config as cms

rootTupleCaloMET = cms.EDProducer( "BristolNTuple_MET",
    InputTag = cms.InputTag( 'patMETs' ),
    Prefix = cms.string( 'CaloMET.' ),
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
    InputTag = cms.InputTag( 'patMETsPF' ),
    Prefix = cms.string( 'PFMET.' ),
    Suffix = cms.string( '' ),
    StoreUncorrectedMET = cms.bool( True )
 )

#rootTuplePFMETType1Cor = cms.EDProducer( "BristolNTuple_MET_Extra",
#    InputTag = cms.InputTag( 'patMETsPFType1Cor' ),
#    Prefix = cms.string( 'PF' ),
#    Suffix = cms.string( 'Type1Cor' ),
#    StoreUncorrectedMET = cms.bool( False )
# )
#
#rootTupleCaloMETExtra = cms.EDProducer( "BristolNTuple_MET_Extra",
#    InputTag = cms.InputTag( 'patMETs' ),
#    Prefix = cms.string( 'Calo' ),
#    Suffix = cms.string( '' ),
#    StoreUncorrectedMET = cms.bool( True )
# )
#
#rootTupleTCMETExtra = cms.EDProducer( "BristolNTuple_MET_Extra",
#    InputTag = cms.InputTag( 'patMETsTC' ),
#    Prefix = cms.string( 'TC' ),
#    Suffix = cms.string( '' ),
#    StoreUncorrectedMET = cms.bool( False )
# )
#
#rootTuplePFMETExtra = cms.EDProducer( "BristolNTuple_MET_Extra",
#    InputTag = cms.InputTag( 'patMETsPF' ),
#    Prefix = cms.string( 'PF' ),
#    Suffix = cms.string( '' ),
#    StoreUncorrectedMET = cms.bool( False )
# )
#
#rootTuplePFMETType1CorExtra = cms.EDProducer( "BristolNTuple_MET_Extra",
#    InputTag = cms.InputTag( 'patMETsPFType1Cor' ),
#    Prefix = cms.string( 'PF' ),
#    Suffix = cms.string( 'Type1Cor' ),
#    StoreUncorrectedMET = cms.bool( False )
#    )


rootTupleMETSequence = cms.Sequence( rootTupleCaloMET + rootTuplePFMET ) 
                                     #+ rootTupleCaloMETExtra + rootTuplePFMETExtra)

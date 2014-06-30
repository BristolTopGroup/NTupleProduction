import FWCore.ParameterSet.Config as cms

eventWeightBtag = cms.EDProducer("BTagWeight_Producer",
    numberOfTagsInput = cms.InputTag( 'TopPairElectronPlusJetsSelection.NumberOfBtags' ),
    jetInput = cms.InputTag( 'TopPairElectronPlusJetsSelection.cleanedJets' ),
    prefix = cms.string('Weights.'),
    MCSampleTag = cms.string('Summer12'), #Fall11 or Summer12 or Summer11Leg
    targetBtagMultiplicity = cms.uint32(0),
    BJetSystematic = cms.int32(0),
)


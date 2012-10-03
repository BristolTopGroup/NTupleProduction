import FWCore.ParameterSet.Config as cms

eventWeightBtag = cms.EDProducer("BTagWeight_Producer",
    numberOfTagsInput = cms.InputTag( 'TopPairElectronPlusJets2012Selection.NumberOfBtags' ),
    jetInput = cms.InputTag( 'TopPairElectronPlusJets2012Selection.cleanedJets' ),
    prefix = cms.string('Weights.'),
    targetBtagMultiplicity = cms.uint(0),
    BJetSystematic = cms.int(0),
)


import FWCore.ParameterSet.Config as cms

topPairEPlusJetsSelection = cms.EDFilter('TopPairElectronPlusJetsSelectionFilter',
    # Specify input collections
    cleanedJets=cms.InputTag("goodJets"),
    cleanedBJets=cms.InputTag("goodBJets"),
    goodElectrons=cms.InputTag("goodElectrons"),
    vetoElectrons=cms.InputTag("vetoElectrons"),
    electrons=cms.InputTag("electronUserData"),
    vetoMuons=cms.InputTag("vetoMuons"),
    HLTInput=cms.InputTag('TriggerResults', '', 'HLT'),

    prefix=cms.untracked.string('TopPairElectronPlusJetsSelection.'),
    MCSampleTag = cms.string('Summer12'),#Fall11 or Summer12 or Summer11Leg

    #flags
    taggingMode=cms.bool(False),

    tagAndProbeStudies = cms.bool(False),
    dropTriggerSelection = cms.bool(False),
    jetSelectionInTaggingMode = cms.bool(False),
    bSelectionInTaggingMode = cms.bool(True),
    nonIsolatedElectronSelection = cms.bool(False),
    invertedConversionSelection = cms.bool(False),
)


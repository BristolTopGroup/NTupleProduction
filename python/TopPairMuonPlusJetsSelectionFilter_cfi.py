import FWCore.ParameterSet.Config as cms
###############################################################################
# signal selection
###############################################################################
topPairMuPlusJetsSelection = cms.EDFilter(
    'TopPairMuonPlusJetsSelectionFilter',
    # Specify input collections
    cleanedJets=cms.InputTag("goodJets"),
    cleanedBJets=cms.InputTag("goodBJets"),
    vetoElectrons=cms.InputTag("vetoElectrons"),
    vetoMuons=cms.InputTag("vetoMuons"),
    goodMuons=cms.InputTag("goodMuons"),
    muons=cms.InputTag("muonUserData"),
    HLTInput=cms.InputTag('TriggerResults', '', 'HLT'),

    prefix=cms.untracked.string('TopPairMuonPlusJetsSelection.'),

    # flags
    taggingMode=cms.bool(False),

    tagAndProbeStudies=cms.bool(False),
    dropTriggerSelection=cms.bool(False),
    bSelectionInTaggingMode=cms.bool(True),
    nonIsolatedMuonSelection1=cms.bool(False),
    nonIsolatedMuonSelection2=cms.bool(False),
)

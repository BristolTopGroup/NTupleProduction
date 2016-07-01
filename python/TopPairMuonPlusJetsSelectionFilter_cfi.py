import FWCore.ParameterSet.Config as cms

topPairMuPlusJetsSelection = cms.EDFilter('TopPairMuonPlusJetsSelectionFilter',
    # Specify input collections
    jetInput=cms.InputTag("patJetsReapplyJEC"),
    electronInput=cms.InputTag("slimmedElectrons"),
    muonInput=cms.InputTag("slimmedMuons"),
    HLTInput=cms.InputTag('TriggerResults', '', 'HLT'),

    #jet cuts
#     min1JetPt=cms.double(20.),
#     min2JetPt=cms.double(20.),
#     min3JetPt=cms.double(20.),
#     min4JetPt=cms.double(20.),
#     minBJetPt=cms.double(20.),
#     minJetPtInNtuples=cms.double(20.),

    # Jet cleaning delta R
    cleaningDeltaR=cms.double(0.4),

    # Apply different JEC
    applyJEC = cms.bool(False),
    JetCorrectionService = cms.string('ak4PFCHSL1FastL2L3'),

    # B Jet Selection
    # Working points taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation74X50ns
    bJetDiscriminator=cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
    minBJetDiscriminator=cms.double(0.800),
    tightBJetDiscriminator=cms.double(0.935),

    prefix=cms.untracked.string('TopPairMuonPlusJetsSelection.'),

    #flags
    debug=cms.untracked.bool(False),
    taggingMode=cms.bool(False),

    tagAndProbeStudies = cms.bool(False),
    dropTriggerSelection = cms.bool(False),
    bSelectionInTaggingMode = cms.bool(True),
    nonIsolatedMuonSelection1 = cms.bool(False),
    nonIsolatedMuonSelection2 = cms.bool(False),
)


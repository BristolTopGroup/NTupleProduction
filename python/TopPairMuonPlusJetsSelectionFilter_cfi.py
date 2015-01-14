import FWCore.ParameterSet.Config as cms

topPairMuPlusJetsSelection = cms.EDFilter('TopPairMuonPlusJetsSelectionFilter',
    # Specify input collections
    jetInput=cms.InputTag("slimmedJets"),
    electronInput=cms.InputTag("slimmedElectrons"),
    muonInput=cms.InputTag("slimmedMuons"),
    HLTInput=cms.InputTag('TriggerResults', '', 'HLT'),
    VertexInput=cms.InputTag('offlineSlimmedPrimaryVertices'),

    # Signal muon cuts
    minSignalMuonPt=cms.double(30.),
    maxSignalMuonEta=cms.double(2.1),
    minLooseMuonPt=cms.double(10.),
    maxLooseMuonEta=cms.double(2.5),
    minLooseElectronPt=cms.double(20.),
    maxLooseElectronEta=cms.double(2.5),

    #jet cuts
    min1JetPt=cms.double(30.),
    min2JetPt=cms.double(30.),
    min3JetPt=cms.double(30.),
    min4JetPt=cms.double(30.),
    minBJetPt=cms.double(30.),
    minJetPtInNtuples=cms.double(30.),

    # Jet cleaning delta R
    cleaningDeltaR=cms.double(0.3),

    # Maximum isolation for signal region
    tightMuonIsolation=cms.double(0.12),
    # Minimum isolation for control region
    controlMuonIsolation=cms.double(0.3),

    # B Jet Selection
<<<<<<< HEAD
    # Working points taken from https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagging#Preliminary_working_or_operating
    bJetDiscriminator=cms.string('combinedInclusiveSecondaryVertexV2BJetTags'),
    minBJetDiscriminator=cms.double(0.814),
=======
    bJetDiscriminator=cms.string('combinedSecondaryVertexBJetTags'),
    minBJetDiscriminator=cms.double(0.679),
>>>>>>> 3a4a153... Update our selection filtersand add to paths.  Simplify by removing many events filters etc.

    prefix=cms.untracked.string('TopPairMuonPlusJetsSelection.'),

    #flags
    debug=cms.untracked.bool(False),
    taggingMode=cms.bool(False),

    tagAndProbeStudies = cms.bool(False),
    dropTriggerSelection = cms.bool(False),
    bSelectionInTaggingMode = cms.bool(False),
    nonIsolatedMuonSelection = cms.bool(False),
)


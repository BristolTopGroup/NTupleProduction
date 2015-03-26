import FWCore.ParameterSet.Config as cms

topPairEPlusJetsSelection = cms.EDFilter('TopPairElectronPlusJetsSelectionFilter',
    # Specify input collections
    jetInput=cms.InputTag("slimmedJets"),
    electronInput=cms.InputTag("slimmedElectrons"),
    muonInput=cms.InputTag("slimmedMuons"),
    HLTInput=cms.InputTag('TriggerResults', '', 'HLT'),
    VertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),

    # Lepton cuts
    minSignalElectronPt=cms.double(30.),
    maxSignalElectronEta=cms.double(2.5),
    signalElectronIDCriteria=cms.string('cutBasedElectronID-CSA14-PU20bx25-V0-standalone-tight'),
    minSignalElectronID=cms.double(0),
    minLooseMuonPt=cms.double(10.),
    maxLooseMuonEta=cms.double(2.5),
    minLooseElectronPt=cms.double(20.),
    maxLooseElectronEta=cms.double(2.5),
    looseElectronIDCriteria=cms.string('cutBasedElectronID-CSA14-PU20bx25-V0-standalone-veto'),
    minLooseElectronID=cms.double(0),

    #jet cuts
    min1JetPt=cms.double(30.),
    min2JetPt=cms.double(30.),
    min3JetPt=cms.double(30.),
    min4JetPt=cms.double(30.),
    minBJetPt=cms.double(30.),
    minJetPtInNtuples=cms.double(25.),
    
    # Jet cleaning delta R
    cleaningDeltaR=cms.double(0.3),

    # Apply different JEC
    applyJEC = cms.bool(True),
    JetCorrectionService = cms.string('ak4PFCHSL1FastL2L3'),  

    # B Jet Selection
    # Working points taken from https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagging#Preliminary_working_or_operating
    bJetDiscriminator=cms.string('combinedInclusiveSecondaryVertexV2BJetTags'),
    minBJetDiscriminator=cms.double(0.814),

    controlElectronIsolation=cms.double(0.21), # endcap iso is <0.2075, so tightened this from >0.2 to >0.21
   
    prefix=cms.untracked.string('TopPairElectronPlusJetsSelection.'),
    MCSampleTag = cms.string('Summer12'),#Fall11 or Summer12 or Summer11Leg

    #flags
    debug=cms.untracked.bool(False),
    taggingMode=cms.bool(False),

    tagAndProbeStudies = cms.bool(False),
    dropTriggerSelection = cms.bool(False),
    jetSelectionInTaggingMode = cms.bool(False),
    bSelectionInTaggingMode = cms.bool(False),
    nonIsolatedElectronSelection = cms.bool(False),
    invertedConversionSelection = cms.bool(False),
)


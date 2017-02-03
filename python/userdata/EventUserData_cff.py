import FWCore.ParameterSet.Config as cms

from BristolAnalysis.NTupleTools.userdata.EventUserData_cfi import eventUserData

# electron signal selection
eventUserDataTopPairElectronPlusJetsSelection = eventUserData.clone()
# electron main QCD control region
eventUserDataTopPairElectronPlusJetsConversionSelection = eventUserData.clone(
    prefix='TopPairElectronPlusJetsConversionSelection.',
    electronCollection='goodConversionElectrons',
    jetCollection='goodJetsEConversionRegion',
    bJetCollection='goodBJetsEConversionRegion',
)
# electron secondary QCD control region
eventUserDataTopPairElectronPlusJetsNonIsoSelection = eventUserData.clone(
    prefix='TopPairElectronPlusJetsQCDSelection.',
    electronCollection='goodNonIsoElectrons',
    jetCollection='goodJetsENonIsoRegion',
    bJetCollection='goodBJetsENonIsoRegion',
)

# muon signal selection
eventUserDataTopPairMuonPlusJetsSelection = eventUserData.clone(
    prefix='TopPairMuonPlusJetsSelection.',
    isElectron=False
)
# muon main QCD control region
eventUserDataTopPairMuonPlusJetsQCD1Selection = eventUserData.clone(
    prefix='TopPairMuonPlusJetsQCDSelection3toInf.',
    muonCollection='goodNonIsoR1Muons',
    jetCollection='goodJetsMuNonIsoR1Region',
    bJetCollection='goodBJetsMuNonIsoR1Region',
)
# muon secondary QCD control region
eventUserDataTopPairMuonPlusJetsQCD2Selection = eventUserData.clone(
    prefix='TopPairMuonPlusJetsQCDSelection1p5to3.',
    muonCollection='goodNonIsoR2Muons',
    jetCollection='goodJetsMuNonIsoR2Region',
    bJetCollection='goodBJetsMuNonIsoR2Region',
)

eventUserDataSequence = cms.Sequence(
    # electrons
    eventUserDataTopPairElectronPlusJetsSelection +
    eventUserDataTopPairElectronPlusJetsConversionSelection +
    eventUserDataTopPairElectronPlusJetsNonIsoSelection +
    # muons
    eventUserDataTopPairMuonPlusJetsSelection +
    eventUserDataTopPairMuonPlusJetsQCD1Selection +
    eventUserDataTopPairMuonPlusJetsQCD2Selection
)

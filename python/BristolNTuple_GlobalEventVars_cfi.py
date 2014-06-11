import FWCore.ParameterSet.Config as cms

rootTupleGlobalEventVars = cms.EDProducer('BristolNTuple_GlobalEventVars',
    jetInputTag=cms.InputTag('topPairEPlusJetsSelection', 'TopPairElectronPlusJetsSelection.cleanedJets'),
    signalLeptonInputTag=cms.InputTag('topPairEPlusJetsSelection', 'TopPairElectronPlusJetsSelection.signalElectron'),
    signalLeptonIndexInputTag=cms.InputTag('topPairEPlusJetsSelection', 'TopPairElectronPlusJetsSelection.signalElectronIndex'),
    metInputTag=cms.InputTag('patMETsPFlow'),
    Prefix=cms.string('Event.'),
    Suffix=cms.string(''),
    Channel=cms.string('EPlusJets')
)

import FWCore.ParameterSet.Config as cms

rootTupleGlobalEventVars = cms.EDProducer('BristolNTuple_GlobalEventVars',
    jetInputTag=cms.InputTag('topPairEPlusJetsSelection', 'TopPairElectronPlusJets2012Selection.cleanedJets'),
    signalLeptonInputTag=cms.InputTag('topPairEPlusJetsSelection', 'TopPairElectronPlusJets2012Selection.signalElectron'),
    metInputTag=cms.InputTag('patMETsPFlow'),
    Prefix=cms.string('recoGlobalEventVars.'),
    Suffix=cms.string(''),
    Channel=cms.string('EPlusJets')
)

import FWCore.ParameterSet.Config as cms

variableProducer = cms.EDProducer(
    'VariableProducer',
    cleanedJets=cms.InputTag('goodJets'),
    cleanedBJets=cms.InputTag('goodBJets'),
    signalElectrons=cms.InputTag('goodElectrons'),
    signalMuons=cms.InputTag('goodMuons'),
    met=cms.InputTag('slimmedMETs'),
    minJetPtForHT=cms.double(20.),
    channel=cms.string('electron'),
    prefix=cms.string('prefix.'),
    suffix=cms.string(''),
)

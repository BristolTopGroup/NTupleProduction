import FWCore.ParameterSet.Config as cms

genLeptonFilter = cms.EDFilter('GenLeptonFilter',
    particleLevelLeptonSelectionInput = cms.InputTag('pseudoTop','leptons','Ntuples'),
    Prefix               = cms.string('Event.'),
    minPt = cms.double(20),
    maxAbsoluteEta = cms.double(2.4),
)


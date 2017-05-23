import FWCore.ParameterSet.Config as cms

nTupleTrigger = cms.EDProducer("BristolNTuple_Trigger",
    HLTInputTag = cms.InputTag('TriggerResults','','HLT'),
    HLTObjectsInputTag = cms.InputTag('selectedPatTrigger'),
    Prefix=cms.string('nTupleTrigger.'),
    Suffix=cms.string(''),
    PathOfInterest = cms.string(''),
    tightenTrigger = cms.bool(False),
    hltFilter = cms.string(''),
    cut = cms.string(''),
    minNumber = cms.uint32(0)
)

# ------ 2016 ReReco ------ #
# Data
# Electron
nTupleTriggerEle32erWPTightGsf = nTupleTrigger.clone( Prefix='HLTEle32erWPTightGsf.', PathOfInterest='HLT_Ele32_eta2p1_WPTight_Gsf_v')
# Muon
nTupleTriggerIsoMu24 = nTupleTrigger.clone( Prefix='HLTIsoMu24.', PathOfInterest='HLT_IsoMu24_v')
nTupleTriggerIsoTkMu24 = nTupleTrigger.clone( Prefix='HLTIsoTkMu24.', PathOfInterest='HLT_IsoTkMu24_v')
# MC
# Electron
nTupleTriggerEle32erWPTightGsfMC = nTupleTrigger.clone( Prefix='HLTEle32erWPTightGsfMC.', PathOfInterest='HLT_Ele32_eta2p1_WPTight_Gsf_v')
# Muon
nTupleTriggerIsoMu24MC = nTupleTrigger.clone( Prefix='HLTIsoMu24MC.', PathOfInterest='HLT_IsoMu24_v')
nTupleTriggerIsoTkMu24MC = nTupleTrigger.clone( Prefix='HLTIsoTkMu24MC.', PathOfInterest='HLT_IsoTkMu24_v')

triggerSequence = cms.Sequence(
    nTupleTriggerEle32erWPTightGsf *
    nTupleTriggerIsoMu24 *
    nTupleTriggerIsoTkMu24 *

    nTupleTriggerEle32erWPTightGsfMC *
    nTupleTriggerIsoMu24MC *
    nTupleTriggerIsoTkMu24MC
)

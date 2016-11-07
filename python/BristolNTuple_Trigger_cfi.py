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

# ------ 2015 ReReco ------ #
# Data
# Electron
nTupleTriggerEle23WPLooseGsf = nTupleTrigger.clone( Prefix='HLTEle23WPLooseGsf.', PathOfInterest='HLT_Ele23_WPLoose_Gsf_v')
# Muon
nTupleTriggerIsoMu20 = nTupleTrigger.clone( Prefix='HLTIsoMu20.', PathOfInterest='HLT_IsoMu20_v')
nTupleTriggerIsoTkMu20 = nTupleTrigger.clone( Prefix='HLTIsoTkMu20.', PathOfInterest='HLT_IsoTkMu20_v')
# MC
# Electron
nTupleTriggerEle23WPLooseGsfMC = nTupleTrigger.clone( Prefix='HLTEle23WPLooseGsfMC.', PathOfInterest='HLT_Ele23_WPLoose_Gsf_v')
# Muon
nTupleTriggerIsoMu20MC = nTupleTrigger.clone( Prefix='HLTIsoMu20MC.', PathOfInterest='HLT_IsoMu20_v')
nTupleTriggerIsoTkMu20MC = nTupleTrigger.clone( Prefix='HLTIsoTkMu20MC.', PathOfInterest='HLT_IsoTkMu20_v')

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

triggerSequence2015 = cms.Sequence(
    nTupleTriggerEle23WPLooseGsf *
    nTupleTriggerIsoMu20 *
    nTupleTriggerIsoTkMu20 *

    nTupleTriggerEle23WPLooseGsfMC *
    nTupleTriggerIsoMu20MC *
    nTupleTriggerIsoTkMu20MC
)

triggerSequence2016 = cms.Sequence(
    nTupleTriggerEle32erWPTightGsf *
    nTupleTriggerIsoMu24 *
    nTupleTriggerIsoTkMu24 *

    nTupleTriggerEle32erWPTightGsfMC *
    nTupleTriggerIsoMu24MC *
    nTupleTriggerIsoTkMu24MC
)

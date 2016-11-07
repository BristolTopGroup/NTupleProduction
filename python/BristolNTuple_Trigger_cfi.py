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
nTupleTriggerEle27WPTightGsf = nTupleTrigger.clone( Prefix='HLTEle27WPTightGsf.', PathOfInterest='HLT_Ele27_WPTight_Gsf_v')
# Muon
nTupleTriggerIsoMu24 = nTupleTrigger.clone( Prefix='HLTIsoMu24.', PathOfInterest='HLT_IsoMu24_v')
nTupleTriggerIsoTkMu24 = nTupleTrigger.clone( Prefix='HLTIsoTkMu24.', PathOfInterest='HLT_IsoTkMu24_v')
# MC
# Electron
nTupleTriggerEle27WPTightGsfMC = nTupleTrigger.clone( Prefix='HLTEle27WPTightGsfMC.', PathOfInterest='HLT_Ele27_WPTight_Gsf_v')
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
    nTupleTriggerEle27WPTightGsf *
    nTupleTriggerIsoMu24 *
    nTupleTriggerIsoTkMu24 *

    nTupleTriggerEle27WPTightGsfMC *
    nTupleTriggerIsoMu24MC *
    nTupleTriggerIsoTkMu24MC
)

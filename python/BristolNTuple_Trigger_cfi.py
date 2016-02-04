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

# RunD 25ns
# Data
# Electron
nTupleTriggerEle22erWPLooseGsf = nTupleTrigger.clone( Prefix='HLTEle22erWPLooseGsf.', PathOfInterest='HLT_Ele22_eta2p1_WPLoose_Gsf_v')

# Muon
nTupleTriggerIsoMu20 = nTupleTrigger.clone( Prefix='HLTIsoMu20.', PathOfInterest='HLT_IsoMu20_v')
nTupleTriggerIsoTkMu20 = nTupleTrigger.clone( Prefix='HLTIsoTkMu20.', PathOfInterest='HLT_IsoTkMu20_v')

# MC
# Electron
nTupleTriggerEle22erWPLooseGsfMC = nTupleTrigger.clone( Prefix='HLTEle22erWPLooseGsfMC.', PathOfInterest='HLT_Ele22_eta2p1_WPLoose_Gsf_v')

# Muon
nTupleTriggerIsoMu20MC = nTupleTrigger.clone( Prefix='HLTIsoMu20MC.', PathOfInterest='HLT_IsoMu20_v')
nTupleTriggerIsoTkMu20MC = nTupleTrigger.clone( Prefix='HLTIsoTkMu20MC.', PathOfInterest='HLT_IsoTkMu20_v')

triggerSequence = cms.Sequence(
    
    # RunII 25ns
    nTupleTriggerEle22erWPLooseGsf *
    nTupleTriggerIsoMu20 *
    nTupleTriggerIsoTkMu20 *

    nTupleTriggerEle22erWPLooseGsfMC *
    nTupleTriggerIsoMu20MC *
    nTupleTriggerIsoTkMu20MC 
)


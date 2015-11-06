import FWCore.ParameterSet.Config as cms

nTupleTrigger = cms.EDProducer("BristolNTuple_Trigger",
    HLTInputTag = cms.InputTag('TriggerResults','','HLT'),
    HLTObjectsInputTag = cms.InputTag('selectedPatTrigger'),
    Prefix=cms.string('nTupleTrigger.'),
    Suffix=cms.string(''),
    PathOfInterest = cms.string(''),
)

# RunD 25ns
# Data
nTupleTriggerEle27erWPLooseGsf = nTupleTrigger.clone( Prefix='HLTEle27erWPLooseGsf.', PathOfInterest='HLT_Ele27_eta2p1_WPLoose_Gsf_v')
# nTupleTriggerIsoMu18 = nTupleTrigger.clone( Prefix='HLTIsoMu18.', PathOfInterest='HLT_IsoMu18_v')
nTupleTriggerIsoMu20 = nTupleTrigger.clone( Prefix='HLTIsoMu20.', PathOfInterest='HLT_IsoMu20_v')
nTupleTriggerIsoTkMu20 = nTupleTrigger.clone( Prefix='HLTIsoTkMu20.', PathOfInterest='HLT_IsoTkMu20_v')

# MC
nTupleTriggerEle27erWP75GsfMC = nTupleTrigger.clone( Prefix='HLTEle27erWP75GsfMC.', PathOfInterest='HLT_Ele27_eta2p1_WP75_Gsf_v')
nTupleTriggerIsoMu20MC = nTupleTrigger.clone( Prefix='HLTIsoMu20MC.', PathOfInterest='HLT_IsoMu20_v')
nTupleTriggerIsoTkMu20MC = nTupleTrigger.clone( Prefix='HLTIsoTkMu20MC.', PathOfInterest='HLT_IsoTkMu20_v')



triggerSequence = cms.Sequence(

    # RunII 25ns
    nTupleTriggerEle27erWPLooseGsf *
    nTupleTriggerIsoMu20 *
    nTupleTriggerIsoTkMu20 *

    nTupleTriggerEle27erWP75GsfMC *
    nTupleTriggerIsoMu20MC *
    nTupleTriggerIsoTkMu20MC 
)




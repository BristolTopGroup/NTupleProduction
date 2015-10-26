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
nTupleTriggerEle23WPLooseGsf = nTupleTrigger.clone( Prefix='HLTEle23WPLooseGsf.', PathOfInterest='HLT_Ele23_WPLoose_Gsf_v')
nTupleTriggerIsoMu18 = nTupleTrigger.clone( Prefix='HLTIsoMu18.', PathOfInterest='HLT_IsoMu18_v')

# MC
nTupleTriggerEle27WP75GsfMC = nTupleTrigger.clone( Prefix='HLTEle27WP75GsfMC.', PathOfInterest='HLT_Ele27_eta2p1_WP75_Gsf_v')
nTupleTriggerIsoMu20erMC = nTupleTrigger.clone( Prefix='HLTIsoMu20erMC.', PathOfInterest='HLT_IsoMu20_eta2p1_v')



triggerSequence = cms.Sequence(

    # RunII 25ns
    nTupleTriggerEle23WPLooseGsf *
    nTupleTriggerIsoMu18 *

    nTupleTriggerEle27WP75GsfMC *
    nTupleTriggerIsoMu20erMC 
)




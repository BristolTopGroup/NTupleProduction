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
nTupleTriggerEle27erWPLooseGsf = nTupleTrigger.clone( Prefix='HLTEle27erWPLooseGsf.', PathOfInterest='HLT_Ele27_eta2p1_WPLoose_Gsf_v')
nTupleTriggerEle23erWPLooseGsf = nTupleTrigger.clone( Prefix='HLTEle23erWPLooseGsf.', PathOfInterest='HLT_Ele23_WPLoose_Gsf_v', tightenTrigger = True, hltFilter = 'hltEle23WPLooseGsfTrackIsoFilter', cut = 'eta > -2.1 && eta < 2.1', minNumber = 1 )

# Muon

nTupleTriggerIsoMu18er = nTupleTrigger.clone( Prefix='HLTIsoMu18er.', PathOfInterest='HLT_IsoMu18_v', tightenTrigger = True, hltFilter = 'hltL3crIsoL1sMu16L1f0L2f10QL3f18QL3trkIsoFiltered0p09', cut = 'eta > -2.1 && eta < 2.1', minNumber = 1 )
nTupleTriggerIsoMu20 = nTupleTrigger.clone( Prefix='HLTIsoMu20.', PathOfInterest='HLT_IsoMu20_v')
nTupleTriggerIsoTkMu20 = nTupleTrigger.clone( Prefix='HLTIsoTkMu20.', PathOfInterest='HLT_IsoTkMu20_v')

# MC
nTupleTriggerEle27erWP75GsfMC = nTupleTrigger.clone( Prefix='HLTEle27erWP75GsfMC.', PathOfInterest='HLT_Ele27_eta2p1_WP75_Gsf_v')
nTupleTriggerEle23erWP75GsfMC = nTupleTrigger.clone( Prefix='HLTEle23erWP75GsfMC.', PathOfInterest='HLT_Ele22_eta2p1_WP75_Gsf_v', tightenTrigger = True, hltFilter = 'hltSingleEle22WP75GsfTrackIsoFilter', cut = 'pt > 23', minNumber = 1 )
# nTupleTriggerEle23erWP75GsfMC = nTupleTrigger.clone( Prefix='HLTEle23erWP75GsfMC.', PathOfInterest='HLT_Ele22_eta2p1_WP75_Gsf_v' )

nTupleTriggerIsoMu18erMC = nTupleTrigger.clone( Prefix='HLTIsoMu18erMC.', PathOfInterest='HLT_IsoMu17_eta2p1_v', tightenTrigger = True, hltFilter = 'hltL3crIsoL1sSingleMu16erL1f0L2f10QL3f17QL3trkIsoFiltered0p09', cut = 'pt > 18', minNumber = 1 )
nTupleTriggerIsoMu20MC = nTupleTrigger.clone( Prefix='HLTIsoMu20MC.', PathOfInterest='HLT_IsoMu20_v')
nTupleTriggerIsoTkMu20MC = nTupleTrigger.clone( Prefix='HLTIsoTkMu20MC.', PathOfInterest='HLT_IsoTkMu20_v')



triggerSequence = cms.Sequence(
    
    # RunII 25ns
    nTupleTriggerEle23erWPLooseGsf *
    nTupleTriggerEle27erWPLooseGsf *
    nTupleTriggerIsoMu18er *
    nTupleTriggerIsoMu20 *
    nTupleTriggerIsoTkMu20 *

    nTupleTriggerEle27erWP75GsfMC *
    nTupleTriggerEle23erWP75GsfMC *
    nTupleTriggerIsoMu18erMC *
    nTupleTriggerIsoMu20MC *
    nTupleTriggerIsoTkMu20MC 
)




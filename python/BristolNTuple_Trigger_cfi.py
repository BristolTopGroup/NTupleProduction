import FWCore.ParameterSet.Config as cms

nTupleTrigger = cms.EDProducer("BristolNTuple_Trigger",
    HLTInputTag = cms.InputTag('TriggerResults','','HLT'),
    HLTObjectsInputTag = cms.InputTag('selectedPatTrigger'),
    Prefix=cms.string('nTupleTrigger.'),
    Suffix=cms.string(''),

    PathOfInterest = cms.string('HLT_IsoMu20_eta2p1_v')

)

# Top Phys14 Triggers
# nTupleTriggerEle32eta2p1WP85Gsf = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP85Gsf.', PathOfInterest='HLT_Ele32_eta2p1_WP85_Gsf_v')
# nTupleTriggerEle32eta2p1WP85GsfCentralPFJet30BTagCSV = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP85GsfCentralPFJet30BTagCSV.', PathOfInterest='HLT_Ele32_eta2p1_WP85_Gsf_CentralPFJet30_BTagCSV_v')
# nTupleTriggerEle32eta2p1WP85GsfTriCentralPFJet40 = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP85GsfTriCentralPFJet40.', PathOfInterest='HLT_Ele32_eta2p1_WP85_Gsf_TriCentralPFJet40_v')
# nTupleTriggerEle32eta2p1WP85GsfTriCentralPFJet605035 = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP85GsfTriCentralPFJet605035.', PathOfInterest='HLT_Ele32_eta2p1_WP85_Gsf_TriCentralPFJet60_50_35_v')

# nTupleTriggerIsoMu24eta2p1IterTrk02 = nTupleTrigger.clone( Prefix='HLTIsoMu24eta2p1IterTrk02.', PathOfInterest='IsoMu24_eta2p1_IterTrk02')

# Top 74X MC Triggers
# 50 ns
nTupleTriggerEle27WPTightGsf = nTupleTrigger.clone( Prefix='HLTEle27WPTightGsf.', PathOfInterest='HLT_Ele27_eta2p1_WPTight_Gsf_v')
nTupleTriggerEle27WPLooseGsf = nTupleTrigger.clone( Prefix='HLTEle27WPLooseGsf.', PathOfInterest='HLT_Ele27_eta2p1_WPLoose_Gsf_v')
nTupleTriggerEle27WP75GsfMC = nTupleTrigger.clone( Prefix='HLTEle27WP75GsfMC.', PathOfInterest='HLT_Ele27_eta2p1_WP75_Gsf_v')


# 25ns
# nTupleTriggerEle32eta2p1WP75Gsf = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP75Gsf.', PathOfInterest='HLT_Ele32_eta2p1_WP75_Gsf_v')
# nTupleTriggerEle27eta2p1WP85GsfHT200 = nTupleTrigger.clone( Prefix='HLTEle27eta2p1WP85GsfHT200.', PathOfInterest='HLT_Ele27_eta2p1_WP85_Gsf_HT200_v')
# nTupleTriggerEle27eta2p1WP75GsfTriCentralPFJet30 = nTupleTrigger.clone( Prefix='HLTEle27eta2p1WP75GsfTriCentralPFJet30.', PathOfInterest='HLT_Ele27_eta2p1_WP75_Gsf_TriCentralPFJet30_v')
# nTupleTriggerEle27eta2p1WP75GsfTriCentralPFJet504030 = nTupleTrigger.clone( Prefix='HLTEle27eta2p1WP75GsfTriCentralPFJet504030.', PathOfInterest='HLT_Ele27_eta2p1_WP75_Gsf_TriCentralPFJet50_40_30_v')


nTupleTriggerIsoMu24eta2p1 = nTupleTrigger.clone( Prefix='HLTIsoMu24eta2p1.', PathOfInterest='HLT_IsoMu24_eta2p1_v')
nTupleTriggerIsoMu20eta2p1 = nTupleTrigger.clone( Prefix='HLTIsoMu20eta2p1.', PathOfInterest='HLT_IsoMu20_eta2p1_v')
nTupleTriggerIsoTkMu20eta2p1 = nTupleTrigger.clone( Prefix='HLTIsoTkMu20eta2p1.', PathOfInterest='HLT_IsoTkMu20_eta2p1_v')
nTupleTriggerIsoMu24eta2p1MC = nTupleTrigger.clone( Prefix='HLTIsoMu24eta2p1MC.', PathOfInterest='HLT_IsoMu24_eta2p1_v')
nTupleTriggerIsoTkMu20eta2p1MC = nTupleTrigger.clone( Prefix='HLTIsoTkMu20eta2p1MC.', PathOfInterest='HLT_IsoTkMu20_eta2p1_v')
nTupleTriggerIsoMu20eta2p1MC = nTupleTrigger.clone( Prefix='HLTIsoMu20eta2p1MC.', PathOfInterest='HLT_IsoMu20_eta2p1_v')

triggerSequence = cms.Sequence(
    # nTupleTriggerEle32eta2p1WP85Gsf *
    # nTupleTriggerEle32eta2p1WP85GsfCentralPFJet30BTagCSV *
    # nTupleTriggerEle32eta2p1WP85GsfTriCentralPFJet40 *
    # nTupleTriggerEle32eta2p1WP85GsfTriCentralPFJet605035 *
    # nTupleTriggerIsoMu24eta2p1IterTrk02 *

    # nTupleTriggerEle32eta2p1WP75Gsf *
    # nTupleTriggerEle27eta2p1WP85GsfHT200 *
    # nTupleTriggerEle27eta2p1WP75GsfTriCentralPFJet30 *
    # nTupleTriggerEle27eta2p1WP75GsfTriCentralPFJet504030 *
    nTupleTriggerIsoMu24eta2p1 *
    nTupleTriggerIsoMu20eta2p1 *
    nTupleTriggerIsoTkMu20eta2p1 *
    nTupleTriggerEle27WPLooseGsf *
    nTupleTriggerEle27WPTightGsf *

    nTupleTriggerIsoMu24eta2p1MC *
    nTupleTriggerIsoMu20eta2p1MC *
    nTupleTriggerIsoTkMu20eta2p1MC *
    nTupleTriggerEle27WP75GsfMC
    )

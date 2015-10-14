import FWCore.ParameterSet.Config as cms

nTupleTrigger = cms.EDProducer("BristolNTuple_Trigger",
    HLTInputTag = cms.InputTag('TriggerResults','','HLT'),
    HLTObjectsInputTag = cms.InputTag('selectedPatTrigger'),
    Prefix=cms.string('nTupleTrigger.'),
    Suffix=cms.string(''),
    PathOfInterest = cms.string(''),
)

# Top Phys14 Triggers
# nTupleTriggerEle32eta2p1WP85Gsf = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP85Gsf.', PathOfInterest='HLT_Ele32_eta2p1_WP85_Gsf_v')
# nTupleTriggerEle32eta2p1WP85GsfCentralPFJet30BTagCSV = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP85GsfCentralPFJet30BTagCSV.', PathOfInterest='HLT_Ele32_eta2p1_WP85_Gsf_CentralPFJet30_BTagCSV_v')
# nTupleTriggerEle32eta2p1WP85GsfTriCentralPFJet40 = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP85GsfTriCentralPFJet40.', PathOfInterest='HLT_Ele32_eta2p1_WP85_Gsf_TriCentralPFJet40_v')
# nTupleTriggerEle32eta2p1WP85GsfTriCentralPFJet605035 = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP85GsfTriCentralPFJet605035.', PathOfInterest='HLT_Ele32_eta2p1_WP85_Gsf_TriCentralPFJet60_50_35_v')

# nTupleTriggerIsoMu24eta2p1IterTrk02 = nTupleTrigger.clone( Prefix='HLTIsoMu24eta2p1IterTrk02.', PathOfInterest='IsoMu24_eta2p1_IterTrk02')



# Top 74X MC Triggers

# # 50 ns
# # Data
# nTupleTriggerEle27WPLooseGsf = nTupleTrigger.clone( Prefix='HLTEle27WPLooseGsf.', PathOfInterest='HLT_Ele27_WPLoose_Gsf_v')
# nTupleTriggerIsoMu20er = nTupleTrigger.clone( Prefix='HLTIsoMu20er.', PathOfInterest='HLT_IsoMu20_eta2p1_v')

# # MC
# nTupleTriggerIsoMu20erMC = nTupleTrigger.clone( Prefix='HLTIsoMu20erMC.', PathOfInterest='HLT_IsoMu20_eta2p1_v')
# nTupleTriggerEle23WP75GsfMC = nTupleTrigger.clone( Prefix='HLTEle23WP75GsfMC.', PathOfInterest='HLT_Ele23_eta2p1_WP75_Gsf_v')


# 25ns
# Data
nTupleTriggerEle23WPLooseGsf = nTupleTrigger.clone( Prefix='HLTEle23WPLooseGsf.', PathOfInterest='HLT_Ele23_WPLoose_Gsf_v')
nTupleTriggerIsoMu18 = nTupleTrigger.clone( Prefix='HLTIsoMu18.', PathOfInterest='HLT_IsoMu18_v')

# MC
nTupleTriggerEle27WP75GsfMC = nTupleTrigger.clone( Prefix='HLTEle27WP75GsfMC.', PathOfInterest='HLT_Ele27_eta2p1_WP75_Gsf_v')
nTupleTriggerIsoMu20erMC = nTupleTrigger.clone( Prefix='HLTIsoMu20erMC.', PathOfInterest='HLT_IsoMu20_eta2p1_v')



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

    # # RunII 50ns
    # nTupleTriggerEle27WPLooseGsf *
    # nTupleTriggerIsoMu20er *

    # nTupleTriggerEle23WP75GsfMC *
    # nTupleTriggerIsoMu20erMC *

    # RunII 25ns
    nTupleTriggerEle23WPLooseGsf *
    nTupleTriggerIsoMu18 *

    nTupleTriggerEle27WP75GsfMC *
    nTupleTriggerIsoMu20erMC 
)




import FWCore.ParameterSet.Config as cms

nTupleTrigger = cms.EDProducer("BristolNTuple_Trigger",
    HLTInputTag = cms.InputTag('TriggerResults','','HLT'),
    HLTObjectsInputTag = cms.InputTag('selectedPatTrigger'),
    Prefix=cms.string('HLTIsoMu20eta2p1.'),
    Suffix=cms.string(''),

    PathOfInterest = cms.string('HLT_IsoMu20_eta2p1_v')

)

# Top Phys14 Triggers
nTupleTriggerEle32eta2p1WP85Gsf = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP85Gsf.', PathOfInterest='HLT_Ele32_eta2p1_WP85_Gsf_v')
nTupleTriggerEle32eta2p1WP85GsfCentralPFJet30BTagCSV = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP85GsfCentralPFJet30BTagCSV.', PathOfInterest='HLT_Ele32_eta2p1_WP85_Gsf_CentralPFJet30_BTagCSV_v')
nTupleTriggerEle32eta2p1WP85GsfTriCentralPFJet40 = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP85GsfTriCentralPFJet40.', PathOfInterest='HLT_Ele32_eta2p1_WP85_Gsf_TriCentralPFJet40_v')
nTupleTriggerEle32eta2p1WP85GsfTriCentralPFJet605035 = nTupleTrigger.clone( Prefix='HLTEle32eta2p1WP85GsfTriCentralPFJet605035.', PathOfInterest='HLT_Ele32_eta2p1_WP85_Gsf_TriCentralPFJet60_50_35_v')

nTupleTriggerIsoMu24eta2p1IterTrk02 = nTupleTrigger.clone( Prefix='HLTIsoMu24eta2p1IterTrk02.', PathOfInterest='IsoMu24_eta2p1_IterTrk02')


triggerSequence = cms.Sequence(
    nTupleTriggerEle32eta2p1WP85Gsf *
    nTupleTriggerEle32eta2p1WP85GsfCentralPFJet30BTagCSV *
    nTupleTriggerEle32eta2p1WP85GsfTriCentralPFJet40 *
    nTupleTriggerEle32eta2p1WP85GsfTriCentralPFJet605035 *
    nTupleTriggerIsoMu24eta2p1IterTrk02 
)

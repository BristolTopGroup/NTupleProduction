# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

#this has to run AFTER setup_PF2PAT
def setup_jets(process, cms, useData, postfix="PFlow"):
    print '=' * 60
    print "Setting up Jets"
    print '=' * 60
    #MC setup
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])
    caloJetCorrection = ('AK5Calo', ['L1Offset' , 'L2Relative', 'L3Absolute'])
    
    if useData :#data set up
        inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
        caloJetCorrection = ('AK5Calo', ['L1Offset' , 'L2Relative', 'L3Absolute', 'L2L3Residual'])   
         
    print 'Using jet energy corrections: '
    print 'Calo Jets'
    print caloJetCorrection
    print 'PF Jets'
    print inputJetCorrLabel
    
    process.patJetCorrFactorsPFlow.payload = inputJetCorrLabel[0]
    process.patJetCorrFactorsPFlow.levels = inputJetCorrLabel[1]
    
    ###############################
    ########## Gen Setup ##########
    ###############################

    process.load("RecoJets.Configuration.GenJetParticles_cff")
    from RecoJets.JetProducers.ca4GenJets_cfi import ca4GenJets
    process.ca8GenJetsNoNu = ca4GenJets.clone(rParam=cms.double(0.8),
                                           src=cms.InputTag("genParticlesForJetsNoNu"))
        
    ###############################
    #### Jet RECO includes ########
    ###############################

    from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
    from RecoJets.JetProducers.PFJetParameters_cfi import *
    from RecoJets.JetProducers.CaloJetParameters_cfi import *
    from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
    #from RecoJets.JetProducers.CATopJetParameters_cfi import *
    from RecoJets.JetProducers.GenJetParameters_cfi import *

    ###############################
    #### Calo Jet Setup    ########
    ###############################
    #this has to run after PF2PAT and before removeMCMatching
    #see https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookPAT38xChanges#Details_with_PF2PAT
    from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection, addJetCollection
#    print 'adding calo jets'
    switchJetCollection(process,
                     jetCollection=cms.InputTag('ak5CaloJets'),
                     jetCorrLabel=caloJetCorrection,
                     doBTagging=True,
                     doType1MET=False,)
    
    
    ###############################
    ###### Bare KT 0.6 jets #######
    ###############################

    from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets

    process.kt6PFJets = kt4PFJets.clone(
                                        rParam=cms.double(0.6),
                                        doAreaFastjet=cms.bool(True),
                                        doRhoFastjet=cms.bool(True)
    )
    process.kt6PFJetsPFlow = kt4PFJets.clone(
                                             rParam=cms.double(0.6),
                                             src=cms.InputTag('pfNoElectron' + postfix),
                                             doAreaFastjet=cms.bool(True),
                                             doRhoFastjet=cms.bool(True)
    )
    process.kt4PFJetsPFlow = kt4PFJets.clone(
                                             rParam=cms.double(0.4),
                                             src=cms.InputTag('pfNoElectron' + postfix),
                                             doAreaFastjet=cms.bool(True),
                                             doRhoFastjet=cms.bool(True)
    )


    ###############################
    ###### Bare CA 0.8 jets #######
    ###############################
    from RecoJets.JetProducers.ca4PFJets_cfi import ca4PFJets
    process.ca8PFJetsPFlow = ca4PFJets.clone(
                                             rParam=cms.double(0.8),
                                             src=cms.InputTag('pfNoElectron' + postfix),
                                             doAreaFastjet=cms.bool(True),
                                             doRhoFastjet=cms.bool(True),
                                             Rho_EtaMax=cms.double(6.0),
                                             Ghost_EtaMax=cms.double(7.0)
    )
    
    addJetCollection(process,
                 cms.InputTag('ca8PFJetsPFlow'), # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'CA8', 'PF',
                 doJTA=True, # Run Jet-Track association & JetCharge
                 doBTagging=True, # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection=cms.InputTag("ca8GenJetsNoNu"),
                 doJetID=False
                 )


    process.patJetCorrFactorsCA8PF.rho = cms.InputTag("kt6PFJetsPFlow", "rho")
    
    ###############################
    ### TagInfo and Matching Setup#
    ###############################
    
    # Do some configuration of the jet substructure things
    for jetcoll in (process.patJetsPFlow,
                    process.patJetsCA8PF
                    ) :
        if useData == False :
            jetcoll.embedGenJetMatch = True
            jetcoll.getJetMCFlavour = True
            jetcoll.addGenPartonMatch = True
        # Add CATopTag info... piggy-backing on b-tag functionality
        jetcoll.addBTagInfo = True
        jetcoll.embedCaloTowers = True
        jetcoll.embedPFCandidates = True
        
    additionalJets = [getattr(process, "kt6PFJets"),
                      getattr(process, "kt6PFJets" + postfix),
                      getattr(process, "kt4PFJets" + postfix),
                      getattr(process, "ca8PFJets" + postfix)]
    pfNoElectron = getattr(process, "pfNoElectron" + postfix)
    for module in additionalJets :
        getattr(process, "patPF2PATSequence" + postfix).replace(pfNoElectron, pfNoElectron * module)

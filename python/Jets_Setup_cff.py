# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.CaloJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *

#this has to run AFTER setup_PF2PAT
def setup_jets(process, cms, options, postfix="PFlow"):
    print '=' * 60
    print "Setting up Jets"
    print '=' * 60
    #MC setup
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])
    caloJetCorrection = ('AK5Calo', ['L1Offset' , 'L2Relative', 'L3Absolute'])
    
    if options.useData :#data set up
        inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
        caloJetCorrection = ('AK5Calo', ['L1Offset' , 'L2Relative', 'L3Absolute', 'L2L3Residual'])   
         
    print 'Using jet energy corrections: '
    print 'Calo Jets'
    print caloJetCorrection
    print 'PF Jets'
    print inputJetCorrLabel

    if options.CMSSW == '44X':
        process.patJetCorrFactorsPFlow.payload = inputJetCorrLabel[0]
        process.patJetCorrFactorsPFlow.levels = inputJetCorrLabel[1]
        process.patJetCorrFactorsPFlow.rho = cms.InputTag("kt6PFJets", "rho")

    #lots of stuff down here is obsolete for 52x - need to clean up
    
    ###############################
    #### Jet RECO includes ########
    ###############################

    from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
    

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
    ### TagInfo and Matching Setup#
    ###############################
    
    # Do some configuration of the jet substructure things
    for jetcoll in [process.patJetsPFlow] :
        if options.useData == False :
            jetcoll.embedGenJetMatch = True
            jetcoll.getJetMCFlavour = True
            jetcoll.addGenPartonMatch = True
        # Add CATopTag info... piggy-backing on b-tag functionality
        jetcoll.addBTagInfo = True
        jetcoll.embedCaloTowers = True
        jetcoll.embedPFCandidates = True
        
    additionalJets = [getattr(process, "kt6PFJets"),
                      getattr(process, "kt6PFJets" + postfix),
                      getattr(process, "kt4PFJets" + postfix)]
    pfNoElectron = getattr(process, "pfNoElectron" + postfix)
    for module in additionalJets :
        getattr(process, "patPF2PATSequence" + postfix).replace(pfNoElectron, pfNoElectron * module)

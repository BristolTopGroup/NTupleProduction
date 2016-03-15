# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.CaloJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *

# this has to run AFTER setup_PF2PAT


def setup_jets(process, cms, options, postfix="PFlow"):
    print '=' * 60
    print "Setting up Jets"
    print '=' * 60
    # use external JECs (sqlite file)
    usePrivateSQlite = options.useJECFromFile
    runOnData = options.isData
    '''
    application of residual corrections. Have to be set to True once the 13 TeV
    residual corrections are available. False to be kept meanwhile. Can be kept
    to False
    '''
    applyResiduals = options.applyResiduals

    # MC setup
    inputJetCorrLabel = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])

    if runOnData:  # data set up
        if applyResiduals:
            inputJetCorrLabel = (
                'AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
        else:
            inputJetCorrLabel = (
                'AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])

    # If you want to use other JEC files then put .db file in data/JEC/ and use option useJECFromFile=1 on command line
    if usePrivateSQlite:
        from CondCore.DBCommon.CondDBSetup_cfi import *
        import os
        era = "Fall15_25nsV2_"
        if runOnData:
            era += 'DATA'
        else:
            era += 'MC'
        dBFile = os.path.expandvars(
            "$CMSSW_BASE/src/BristolAnalysis/NTupleTools/data/JEC/" + era + ".db")
            # era + ".db")
        print 'Using JEC from DB: {0}'.format(dBFile)
        process.jec = cms.ESSource("PoolDBESSource", CondDBSetup,
                                   connect=cms.string(
                                       "sqlite_file:" + dBFile),
                                   toGet=cms.VPSet(
                                       cms.PSet(
                                           record=cms.string(
                                               "JetCorrectionsRecord"),
                                           tag=cms.string(
                                               "JetCorrectorParametersCollection_" + era + "_AK4PF"),
                                           label=cms.untracked.string("AK4PF")
                                       ),
                                       cms.PSet(
                                           record=cms.string(
                                               "JetCorrectionsRecord"),
                                           tag=cms.string(
                                               "JetCorrectorParametersCollection_" + era + "_AK4PFchs"),
                                           label=cms.untracked.string(
                                               "AK4PFchs")
                                       ),
                                   )
                                   )
        process.es_prefer_jec = cms.ESPrefer("PoolDBESSource", 'jec')


    print 'Using jet energy corrections: '
    print 'PF Jets'
    print inputJetCorrLabel

    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetCorrFactorsUpdated
    process.patJetCorrFactorsReapplyJEC = patJetCorrFactorsUpdated.clone(
      src = cms.InputTag("slimmedJets"),
      levels = inputJetCorrLabel[1],
      payload = inputJetCorrLabel[0] ) # Make sure to choose the appropriate levels and payload here!

    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated
    process.patJetsReapplyJEC = patJetsUpdated.clone(
      jetSource = cms.InputTag("slimmedJets"),
      jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
      )

    process.reapplyJEC = cms.Sequence( process.patJetCorrFactorsReapplyJEC + process.patJetsReapplyJEC )

#     if options.CMSSW == '44X':
#         process.patJetCorrFactorsPFlow.payload = inputJetCorrLabel[0]
#         process.patJetCorrFactorsPFlow.levels = inputJetCorrLabel[1]
#         process.patJetCorrFactorsPFlow.rho = cms.InputTag("kt6PFJets", "rho")
#
#     ###############################
#     #### Jet RECO includes ########
#     ###############################
#
#     from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
#
#     ###############################
#     ###### Bare KT 0.6 jets #######
#     ###############################
#
#     from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
#
#     process.kt6PFJets = kt4PFJets.clone(
#                                         rParam=cms.double(0.6),
#                                         doAreaFastjet=cms.bool(True),
#                                         doRhoFastjet=cms.bool(True)
#     )
#     process.kt6PFJetsPFlow = kt4PFJets.clone(
#                                              rParam=cms.double(0.6),
#                                              src=cms.InputTag('pfNoElectron' + postfix),
#                                              doAreaFastjet=cms.bool(True),
#                                              doRhoFastjet=cms.bool(True)
#     )
#     process.kt4PFJetsPFlow = kt4PFJets.clone(
#                                              rParam=cms.double(0.4),
#                                              src=cms.InputTag('pfNoElectron' + postfix),
#                                              doAreaFastjet=cms.bool(True),
#                                              doRhoFastjet=cms.bool(True)
#     )
#
#     ###############################
#     ### TagInfo and Matching Setup#
#     ###############################
#
# Do some configuration of the jet substructure things
#     for jetcoll in [process.patJetsPFlow] :
#         if options.useData == False :
#             jetcoll.embedGenJetMatch = True
#             jetcoll.getJetMCFlavour = True
#             jetcoll.addGenPartonMatch = True
# Add CATopTag info... piggy-backing on b-tag functionality
#         jetcoll.addBTagInfo = True
#         jetcoll.embedCaloTowers = True
#         jetcoll.embedPFCandidates = True
#
#     additionalJets = [getattr(process, "kt6PFJets"),
#                       getattr(process, "kt6PFJets" + postfix),
#                       getattr(process, "kt4PFJets" + postfix)]
#     pfNoElectron = getattr(process, "pfNoElectron" + postfix)
#     for module in additionalJets :
#         getattr(process, "patPF2PATSequence" + postfix).replace(pfNoElectron, pfNoElectron * module)

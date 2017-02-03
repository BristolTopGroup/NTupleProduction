# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.CaloJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *
from BristolAnalysis.NTupleTools.options import CMSSW_MAJOR_VERSION
# this has to run AFTER setup_PF2PAT


def setup_jets(process, cms, options, postfix="PFlow"):
    print '=' * 60
    print "Setting up Jets"
    print "Deprecated : JEC from GT are applied in JetUserData"
    print '=' * 60
    # use external JECs (sqlite file)
    usePrivateSQlite = options.useJECFromFile
    runOnData = options.isData

    if not usePrivateSQlite:
      print 'Using default JEC already applied on jets in miniAOD'
      process.reapplyJEC = cms.Sequence()
      return

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
        era = "Spring16_25nsV6_"
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

    if int(CMSSW_MAJOR_VERSION) < 8:
        from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetCorrFactorsUpdated as updatedPatJetCorrFactors
    else:
        from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJetCorrFactors
    process.patJetCorrFactorsReapplyJEC = updatedPatJetCorrFactors.clone(
      src = cms.InputTag("slimmedJets"),
      levels = inputJetCorrLabel[1],
      payload = inputJetCorrLabel[0] ) # Make sure to choose the appropriate levels and payload here!

    if int(CMSSW_MAJOR_VERSION) < 8:
        from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated as updatedPatJets
    else:
        from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJets
    process.patJetsReapplyJEC = updatedPatJets.clone(
      jetSource = cms.InputTag("slimmedJets"),
      jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
      )

    process.reapplyJEC = cms.Sequence( process.patJetCorrFactorsReapplyJEC + process.patJetsReapplyJEC )

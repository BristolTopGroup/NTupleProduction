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
    '''
    application of residual corrections. Have to be set to True once the 13 TeV
    residual corrections are available. False to be kept meanwhile. Can be kept
    to False
    '''
    print '=' * 60
    print "Setting up Jets"
    print "Overwrites JEC/JER in GT for application in JetUserData"
    print "Presently only JER (Please modify for JEC)"
    print '=' * 60
    import os
    # If you want to use other JEC files then put .db file in data/JEC/ and use option useJECFromFile=1 on command line

    runOnData = options.isData
    era = "Spring16_25nsV10_"
    if runOnData: era += 'DATA'
    else: era += 'MC'
    dBFile = os.path.expandvars("$CMSSW_BASE/src/BristolAnalysis/NTupleTools/data/JEC/" + era + ".db")
    print 'Using JEC from DB: {0}'.format(dBFile)

    if not runOnData:
        # JER
        process.load('Configuration.StandardSequences.Services_cff')
        process.load("JetMETCorrections.Modules.JetResolutionESProducer_cfi")
        from CondCore.DBCommon.CondDBSetup_cfi import CondDBSetup

        process.jer = cms.ESSource("PoolDBESSource",
                CondDBSetup,
                toGet = cms.VPSet(
                    # Resolution
                    cms.PSet(
                        record = cms.string('JetResolutionRcd'),
                        tag    = cms.string('JR_Spring16_25nsV10_MC_PtResolution_AK4PFchs'),
                        label  = cms.untracked.string('AK4PFchs_pt')
                        ),

                    # Scale factors
                    cms.PSet(
                        record = cms.string('JetResolutionScaleFactorRcd'),
                        tag    = cms.string('JR_Spring16_25nsV10_MC_SF_AK4PFchs'),
                        label  = cms.untracked.string('AK4PFchs')
                        ),
                    ),
                connect = cms.string('sqlite_file:'+dBFile)
                )
        process.es_prefer_jer = cms.ESPrefer('PoolDBESSource', 'jer')

    # process.jec = cms.ESSource("PoolDBESSource", 
    #         CondDBSetup,
    #         toGet=cms.VPSet(
    #             cms.PSet(
    #                 record=cms.string("JetCorrectionsRecord"),
    #                 tag=cms.string("JetCorrectorParametersCollection_" + era + "_AK4PF"),
    #                 label=cms.untracked.string("AK4PF")
    #             ),
    #             cms.PSet(
    #                 record=cms.string("JetCorrectionsRecord"),
    #                 tag=cms.string("JetCorrectorParametersCollection_" + era + "_AK4PFchs"),
    #                 label=cms.untracked.string("AK4PFchs")
    #             ),
    #         ),
    #         connect=cms.string("sqlite:" + dBFile),
    # )
    # process.es_prefer_jec = cms.ESPrefer("PoolDBESSource", 'jec')


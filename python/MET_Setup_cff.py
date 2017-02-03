# this has to run AFTER setup_PF2PAT
def setup_MET(process, cms, options, postfix="PFlow"):
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    print '=' * 60
    print "Re-running MET on MiniAOD"
    print '=' * 60
    usePrivateSQlite = options.useJECFromFile
    runOnData = options.isData
    '''
    application of residual corrections. Have to be set to True once the 13 TeV
    residual corrections are available. False to be kept meanwhile. Can be kept
    to False
    '''
    applyResiduals = options.applyResiduals

    if usePrivateSQlite:
        from CondCore.DBCommon.CondDBSetup_cfi import *
        import os
        era = "Fall15_25nsV2_"
        if runOnData:
            era += 'DATA'
        else:
            era += 'MC'
        dBFile = os.path.expandvars(
            era + ".db")
           # "$CMSSW_BASE/src/BristolAnalysis/NTupleTools/data/JEC/" + era + ".db")
        process.jec = cms.ESSource( "PoolDBESSource",CondDBSetup,
                                    connect = cms.string( "sqlite_file:"+dBFile ),
                                    toGet =  cms.VPSet(
                                        cms.PSet(
                                            record = cms.string("JetCorrectionsRecord"),
                                            tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PF"),
                                            label= cms.untracked.string("AK4PF")
                                            ),
                                        cms.PSet(
                                            record = cms.string("JetCorrectionsRecord"),
                                            tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PFchs"),
                                            label= cms.untracked.string("AK4PFchs")
                                            ),
                                        )
                                    )
        process.es_prefer_jec = cms.ESPrefer("PoolDBESSource",'jec')

    # recalculate MET with JEC
    runMetCorAndUncFromMiniAOD(
        process,
        isData=runOnData,
        electronColl = cms.InputTag('calibratedPatElectrons'),
    )



# this has to run AFTER setup_PF2PAT
def setup_MET(process, cms, options, postfix="PFlow"):
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    print '=' * 60
    print "Re-running MET on MiniAOD"
    print '=' * 60
    runOnData = options.isData

    # Running post Jet_Setup so GT should already be overwritten if needed?
    # recalculate MET with JEC
    runMetCorAndUncFromMiniAOD(
        process,
        isData=runOnData,
        electronColl = cms.InputTag('calibratedPatElectrons'),
    )



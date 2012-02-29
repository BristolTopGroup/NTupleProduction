#--------------------------------------------------------------------------------
#
# configure Jet Energy Corrections
#--------------------------------------------------------------------------------
def configureCustomJEC(process, cms):
    process.load("CondCore.DBCommon.CondDBCommon_cfi")
    process.jec = cms.ESSource("PoolDBESSource",
            DBParameters = cms.PSet(
            messageLevel = cms.untracked.int32(0)
            ),
            timetype = cms.string('runnumber'),
            toGet = cms.VPSet(
                    cms.PSet(
                             record = cms.string('JetCorrectionsRecord'),
                             tag    = cms.string('JetCorrectorParametersCollection_Jec11_V12_AK5PF'),
                             label  = cms.untracked.string('AK5PF')
            ),
        cms.PSet(
           record = cms.string('JetCorrectionsRecord'),
           tag    = cms.string('JetCorrectorParametersCollection_Jec11_V12_AK5Calo'),
           label  = cms.untracked.string('AK5Calo')
       )
   ),
   connect = cms.string('sqlite_fip:Jec11_V12_20111220.db')
   )
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource', 'jec')
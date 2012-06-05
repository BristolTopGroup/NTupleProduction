#--------------------------------------------------------------------------------
#
# configure Jet Energy Corrections
#--------------------------------------------------------------------------------
def configureCustomJEC_DATA(process, cms, database = 'Jec11_V12_20111220.db'):
    database = 'sqlite_fip:' + database
    print 'Using "%s" as JEC database for DATA' % database
    process.load("CondCore.DBCommon.CondDBCommon_cfi")
    process.jec = cms.ESSource("PoolDBESSource",
            DBParameters = cms.PSet(
            messageLevel = cms.untracked.int32(0)
            ),
            timetype = cms.string('runnumber'),
            toGet = cms.VPSet(
                    cms.PSet(
                             record = cms.string('JetCorrectionsRecord'),
                             tag    = cms.string('JetCorrectorParametersCollection_Summer12_V3_DATA_AK5PF'),
                             label  = cms.untracked.string('AK5PF')
            ),
        cms.PSet(
           record = cms.string('JetCorrectionsRecord'),
           tag    = cms.string('JetCorrectorParametersCollection_Summer12_V3_DATA_AK5Calo'),
           label  = cms.untracked.string('AK5Calo')
       )
   ),
   connect = cms.string(database)
   )
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource', 'jec')

def configureCustomJEC_MC(process, cms, database = 'Jec11_V12_20111220.db'):
    database = 'sqlite_fip:' + database
    print 'Using "%s" as JEC database for MC' % database
    process.load("CondCore.DBCommon.CondDBCommon_cfi")
    process.jec = cms.ESSource("PoolDBESSource",
            DBParameters = cms.PSet(
            messageLevel = cms.untracked.int32(0)
            ),
            timetype = cms.string('runnumber'),
            toGet = cms.VPSet(
                    cms.PSet(
                             record = cms.string('JetCorrectionsRecord'),
                             tag    = cms.string('JetCorrectorParametersCollection_Summer12_V3_MC_AK5PF'),
                             label  = cms.untracked.string('AK5PF')
            ),
	cms.PSet(
           record = cms.string('JetCorrectionsRecord'),
           tag    = cms.string('JetCorrectorParametersCollection_Summer12_V3_MC_AK5Calo'),
           label  = cms.untracked.string('AK5Calo')
       )
   ),
   connect = cms.string(database)
   )
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource', 'jec')


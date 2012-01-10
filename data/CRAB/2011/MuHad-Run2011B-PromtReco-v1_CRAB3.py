from WMCore.Configuration import Configuration

config = Configuration()
config.section_("General")
config.General.requestName   = 'MuHad_Run2011B-PromptReco-v1_nTupleV4d'
config.General.serverUrl = 'vocms104.cern.ch:8880'

## Specific option of the job type
## these options are directly readable from the job type plugin
config.section_("JobType")
config.JobType.pluginName  = 'Cmssw'
config.JobType.psetName    = 'BristolAnalysis/NTupleTools/test/nTupleMaker_cfg.py'

## Specific data options
config.section_("Data")
config.Data.inputDataset = '/MuHad/Run2011B-PromptReco-v1/AOD'
config.Data.processingVersion = 'v4d'
config.Data.lumiMask = 'BristolAnalysis/NTupleTools/data/CertifiedJSONs/Cert_160404-178677_7TeV_PromptReco_Collisions11_JSON.txt'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJobs = 50

## User options
config.section_("User")
config.User.team  = 'TopQuarkAnalysis'
config.User.group = 'TopQuarkAnalysis'
config.User.email = ''

config.section_("Site")
config.Site.storageSite = 'T2_UK_SGrid_Bristol'
config.Site.blacklist = ['T1_DE_KIT','T1_ES_PIC','T1_FR_CCIN2P3','T1_IT_CNAF','T1_TW_ASGC','T1_UK_RAL','T1_US_FNAL']
config.Site.whitelist = ['T2_DE_DESY', 'T2_DE_RWTH', 'T2_UK_*']

#[CRAB]
#scheduler = glidein
#use_server = 1

#get_edm_output = 1
#pycfg_params = useData=1 dataType=MuHad skim=MuonOnly


#[USER]
#debug_wrapper = 1
#return_data = 0
#copy_data = 1
#storage_element = T2_UK_SGrid_Bristol
#publish_data = 1
#publish_data_name = nTuple_v4c_Run2011B-PromptReco-v1_GoldenJSON_muonSkim
#dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
#check_user_remote_dir = 0
#ui_working_dir = MuHad_Run2011B-PromptReco-v1_nTupleV4c

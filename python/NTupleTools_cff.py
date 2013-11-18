# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# Import LumiList for running on specific JSON files or excluding/including specific events when running locally.
import FWCore.PythonUtilities.LumiList as LumiList

from PhysicsTools.PatAlgos.tools.coreTools import *
#set up analysis

#use jet energy correction from database (loaded from BristolAnalysis/NTupleTools/python_custom_JEC_cff.py)
#==False -> use JEC from Global Tag 
USE_JEC_FROM_DB = False
#if 'False' taus are included in the jet collections
removeTausFromJetCollection = False
#if remove eles from gen jets
excludeElectronsFromWsFromGenJets = True	

#maximal relative isolation for loose leptons
maxLooseLeptonRelIso = 999.0

makePATTuple = False

postfix = "PFlow"
###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Run this on real data")

options.register ('hltProcess',
                  'HLT',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "HLT process name to use.")

options.register ('writeFat',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Calo Jets and leptons")

options.register ('useGSFelectrons',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Use GSF instead of PF electrons in PAT")

options.register ('setupMETmanually',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Alternative way of setting up PFMET with PF2PAT (see python/MET_Setup_cff.py)")

options.register ('applyType0METcorrection',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Apply type0 MET correction")

options.register ('applySysShiftCorrection',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Apply x/y Shift Correction (for phi modulation)")

options.register ('writeIsolatedPFLeptons',
                  True,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Output isolated PF leptons")

options.register ('forceCheckClosestZVertex',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Force the check of the closest z vertex")

options.register ('dataType',
                  '',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "DataType prefix for output file name")

options.register ('skim',
                  'Lepton_2Jets',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "Skim definition")

options.register ('maxLooseLeptonRelIso',
                  5.,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.float,
                  "Maximum (PF)relIso value for leptons to be stored.")

options.register ('printEventContent',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Outputs the event content at the end of the path")

options.register ('CMSSW',
                  '53X',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "CMSSW version used: 53X (default), 52X or 44X")

options.register ('centreOfMassEnergy',
                  8,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.float,
                  "Centre of Mass Energy in TeV; 7TeV for 2011, 8TeV for 2012")

options.register ('storePDFWeights',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Will store the PDF weights from cteq6.6")

options.register ('isTTbarMC',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Identify if samples contains ttbar events")

options.register ('isMCatNLO',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
		 "Identify if samples contains ttbar MC@NLO events (different genParticle structure)")

options.register ('skipEvents',
                  0,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Number of events to skip (0 for none)")
			       
#CMSSW 44X can't compile this file in the python directory correctly 
#as it fails to identify the file ending. This hack helps.
import sys
hasCorrectEnding = False
for arg in sys.argv:
    if '.py' in arg:
        hasCorrectEnding = True
if not hasCorrectEnding:
    sys.argv.append('something.py')

options.parseArguments()

#https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions
#Globals tags have been updated with the new JEC from https://twiki.cern.ch/twiki/bin/viewauth/CMS/JECDataMC

if options.CMSSW == "53X" and options.centreOfMassEnergy == 8:
    #Data Global Tag
    GLOBALTAG_DATA = 'FT_53_V21_AN3::All' # Used for 2012 A, B, C and D: 22Jan2013 re-reco
    #Monte Carlo Global Tag
    GLOBALTAG_MC = 'START53_V21::All' #TO BE UPDATED TO RELEVANT 5_3_X 2011 7TEV PRODUCTION GLOBAL TAGS
    FILETAG = '53X'
    TEST_DATA_FILE = 'file:///storage/TopQuarkGroup/test/SingleElectron_Run2012B_13Jul2012_ReReco_AOD.root'
    TEST_MC_FILE = 'file:///storage/TopQuarkGroup/mc/8TeV/SynchEx/Summer12_DR53X_TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola_AODSIM_PU_S10_START53_V7A-v1.root'
elif options.CMSSW == "53X" and options.centreOfMassEnergy == 7:
    #Data Global Tag
    GLOBALTAG_DATA = 'FT_R_53_LV5::All' #Winter 2013 2011A&B Legacy re-reco in CMSSW_5_3_X
    #Monte Carlo Global Tag
    GLOBALTAG_MC = 'START53_V21::All' #TO BE UPDATED TO RELEVANT 5_3_X 2011 7TEV PRODUCTION GLOBAL TAGS WHEN AVAILABLE
    FILETAG = '53X'
    TEST_DATA_FILE = 'file:///storage/TopQuarkGroup/test/ElectronHad_Run2011A-12Oct2013-v1_AOD.root' #test file for 2011 7TEV RunA Oct2013 re-reco
    TEST_MC_FILE = '' # NOT AVAILABLE YET
elif options.CMSSW == '44X':
    GLOBALTAG_DATA = 'GR_R_44_V15::All'
    GLOBALTAG_MC = 'START44_V13::All'
    FILETAG = '44X'
    TEST_DATA_FILE = 'file:///storage/TopQuarkGroup/test/ElectronHad_Run2011A_44X_AOD.root'
    TEST_MC_FILE = 'file:///storage/TopQuarkGroup/test/TTJets_TuneZ2_7TeV_Fall11_44X_AODSIM.root'
    #CERN
    #TEST_DATA_FILE = '/store/data/Run2011A/ElectronHad/AOD/08Nov2011-v1/0012/C481C0D4-1D1A-E111-8B01-E0CB4E1A1190.root'
    #TEST_MC_FILE =  '/store/mc/Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S6_START44_V9B-v1/0003/FEE78BEE-0237-E111-9CBC-003048678F06.root'
elif options.CMSSW == '52X':
    GLOBALTAG_DATA = 'GR_R_52_V9D::All'
    GLOBALTAG_MC = 'START52_V11C::All'
    FILETAG = '52X'
    TEST_DATA_FILE = 'file:///storage/TopQuarkGroup/test/SingleElectron_Run2012B_196531_524_PromptReco-v1_AOD.root'
    TEST_MC_FILE = 'file:///storage/TopQuarkGroup/mc/8TeV/SynchEx/Summer12_TTJets_TuneZ2star_8TeV-madgraph-tauola_AODSIM_PU_S7_START52_V5-v1.root'
    #CERN
#    TEST_DATA_FILE = '/store/data/Run2012A/ElectronHad/AOD/PromptReco-v1/000/193/336/C47F154E-A697-E111-83F5-001D09F24D8A.root'
#    TEST_MC_FILE = '/store/mc/Summer12/TTJets_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S7_START52_V9-v1/0000/FEDDBC6A-9290-E111-B7FD-0018F3D09628.root'

#CERN
#TEST_DATA_FILE = '/store/data/Run2012A/ElectronHad/AOD/PromptReco-v1/000/193/336/C47F154E-A697-E111-83F5-001D09F24D8A.root'
#TEST_MC_FILE = 'file:///afs/cern.ch/user/s/senkin/workspace/public/Summer12_DR53X_TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola_AODSIM_PU_S10_START53_V7A-v1.root'

maxLooseLeptonRelIso = options.maxLooseLeptonRelIso

if USE_JEC_FROM_DB:
    print "Loading JEC from database"
    from BristolAnalysis.NTupleTools.custom_JEC_cff import *
    database = ''
    if options.useData:
        database = 'BristolAnalysis/NTupleTools/data/JEC/Summer12_V3_DATA.db'
        configureCustomJEC_DATA(process, cms, database)
    else:
        database = 'BristolAnalysis/NTupleTools/data/JEC/Summer12_V3_MC.db'
        configureCustomJEC_MC(process, cms, database)
    
if not options.useData :
    process.source.fileNames = [
            TEST_MC_FILE
            ]
else:
    process.source.fileNames = [
            TEST_DATA_FILE
            ]

# Use lumisToProcess to specify a JSON file to use when running locally.
#process.source.lumisToProcess = LumiList.LumiList(filename = 'BristolAnalysis/NTupleTools/data/CertifiedJSONs/Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt').getVLuminosityBlockRange()
# Use eventsToSkip to specify events which you do not want to process when running locally.
#process.source.eventsToSkip = cms.untracked.VEventRange('193336:280110630')
    
# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")

###############################
####### Global Setup ##########
###############################
if options.useData :
        process.GlobalTag.globaltag = cms.string(GLOBALTAG_DATA)
else :
        process.GlobalTag.globaltag = cms.string(GLOBALTAG_MC)

        
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
    
process.goodOfflinePrimaryVertices = cms.EDFilter(
  "PrimaryVertexObjectFilter",
  filterParams=cms.PSet(
                        minNdof=cms.double(4.),
                        maxZ=cms.double(24.),
                        maxRho=cms.double(2.)
                        ),
  filter=cms.bool(True),
  src=cms.InputTag('offlinePrimaryVertices')
)

#EventFilters and skim
from BristolAnalysis.NTupleTools.EventFilters_cff import *
process.EventFilters = setup_eventfilters(process, cms, options)
#PF2PAT
from BristolAnalysis.NTupleTools.PF2PAT_Setup_cff import *
setup_PF2PAT(process, cms, options, postfix=postfix, removeTausFromJetCollection=removeTausFromJetCollection)
setup_looseLeptons(process, cms, options, postfix=postfix, maxLooseLeptonRelIso=maxLooseLeptonRelIso)
#Jets
from BristolAnalysis.NTupleTools.Jets_Setup_cff import *
setup_jets(process, cms, options, postfix=postfix)
#MET
from BristolAnalysis.NTupleTools.MET_Setup_cff import *
if options.setupMETmanually:
    setup_MET_manually(process, cms, options, postfix=postfix)
else:
    setup_MET(process, cms, options, postfix=postfix)
#electron ID
from BristolAnalysis.NTupleTools.ElectronID_cff import *
setup_electronID(process, cms)
#Object selection
from BristolAnalysis.NTupleTools.ObjectSelection_cff import *
selectObjects(process, cms)

#fix for loose pfIsolatedMuons for the newer tags
process.patMuonsLoosePFlow.pfMuonSource = cms.InputTag("pfIsolatedMuonsLoose" + postfix)
#fix for loose pfIsolatedElectrons for the newer tags
process.patElectronsLoosePFlow.pfElectronSource = cms.InputTag("pfIsolatedElectronsLoose" + postfix)

# turn to false when running on data
if options.useData :
    removeMCMatching(process, ['All'])
    process.looseLeptonSequence.remove(process.muonMatchLoosePFlow)
    
if not options.useData :
    ## needed for redoing the ak5GenJets
    process.load("BristolAnalysis.NTupleTools.GenJetParticles_cfi")
    process.load("RecoJets.Configuration.RecoGenJets_cff")
    #exclude the following particles with ids below from the gen jets electron had to be added, the rest are default
    if excludeElectronsFromWsFromGenJets :
        process.genParticlesForJetsNoNu.excludeFromResonancePids = [11, 12, 13, 14, 16]

process.patseq = cms.Sequence(
#    process.HBHENoiseFilter * 
    process.goodOfflinePrimaryVertices * 
    process.eidMVASequence *
    process.genParticlesForJetsNoNu *
    getattr(process, "patPF2PATSequence" + postfix) * 
    process.looseLeptonSequence * 
    process.patDefaultSequence * 
    process.goodPatJets * 
    process.goodPatJetsPFlow * 
    process.metUncertaintySequence * 
    process.EventFilters * 
    process.flavorHistorySeq 
    )

if options.useData:
    process.patseq.remove(process.genParticlesForJetsNoNu)
    process.patseq.remove(process.genJetParticles)    
    process.patseq.remove(process.flavorHistorySeq)
    process.patseq.remove(process.genParticlesForJets)
        
# remove flavour history as it has problems with the MC@NLO genparticles
if options.isMCatNLO:
    process.patseq.remove(process.flavorHistorySeq)

# HLT Trigger Report
process.hlTrigReport = cms.EDAnalyzer("HLTrigReport",
    HLTriggerResults=cms.InputTag("TriggerResults", "", options.hltProcess)
)


process.printEventContent = cms.EDAnalyzer("EventContentAnalyzer")
process.pdfWeights = cms.EDProducer("PdfWeightProducer",
                                    PdfInfoTag=cms.untracked.InputTag("generator"),
                                    PdfSetNames=cms.untracked.vstring(
                                         "cteq66.LHgrid", # 44 members
                                         )
                                    )

process.load('BristolAnalysis.NTupleTools.EventWeight_Producer_PU_cfi')
if options.CMSSW == '44X':
        process.eventWeightPU.MCSampleTag = cms.string("Fall11") # valid identifier: Fall11, Summer12    MCSampleFile        = cms.FileInPath("BristolAnalysis/NTupleTools/data/PileUp/MC_PUDist_Default2011.root"),
    	process.eventWeightPU.MCSampleFile        = cms.FileInPath("BristolAnalysis/NTupleTools/data/PileUp/MC_PUDist_Default2011.root")
    	process.eventWeightPU.MCSampleHistoName   = cms.string("histo_Fall11_true")
    	process.eventWeightPU.DataFile            = cms.FileInPath("BristolAnalysis/NTupleTools/data/PileUp/Data_PUDist_2011Full.root")
    	process.eventWeightPU.DataHistoName       = cms.string("histoData_true")
else:
        process.eventWeightPU.MCSampleTag = cms.string("Summer12")
        #process.eventWeightPU.MCSampleFile = cms.FileInPath("BristolAnalysis/NTupleTools/data/PileUp/MC_PUDist_Summer2012.root")
        process.eventWeightPU.MCSampleFile = cms.FileInPath("BristolAnalysis/NTupleTools/data/PileUp/MC_PUDist_Default2012.root")
	process.eventWeightPU.MCSampleHistoName   = cms.string("puhisto")

process.TFileService = cms.Service("TFileService",
                           fileName=cms.string('ntuple.root')
                           )
# rename output file
outPutFilePrefix = ''
if not options.dataType == '':
    outPutFilePrefix = options.dataType + '_'
if options.useData :
    if options.writeFat :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'nTuple_' + FILETAG + '_data_fat.root')
    else :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'nTuple_' + FILETAG + '_data.root')
else :
    if options.writeFat :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'nTuple_' + FILETAG + '_mc_fat.root')
    else :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'nTuple_' + FILETAG + '_mc.root')


# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)

#----------------------------------------------------------------------------------------------------
# The ECAL laser correction filter (ecalLaserCorrFilter) occasionally 
# interpolates laser correction values of < 1 and issues a LogError message
# 
# This does not affect the laser correction that is applied: only the interpolated estimate 
# that the filter uses.  The filter runs in "Tagging Mode", so no events can be removed.
# 
# Error message comes from line 173 of:
# CalibCalorimetry/EcalLaserCorrection/src/EcalLaserDbService.cc
# function = EcalLaserDbService::getLaserCorrection
# Message = "The interpolated laser correction is <= zero!"
#
# We suppress these messages.  Suppression can be removed by commenting the following line.
#----------------------------------------------------------------------------------------------------
process.MessageLogger.suppressError = cms.untracked.vstring ('ecalLaserCorrFilter') 

# process all the events
if options.maxEvents:
    process.maxEvents.input = options.maxEvents
else:
    process.maxEvents.input = 100
    
process.source.skipEvents = cms.untracked.uint32(options.skipEvents)
    
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")
process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*")

if not makePATTuple:
    #do not write PAT-tuple information
    del process.outpath

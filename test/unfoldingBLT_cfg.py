# import default nTuple stub
from BristolAnalysis.NTupleTools.NTupleTools_cff import *

##########################################################################################
#            General
##########################################################################################
process.load( 'TopQuarkAnalysis.TopSkimming.TtFullyHadronicFilter_cfi' )
process.load( 'TopQuarkAnalysis.TopSkimming.TtFullyLeptonicFilter_cfi' )
process.load( 'TopQuarkAnalysis.TopSkimming.TtSemiLeptonicFilter_cfi' )

process.load( 'BristolAnalysis.NTupleTools.TopPairElectronPlusJetsSelectionFilter_cfi' )
process.load( 'BristolAnalysis.NTupleTools.TopPairMuonPlusJetsSelectionFilter_cfi' )
 # filters only in tagging mode
process.topPairEPlusJetsSelection.taggingMode = cms.bool( True )
process.topPairMuPlusJetsSelection.taggingMode = cms.bool( True )

process.ttFullHadronicFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicFilter.taggingMode = cms.bool( True )
process.ttSemiLeptonicElectronFilter.taggingMode = cms.bool( True )
process.ttSemiLeptonicMuonFilter.taggingMode = cms.bool( True )
process.ttSemiLeptonicTauFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicEEFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicMuMuFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicTauTauFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicETauFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicEMuFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicMuTauFilter.taggingMode = cms.bool( True )

if options.isMCatNLO:
    process.ttFullHadronicFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicFilter.useMCATNLO = cms.bool( True )
    process.ttSemiLeptonicElectronFilter.useMCATNLO = cms.bool( True )
    process.ttSemiLeptonicMuonFilter.useMCATNLO = cms.bool( True )
    process.ttSemiLeptonicTauFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicEEFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicMuMuFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicTauTauFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicETauFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicEMuFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicMuTauFilter.useMCATNLO = cms.bool( True )

if options.CMSSW == '44X':
    process.topPairEPlusJetsSelection.MCSampleTag = cms.string( 'Fall11' )  
    process.topPairMuPlusJetsSelection.MCSampleTag = cms.string( 'Fall11' )
elif options.CMSSW == '53X' and options.centreOfMassEnergy == 8:
    process.topPairEPlusJetsSelection.MCSampleTag = cms.string( 'Summer12' )  
    process.topPairMuPlusJetsSelection.MCSampleTag = cms.string( 'Summer12' )
elif options.CMSSW == '53X' and options.centreOfMassEnergy == 7:
    process.topPairEPlusJetsSelection.MCSampleTag = cms.string( 'Summer11Leg' )  
    process.topPairMuPlusJetsSelection.MCSampleTag = cms.string( 'Summer11Leg' )

if options.applyZselection:
    process.topPairEPlusJetsSelection.tagAndProbeStudies = cms.bool( True )
    process.topPairMuPlusJetsSelection.tagAndProbeStudies = cms.bool( True )

if options.dropTriggerSelection:
    process.topPairEPlusJetsSelection.dropTriggerSelection = cms.bool( True )
    process.topPairMuPlusJetsSelection.dropTriggerSelection = cms.bool( True )

electronselectionPrefix = 'TopPairElectronPlusJetsSelection.'
muonselectionPrefix = 'TopPairMuonPlusJetsSelection.'

process.topPairEPlusJetsSelection.prefix = cms.untracked.string( electronselectionPrefix )
process.topPairMuPlusJetsSelection.prefix = cms.untracked.string( muonselectionPrefix )

process.load( "TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff" )

process.MCFiltersInTaggingMode = cms.Sequence( process.makeGenEvt * 
                                                     process.ttFullHadronicFilter * 
                                                     process.ttFullLeptonicFilter * 
                                                     process.ttSemiLeptonicElectronFilter * 
                                                     process.ttSemiLeptonicMuonFilter * 
                                                     process.ttSemiLeptonicTauFilter * 
                                                     process.ttFullLeptonicEEFilter * 
                                                     process.ttFullLeptonicMuMuFilter * 
                                                     process.ttFullLeptonicTauTauFilter * 
                                                     process.ttFullLeptonicETauFilter * 
                                                     process.ttFullLeptonicEMuFilter * 
                                                     process.ttFullLeptonicMuTauFilter )

process.eventFiltersIntaggingMode = cms.Sequence( process.MCFiltersInTaggingMode * 
                                                     process.topPairEPlusJetsSelection * 
                                                     process.topPairMuPlusJetsSelection )

##########################################################################################
#            Unfolding Config
##########################################################################################
process.load( 'BristolAnalysis.NTupleTools.BTagWeight_Producer_cfi' )
process.load( 'BristolAnalysis.NTupleTools.MuonWeight_Producer_cfi' )
process.load( 'BristolAnalysis.NTupleTools.ElectronWeight_Producer_cfi' )
process.load( 'BristolAnalysis.NTupleTools.UnfoldingProducer_cfi' )
process.eventWeightBtagEPlusJets = process.eventWeightBtag.clone( 
            numberOfTagsInput = cms.InputTag( "topPairEPlusJetsSelection", electronselectionPrefix + 'NumberOfBtags', 'PAT' ),
            jetInput = cms.InputTag( "topPairEPlusJetsSelection", electronselectionPrefix + 'cleanedJets', 'PAT' ),
            targetBtagMultiplicity = cms.uint32( 2 ),  # will calculate the weight for b-tag multiplicity >=2
            BTagSystematic = cms.int32( 0 )
            )
process.eventWeightBtagMuPlusJets = process.eventWeightBtagEPlusJets.clone( 
            numberOfTagsInput = cms.InputTag( "topPairMuPlusJetsSelection", muonselectionPrefix + 'NumberOfBtags', 'PAT' )  ,
            jetInput = cms.InputTag( "topPairMuPlusJetsSelection", muonselectionPrefix + 'cleanedJets', 'PAT' ),
                                                              )
process.eventWeightElectrons.electronIDScaleFactorsFile = cms.FileInPath("BristolAnalysis/NTupleTools/data/ScaleFactors/scaleFactors_electron_id_iso.root")
process.eventWeightElectrons.electronTriggerEfficiencyFile = cms.FileInPath("BristolAnalysis/NTupleTools/data/ScaleFactors/scaleFactors_electron_trigger.root")
process.eventWeightElectrons.hadronLegEfficiencyFileName = cms.FileInPath("BristolAnalysis/NTupleTools/data/ScaleFactors/hadronLegEfficiencies_electron.root")
process.eventWeightMuons.muonScaleFactorsFile = cms.FileInPath("BristolAnalysis/NTupleTools/data/ScaleFactors/MuonEfficiencies_SF_2011_53X_DataMC.root")

if options.CMSSW == '53X' and options.centreOfMassEnergy == 8:
  process.eventWeightElectrons.MCSampleTag = cms.string( 'Summer12' )
  process.eventWeightMuons.MCSampleTag = cms.string( 'Summer12' )
elif options.CMSSW == '53X' and options.centreOfMassEnergy == 7:
  process.eventWeightElectrons.MCSampleTag = cms.string( 'Summer11Leg' )
  process.eventWeightMuons.MCSampleTag = cms.string( 'Summer11Leg' )

electron_unfolding_analysers = [
    process.unfoldingProducerElectron,
]

# Set input collections
# e.g. use cleaned jets (rather than default selected jets)
for analyser in electron_unfolding_analysers:
    analyser.selection_flag_input = cms.InputTag( "topPairEPlusJetsSelection", electronselectionPrefix + 'FullSelection', 'PAT' )
    analyser.b_tag_weight_input = cms.InputTag( 'eventWeightBtagEPlusJets' )
    analyser.reco_jet_input = cms.InputTag( "topPairEPlusJetsSelection", electronselectionPrefix + 'cleanedJets', 'PAT' )
    analyser.electron_input = cms.InputTag( "topPairEPlusJetsSelection", electronselectionPrefix + 'signalElectron', 'PAT' )
    analyser.leptonWeightsInputTag = cms.InputTag( "eventWeightElectrons" )

muon_unfolding_analysers = [
    process.unfoldingProducerMuon,    
]

for analyser in muon_unfolding_analysers:
    analyser.selection_flag_input = cms.InputTag( "topPairMuPlusJetsSelection", muonselectionPrefix + 'FullSelection', 'PAT' )
    analyser.b_tag_weight_input = cms.InputTag( 'eventWeightBtagMuPlusJets' )
    analyser.reco_jet_input = cms.InputTag( "topPairMuPlusJetsSelection", muonselectionPrefix + 'cleanedJets', 'PAT' )
    analyser.muon_input = cms.InputTag( "topPairMuPlusJetsSelection", muonselectionPrefix + 'signalMuon', 'PAT' )

# NTuple setup
process.rootTupleTree = cms.EDAnalyzer("RootTupleMakerV2_Tree",
    treeName = cms.string('tree'),
    outputCommands=cms.untracked.vstring(
       'drop *',
    )
)

# E+jets channel
process.rootTupleTreeEPlusJets = copy.copy( process.rootTupleTree )
process.rootTupleTreeEPlusJets.treeName=cms.string( 'ePlusJetsTree' )
process.rootTupleTreeEPlusJets.outputCommands=cms.untracked.vstring(
                                                                    'drop *',
                                                                    'keep *_unfoldingProducerElectron_*_*'
                                                                    )
# Mu+jets channel
process.rootTupleTreeMuPlusJets = copy.copy( process.rootTupleTree )
process.rootTupleTreeMuPlusJets.treeName=cms.string( 'muPlusJetsTree' )
process.rootTupleTreeMuPlusJets.outputCommands=cms.untracked.vstring(
                                                                    'drop *',
                                                                    'keep *_unfoldingProducerMuon_*_*'
                                                                    )

process.load( 'BristolAnalysis.NTupleTools.SelectionAnalyser_cfi' )

process.commonSequence = cms.Sequence(
                                      process.pdfWeights *
                                      process.printEventContent *
                                      process.hlTrigReport * 
                                      process.egammaIDLikelihood * 
                                      process.pfMEtSysShiftCorrSequence * 
                                      process.patseq * 
                                      getattr( process, "producePatPFMETCorrections" + postfix ) * 
                                      getattr( process, "patMETs" + postfix ) *
                                      process.eventFiltersIntaggingMode * 
                                      process.eventWeightPU *
                                      process.ttbarDecayAnalyser
                                      )

if not options.printEventContent:
    process.commonSequence.remove( process.printEventContent )
    
process.ePlusJetsUnfoldingAnalysis = cms.Path( 
          process.commonSequence *
          process.eventWeightBtagEPlusJets * 
          process.topPairEPlusJetsSelectionAnalyser *
          process.eventWeightElectrons *
          process.unfoldingProducerElectron *
          process.rootTupleTreeEPlusJets
		  )

process.muPlusJetsUnfoldingAnalysis = cms.Path( 
          process.commonSequence *
          process.eventWeightBtagMuPlusJets * 
          process.topPairMuPlusJetsSelectionAnalyser *
          process.eventWeightMuons *
          process.unfoldingProducerMuon *
          process.rootTupleTreeMuPlusJets
          )

if not options.storePDFWeights:
    process.commonSequence.remove( process.pdfWeights )
    process.unfoldingProducerElectron.storePDFWeights = cms.bool(False)
    process.unfoldingProducerMuon.storePDFWeights = cms.bool(False)
                                                 
if not options.setupMETmanually:
    process.commonSequence.remove( getattr( process, "producePatPFMETCorrections" + postfix ) )
    process.commonSequence.remove( getattr( process, "patMETs" + postfix ) )

#this has to run AFTER setup_PF2PAT
def setup_MET(process, cms, options, postfix="PFlow"):
    print '=' * 60
    print "Setting up PFMET from PAT"
    print '=' * 60
        
    getattr(process,'patPFMet'+postfix).addGenMET = cms.bool(not options.useData)
    process.patPFMet.addGenMET = cms.bool(not options.useData)
    
    process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")
    
    setup_MET_uncertainties(process, cms, options, postfix)
    
    #these flags are false for '+postfix' mets by default, but true for non-postfix ones!
    getattr(process,'patPFJetMETtype1p2Corr'+postfix).skipEM = cms.bool(False)
    getattr(process,'patPFJetMETtype1p2Corr'+postfix).skipMuons = cms.bool(False)

def setup_MET_manually(process, cms, options, postfix="PFlow"):
    print '=' * 60
    print "Setting up PFMET from PAT manually"
    print '=' * 60
    
    #PFMET setup: following by-hand recipe from https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMetAnalysis#Type_I_II_0_with_PF2PAT
    process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
    getattr(process,'patPF2PATSequence'+postfix).remove(getattr(process,'patMETs'+postfix))

    from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
    cloneProcessingSnippet(process, process.producePatPFMETCorrections, postfix)

    getattr(process,'selectedPatJetsForMETtype1p2Corr'+postfix).src = cms.InputTag('selectedPatJets'+postfix)
    getattr(process,'selectedPatJetsForMETtype2Corr'+postfix).src = cms.InputTag('selectedPatJets'+postfix)
    getattr(process,'pfCandMETcorr'+postfix).src = cms.InputTag('pfNoJet'+postfix)
    getattr(process,'patPFJetMETtype1p2Corr'+postfix).type1JetPtThreshold = cms.double(10.0)
            
    getattr(process,'patType1CorrectedPFMet'+postfix).srcType1Corrections = cms.VInputTag(
                            cms.InputTag("patPFJetMETtype1p2Corr"+postfix,"type1"),
                            )
    getattr(process,'patType1p2CorrectedPFMet'+postfix).srcType1Corrections = cms.VInputTag(
                            cms.InputTag("patPFJetMETtype1p2Corr"+postfix,"type1"),
                            )
            
    getattr(process,'patPFJetMETtype1p2Corr'+postfix).skipEM = cms.bool(False)
    getattr(process,'patPFJetMETtype1p2Corr'+postfix).skipMuons = cms.bool(False)
    getattr(process,'patPFJetMETtype2Corr'+postfix).skipEM = cms.bool(False)
    getattr(process,'patPFJetMETtype2Corr'+postfix).skipMuons = cms.bool(False)

    ##for type I+II corrections, switch this to patType1p2CorrectedPFMet
    getattr(process,'patMETs'+postfix).metSource = cms.InputTag('patType1CorrectedPFMet'+postfix)

    getattr(process,'patDefaultSequence'+postfix).remove(getattr(process,'patMETs'+postfix))

    if options.useData:
        getattr(process,'patPFJetMETtype1p2Corr'+postfix).jetCorrLabel = 'L2L3Residual'
        getattr(process,'patPFJetMETtype2Corr'+postfix).jetCorrLabel = 'L2L3Residual'
    
    getattr(process,'patPFMet'+postfix).addGenMET = cms.bool(not options.useData)
    process.patPFMet.addGenMET = cms.bool(not options.useData)
    
    process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")
    
    #these flags are false for '+postfix' mets by default, but true for non-postfix ones!
    getattr(process,'patPFJetMETtype1p2Corr'+postfix).skipEM = cms.bool(False)
    getattr(process,'patPFJetMETtype1p2Corr'+postfix).skipMuons = cms.bool(False)
    
    setup_MET_uncertainties(process, cms, options, postfix)


def setup_MET_uncertainties(process, cms, options, postfix="PFlow"):
    from PhysicsTools.PatUtils.tools.metUncertaintyTools import runMEtUncertainties
    #runMEtUncertainties(process, doSmearJets=not options.useData, jetCollection='goodPatJetsPFlow', addToPatDefaultSequence=False)                                                                                                             
    if options.useData:
        inputJetCorrLabelForMETuncertainties = 'L2L3Residual'
    else:
        inputJetCorrLabelForMETuncertainties = 'L3Absolute'

    runMEtUncertainties(process,
                    electronCollection = cms.InputTag('cleanPatElectrons'),
                    muonCollection = 'cleanPatMuons',
                    tauCollection = 'cleanPatTaus',
                    jetCollection = cms.InputTag('goodPatJetsPFlow'),
                    jetCorrLabel = inputJetCorrLabelForMETuncertainties,
                    doSmearJets = not options.useData,
#                    makeType1corrPFMEt = True,
#                    makeType1p2corrPFMEt = True,
#                    makePFMEtByMVA = False,
#                    makeNoPileUpPFMEt = False,
#                    doApplyType0corr = options.applyType0METcorrection,
#                    sysShiftCorrParameter = process.pfMEtSysShiftCorrParameters_2012runAvsNvtx_data,
#                    doApplySysShiftCorr = options.applySysShiftCorrection,
                    addToPatDefaultSequence=False
                    )

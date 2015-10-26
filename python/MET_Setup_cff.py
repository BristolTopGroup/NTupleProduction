# this has to run AFTER setup_PF2PAT
def setup_MET(process, cms, options, postfix="PFlow"):
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    print '=' * 60
    print "Re-running MET on MiniAOD"
    print '=' * 60
    runOnData = options.isData
    '''
    application of residual corrections. Have to be set to True once the 13 TeV
    residual corrections are available. False to be kept meanwhile. Can be kept
    to False
    '''
    applyResiduals = options.applyResiduals



#     getattr(process,'patPFMet'+postfix).addGenMET = cms.bool(not options.isData)
#     process.patPFMet.addGenMET = cms.bool(not options.useData)
#
#     process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")
#     process.load("JetMETCorrections.Type1MET.pfMETsysShiftCorrections_cfi")
#
#     setup_MET_uncertainties(process, cms, options, postfix)
#
#     if options.applyType0METcorrection:
#         getattr(process,'patType1CorrectedPFMet'+postfix).srcType1Corrections = cms.VInputTag(
#                 cms.InputTag("patPFJetMETtype1p2Corr"+postfix,"type1"),
#                 cms.InputTag("patPFMETtype0Corr"+postfix)
#                 )
#         getattr(process,'patType1p2CorrectedPFMet'+postfix).srcType1Corrections = cms.VInputTag(
#                 cms.InputTag("patPFJetMETtype1p2Corr"+postfix,"type1"),
#                 cms.InputTag("patPFMETtype0Corr"+postfix)
#                 )

    # these flags are false for '+postfix' mets by default, but true for non-postfix ones!
#     getattr(process,'patPFJetMETtype1p2Corr'+postfix).skipEM = cms.bool(False)
#     getattr(process,'patPFJetMETtype1p2Corr'+postfix).skipMuons = cms.bool(False)

#     if options.applySysShiftCorrection:
#         getattr(process,'patType1CorrectedPFMet'+postfix).srcType1Corrections.append(cms.InputTag('pfMEtSysShiftCorr'))
#         getattr(process,'patType1p2CorrectedPFMet'+postfix).srcType1Corrections.append(cms.InputTag('pfMEtSysShiftCorr'))


    # if not applyResiduals:
    # process.patPFMetT1T2CorrCustomJEC.jetCorrLabelRes = cms.InputTag("L3Absolute")
    # process.patPFMetT1T2SmearCorrCustomJEC.jetCorrLabelRes = cms.InputTag("L3Absolute")
    # process.patPFMetT2CorrCustomJEC.jetCorrLabelRes = cms.InputTag("L3Absolute")
    # process.patPFMetT2SmearCorrCustomJEC.jetCorrLabelRes = cms.InputTag("L3Absolute")
    # process.shiftedPatJetEnDownCustomJEC.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
    # process.shiftedPatJetEnUpCustomJEC.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")

    # process.patPFMetT1T2CorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
    # process.patPFMetT1T2SmearCorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
    # process.patPFMetT2CorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
    # process.patPFMetT2SmearCorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
    # process.shiftedPatJetEnDownNoHF.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
    # process.shiftedPatJetEnUpNoHF.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")

def setup_MET_manually(process, cms, options, postfix="PFlow"):
    print '=' * 60
    print "Setting up PFMET from PAT manually"
    print '=' * 60

    # PFMET setup: following by-hand recipe from
    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMetAnalysis#Type_I_II_0_with_PF2PAT
    process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
    getattr(process, 'patPF2PATSequence' +
            postfix).remove(getattr(process, 'patMETs' + postfix))

    from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
    cloneProcessingSnippet(
        process, process.producePatPFMETCorrections, postfix)

    getattr(process, 'selectedPatJetsForMETtype1p2Corr' +
            postfix).src = cms.InputTag('selectedPatJets' + postfix)
    getattr(process, 'selectedPatJetsForMETtype2Corr' +
            postfix).src = cms.InputTag('selectedPatJets' + postfix)
    getattr(process, 'pfCandMETcorr' +
            postfix).src = cms.InputTag('pfNoJet' + postfix)
    getattr(process, 'patPFJetMETtype1p2Corr' +
            postfix).type1JetPtThreshold = cms.double(10.0)

    if options.applyType0METcorrection:
        getattr(process, 'patType1CorrectedPFMet' + postfix).srcType1Corrections = cms.VInputTag(
            cms.InputTag("patPFJetMETtype1p2Corr" + postfix, "type1"),
            cms.InputTag("patPFMETtype0Corr" + postfix)
        )
        getattr(process, 'patType1p2CorrectedPFMet' + postfix).srcType1Corrections = cms.VInputTag(
            cms.InputTag("patPFJetMETtype1p2Corr" + postfix, "type1"),
            cms.InputTag("patPFMETtype0Corr" + postfix)
        )
    else:
        getattr(process, 'patType1CorrectedPFMet' + postfix).srcType1Corrections = cms.VInputTag(
            cms.InputTag("patPFJetMETtype1p2Corr" + postfix, "type1"),
        )
        getattr(process, 'patType1p2CorrectedPFMet' + postfix).srcType1Corrections = cms.VInputTag(
            cms.InputTag("patPFJetMETtype1p2Corr" + postfix, "type1"),
        )

    getattr(process, 'patPFJetMETtype1p2Corr' +
            postfix).skipEM = cms.bool(False)
    getattr(process, 'patPFJetMETtype1p2Corr' +
            postfix).skipMuons = cms.bool(False)
    getattr(process, 'patPFJetMETtype2Corr' + postfix).skipEM = cms.bool(False)
    getattr(process, 'patPFJetMETtype2Corr' +
            postfix).skipMuons = cms.bool(False)

    # for type I+II corrections, switch this to patType1p2CorrectedPFMet
    getattr(process, 'patMETs' +
            postfix).metSource = cms.InputTag('patType1CorrectedPFMet' + postfix)

    getattr(process, 'patDefaultSequence' +
            postfix).remove(getattr(process, 'patMETs' + postfix))

    if options.useData:
        getattr(process, 'patPFJetMETtype1p2Corr' +
                postfix).jetCorrLabel = 'L2L3Residual'
        getattr(process, 'patPFJetMETtype2Corr' +
                postfix).jetCorrLabel = 'L2L3Residual'

    getattr(
        process, 'patPFMet' + postfix).addGenMET = cms.bool(not options.useData)
    process.patPFMet.addGenMET = cms.bool(not options.useData)

    process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")
    process.load("JetMETCorrections.Type1MET.pfMETsysShiftCorrections_cfi")

    # these flags are false for '+postfix' mets by default, but true for
    # non-postfix ones!
    getattr(process, 'patPFJetMETtype1p2Corr' +
            postfix).skipEM = cms.bool(False)
    getattr(process, 'patPFJetMETtype1p2Corr' +
            postfix).skipMuons = cms.bool(False)

    setup_MET_uncertainties(process, cms, options, postfix)


def setup_MET_uncertainties(process, cms, options, postfix="PFlow"):
    from PhysicsTools.PatUtils.tools.metUncertaintyTools import runMEtUncertainties
    #runMEtUncertainties(process, doSmearJets=not options.useData, jetCollection='goodPatJetsPFlow', addToPatDefaultSequence=False)
    if options.useData:
        inputJetCorrLabelForMETuncertainties = 'L2L3Residual'
        if options.centreOfMassEnergy == 8:
            metSysShiftCorrParameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_data
            print "using pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_data"
        elif options.centreOfMassEnergy == 7:
            metSysShiftCorrParameter = process.pfMEtSysShiftCorrParameters_2011runAplusBvsNvtx_data
            print "using pfMEtSysShiftCorrParameters_2011runAplusBvsNvtx_data"
    else:
        inputJetCorrLabelForMETuncertainties = 'L3Absolute'
        if options.centreOfMassEnergy == 8:
            metSysShiftCorrParameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_mc
            print "using pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_mc"
        elif options.centreOfMassEnergy == 7:
            metSysShiftCorrParameter = process.pfMEtSysShiftCorrParameters_2011runAplusBvsNvtx_mc
            print "using pfMEtSysShiftCorrParameters_2011runAplusBvsNvtx_mc"

    process.pfMEtSysShiftCorr.parameter = metSysShiftCorrParameter

    runMEtUncertainties(process,
                        electronCollection=cms.InputTag('patElectronsPFlow'),
                        muonCollection='patMuonsPFlow',
                        tauCollection='patTausPFlow',
                        jetCollection=cms.InputTag('goodPatJetsPFlow'),
                        jetCorrLabel=inputJetCorrLabelForMETuncertainties,
                        doSmearJets=not options.useData,
                        makeType1corrPFMEt=True,
                        makeType1p2corrPFMEt=True,
                        makePFMEtByMVA=False,
                        makeNoPileUpPFMEt=False,
                        doApplyType0corr=options.applyType0METcorrection,
                        sysShiftCorrParameter=metSysShiftCorrParameter,
                        doApplySysShiftCorr=options.applySysShiftCorrection,
                        addToPatDefaultSequence=False
                        )

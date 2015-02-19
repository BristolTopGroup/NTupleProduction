def setup_ntupler(process, cms, options):
    print '=' * 60
    print "Setting up NTupler"
    print '=' * 60
    ######################################################################################################
    ################################## nTuple Configuration ##############################################
    ######################################################################################################
    process.load('BristolAnalysis.NTupleTools.Ntuple_cff')
    #vertices
    process.rootTupleVertex.InputTag = cms.InputTag('goodOfflinePrimaryVertices')
    process.rootTupleVertex.Prefix = cms.string('goodOfflinePrimaryVertices.')
    #PF2PAT jets
    process.rootTuplePF2PATJets.InputTag = cms.InputTag('goodPatJetsPFlow')
    process.rootTuplePF2PATJets.Prefix = cms.string('goodPatJetsPFlow.')
    process.rootTuplePF2PATJets.isRealData = cms.bool(options.useData)
    #selection on GenParticles
    process.rootTupleGenParticles.minPt = cms.double(-1)
    process.rootTupleGenParticles.maxAbsoluteEta = cms.double(100)
    #GSF Electrons
    process.rootTupleElectrons.InputTag = cms.InputTag('selectedPatElectrons')
    process.rootTupleElectrons.Prefix = cms.string('selectedPatElectrons.')
    #isolated PF Electrons
    process.rootTuplePFElectrons.InputTag = cms.InputTag('selectedPatElectronsPFlow')
    process.rootTuplePFElectrons.Prefix = cms.string('selectedPatElectronsPFlow.')
    #non-isolated PF electrons
    process.rootTuplePFLooseElectrons.InputTag = cms.InputTag('selectedPatElectronsLoosePFlow')
    process.rootTuplePFLooseElectrons.Prefix = cms.string('selectedPatElectronsLoosePFlow.')
    #muons
    process.nTupleMuons.InputTag = cms.InputTag('selectedPatMuons')
    process.nTupleMuons.Prefix = cms.string('selectedPatMuons.')
    #standard PF muons
    process.nTuplePFMuons.InputTag = cms.InputTag('selectedPatMuonsPFlow')
    process.nTuplePFMuons.Prefix = cms.string('selectedPatMuonsPFlow.')
    #non isolated PF muons
    process.nTuplePFLooseMuons.InputTag = cms.InputTag('selectedPatMuonsLoosePFlow')
    process.nTuplePFLooseMuons.Prefix = cms.string('selectedPatMuonsLoosePFlow.')
    #PF taus
    process.rootTupleTaus.InputTag = cms.InputTag('selectedPatTausPFlow')
    process.rootTupleTaus.Prefix = cms.string('selectedPatTausPFlow.')
    #PF photons
    process.rootTuplePhotons.InputTag = cms.InputTag('patPhotons')
    process.rootTuplePhotons.Prefix = cms.string('patPhotons.')
    #trigger and trigger objects
    process.rootTupleTrigger.HLTInputTag = cms.InputTag('TriggerResults', '', options.hltProcess)
    process.rootTupleTriggerObjectElectronLeg.HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD', '', options.hltProcess)
    process.rootTupleTriggerObjectElectronIsoLeg.HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD', '', options.hltProcess)
    process.rootTupleTriggerObjectHadronLeg.HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD', '', options.hltProcess)
    process.rootTupleTriggerObjectHadronIsoLeg.HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD', '', options.hltProcess)
    process.rootTupleTriggerObjectHadronPFIsoLeg.HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD', '', options.hltProcess)
    process.rootTupleTriggerObjectSingleElectron.HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD', '', options.hltProcess)
    process.rootTupleTriggerObjectMuon1.HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD', '', options.hltProcess)
    process.rootTupleTriggerObjectMuon2.HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD', '', options.hltProcess)
    process.rootTupleTriggerObjectMuon2p1.HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD', '', options.hltProcess)
    process.rootTupleTriggerObjectMuon2012.HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD', '', options.hltProcess)
    process.rootTupleTriggerObjectMuon2012Rho.HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD', '', options.hltProcess)
    process.rootTupleTriggerObjectQuadJets.HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD', '', options.hltProcess)
    #GEN event
    process.rootTupleGenEventInfo.StorePDFWeights = cms.bool(options.storePDFWeights)
    process.rootTupleGenEventInfo.isTTbarMC = cms.bool(options.isTTbarMC)
    
    process.rootTupleTree = cms.EDAnalyzer("RootTupleMakerV2_Tree",
        treeName = cms.string('tree'),
        outputCommands=cms.untracked.vstring(
           'drop *',
            #EventContent
            'keep *_rootTupleEvent_*_*',
            #PF jets
            'keep *_rootTuplePF2PATJets_*_*',
            #electrons
            'keep *_rootTupleElectrons_*_*',
            'keep *_rootTuplePFElectrons_*_*',
            'keep *_rootTuplePFLooseElectrons_*_*',
            #MET
            'keep *_rootTupleRecoPFMET_*_*',
            'keep *_rootTupleCaloMET_*_*',
            'keep *_rootTuplePFMET_*_*',
            'keep *_rootTuplePFType1CorrectedMET_*_*',
            'keep *_rootTuplePFType1p2CorrectedMET_*_*',
            'keep *_rootTuplePFMet*_*_*',
            'keep *_rootTupleType1CorrectedPFMet*_*_*',
            'keep *_rootTupleType1p2CorrectedPFMet*_*_*',
            #MET corrections                                                                                                                                                                                                          
            'keep *_rootTupleSysShiftMetCorrections*_*_*',
            'keep *_rootTupleType0MetCorrections*_*_*',
            'keep *_rootTupleType1MetCorrections*_*_*',
            #muons
            'keep *_nTupleMuons_*_*',
            'keep *_nTuplePFMuons_*_*',
            'keep *_nTuplePFLooseMuons_*_*',
            #taus
            'keep *_rootTupleTaus_*_*',
            #photons
            'keep *_rootTuplePhotons_*_*',
            #trigger and trigger objects
            'keep *_rootTupleTrigger*_*_*',
            #vertices (DA)
            'keep *_rootTupleVertex_*_*',
            #gen information
            'keep *_rootTupleGenEventInfo_*_*',
            'keep *_rootTupleGenParticles_*_*',
            'keep *_rootTupleGenJets_*_*',
            'keep *_rootTupleGenMETTrue_*_*',
            # Global event variables
            'keep *_rootTupleGlobalEventVars_*_*',
        )
    )
    
    process.rootNTuples = cms.Sequence((
        #vertices
        process.rootTupleVertex + 
        #jets
        process.rootTuplePF2PATJets + 
        #electrons
        process.rootTupleElectrons + 
        process.rootTuplePFElectrons + 
        process.rootTuplePFLooseElectrons + 
        #muons
        process.nTuplePFMuons + 
        process.nTuplePFLooseMuons + 
        process.nTupleMuons + 
        #taus
        process.rootTupleTaus + 
        #photons
        process.rootTuplePhotons + 
        #MET
        process.rootTupleRecoPFMET + 
        process.rootTupleCaloMET + 
        process.rootTuplePFMET + 
        process.rootTuplePFType1CorrectedMET +
        process.rootTuplePFType1p2CorrectedMET +
        process.rootTuplePFType1p2CorrectedMetPFlow +
        #MET corrections
        process.rootTupleSysShiftMetCorrections +
        process.rootTupleType0MetCorrections +
        process.rootTupleType1MetCorrections +
        #MET uncertainties
        process.rootTuplePFMetElectronEnUp +
        process.rootTuplePFMetElectronEnDown +
        process.rootTuplePFMetMuonEnUp +
        process.rootTuplePFMetMuonEnDown +
        process.rootTuplePFMetTauEnUp +
        process.rootTuplePFMetTauEnDown +
        process.rootTuplePFMetJetResUp +
        process.rootTuplePFMetJetResDown +
        process.rootTuplePFMetJetEnUp +
        process.rootTuplePFMetJetEnDown +
        process.rootTuplePFMetUnclusteredEnUp +
        process.rootTuplePFMetUnclusteredEnDown +
        #Type 1 MET uncertainties
        process.rootTupleType1CorrectedPFMetElectronEnUp +
        process.rootTupleType1CorrectedPFMetElectronEnDown +
        process.rootTupleType1CorrectedPFMetMuonEnUp +
        process.rootTupleType1CorrectedPFMetMuonEnDown +
        process.rootTupleType1CorrectedPFMetTauEnUp +
        process.rootTupleType1CorrectedPFMetTauEnDown +
        process.rootTupleType1CorrectedPFMetJetResUp +
        process.rootTupleType1CorrectedPFMetJetResDown +
        process.rootTupleType1CorrectedPFMetJetEnUp +
        process.rootTupleType1CorrectedPFMetJetEnDown +
        process.rootTupleType1CorrectedPFMetUnclusteredEnUp +
        process.rootTupleType1CorrectedPFMetUnclusteredEnDown +
        #Type 1 + 2 MET uncertainties
        process.rootTupleType1p2CorrectedPFMetElectronEnUp +
        process.rootTupleType1p2CorrectedPFMetElectronEnDown +
        process.rootTupleType1p2CorrectedPFMetMuonEnUp +
        process.rootTupleType1p2CorrectedPFMetMuonEnDown +
        process.rootTupleType1p2CorrectedPFMetTauEnUp +
        process.rootTupleType1p2CorrectedPFMetTauEnDown +
        process.rootTupleType1p2CorrectedPFMetJetResUp +
        process.rootTupleType1p2CorrectedPFMetJetResDown +
        process.rootTupleType1p2CorrectedPFMetJetEnUp +
        process.rootTupleType1p2CorrectedPFMetJetEnDown +
        process.rootTupleType1p2CorrectedPFMetUnclusteredEnUp +
        process.rootTupleType1p2CorrectedPFMetUnclusteredEnDown +
        #Event
        process.rootTupleEvent + 
        #trigger and trigger objects
        process.rootTupleTrigger + 
        process.rootTupleTriggerObjectElectronLeg + 
        process.rootTupleTriggerObjectElectronIsoLeg + 
        process.rootTupleTriggerObjectHadronLeg + 
        process.rootTupleTriggerObjectHadronIsoLeg + 
        process.rootTupleTriggerObjectHadronPFIsoLeg + 
        process.rootTupleTriggerObjectSingleElectron +
        process.rootTupleTriggerObjectMuon1 + 
        process.rootTupleTriggerObjectMuon2 + 
        process.rootTupleTriggerObjectMuon2p1 + 
        process.rootTupleTriggerObjectMuon2012 + 
        process.rootTupleTriggerObjectMuon2012Rho + 
        process.rootTupleTriggerObjectQuadJets + 
        #genEventInfos
        process.rootTupleGenEventInfo + 
        process.rootTupleGenParticles + 
        process.rootTupleGenJetSequence + 
        process.rootTupleGenMETTrue) * 
                                       
        process.rootTupleTree)
    
    
    if options.useData:
        process.rootNTuples.remove(process.rootTupleGenEventInfo)
        process.rootNTuples.remove(process.rootTupleGenParticles)
        process.rootNTuples.remove(process.rootTupleGenJetSequence)
        process.rootNTuples.remove(process.rootTupleGenMETTrue)
        process.rootNTuples.remove(process.rootTuplePFMetJetResUp)
        process.rootNTuples.remove(process.rootTuplePFMetJetResDown)
        process.rootNTuples.remove(process.rootTupleType1CorrectedPFMetJetResUp)
        process.rootNTuples.remove(process.rootTupleType1CorrectedPFMetJetResDown)
        process.rootNTuples.remove(process.rootTupleType1p2CorrectedPFMetJetResUp)
        process.rootNTuples.remove(process.rootTupleType1p2CorrectedPFMetJetResDown)
        process.rootNTuples.remove(process.eventWeightPU)
        
    if not options.writeFat:#write only PF particles
        process.rootNTuples.remove(process.rootTupleCaloMET)
        process.rootNTuples.remove(process.rootTupleElectrons)
        process.rootNTuples.remove(process.nTupleMuons)
        process.rootNTuples.remove(process.rootTuplePhotons)
        
    if not options.writeFat and not options.writeIsolatedPFLeptons:#write only PF particles
        #isolated leptons
        process.rootNTuples.remove(process.rootTuplePFElectrons)
        process.rootNTuples.remove(process.nTuplePFMuons)

    if not options.writeTriggerObjects:
        process.rootNTuples.remove(process.rootTupleTriggerObjectElectronLeg)
        process.rootNTuples.remove(process.rootTupleTriggerObjectElectronIsoLeg)
        process.rootNTuples.remove(process.rootTupleTriggerObjectHadronLeg)
        process.rootNTuples.remove(process.rootTupleTriggerObjectHadronIsoLeg)
        process.rootNTuples.remove(process.rootTupleTriggerObjectHadronPFIsoLeg)
        process.rootNTuples.remove(process.rootTupleTriggerObjectSingleElectron)
        process.rootNTuples.remove(process.rootTupleTriggerObjectMuon1)
        process.rootNTuples.remove(process.rootTupleTriggerObjectMuon2)
        process.rootNTuples.remove(process.rootTupleTriggerObjectMuon2p1)
        process.rootNTuples.remove(process.rootTupleTriggerObjectMuon2012)
        process.rootNTuples.remove(process.rootTupleTriggerObjectMuon2012Rho)
        process.rootNTuples.remove(process.rootTupleTriggerObjectQuadJets)


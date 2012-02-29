
def createSkim(process, skim, cms):
    skim = skim.lower()
    if 'electron' in skim or 'lepton' in skim:
        process.EventFilter.maxAbsElectronEta   = cms.double(2.5)#within tracker volume
        #electron multiplicity
        if 'di' in skim:
            process.EventFilter.minNElectrons       = cms.int32(2)
        else:
            process.EventFilter.minNElectrons       = cms.int32(1)
        
        if 'loose' in skim:#loose Pt cut
            process.EventFilter.minElectronPt       = cms.double(20.)
            process.EventFilter.electronInput = cms.InputTag("selectedPatElectrons")#GSF electrons
        else:
            process.EventFilter.minElectronPt       = cms.double(30.)
            process.EventFilter.electronInput = cms.InputTag("selectedPatElectronsLoosePFlow")
    
    if 'muon'  in skim or 'lepton' in skim:
        #muon multiplicity
        if 'di' in skim:
            process.EventFilter.minNMuons       = cms.int32(2)
        else:
            process.EventFilter.minNMuons       = cms.int32(1)
        if 'loose' in skim:#loose Pt cut and eta cut
            process.EventFilter.maxAbsMuonEta   = cms.double(2.5)#within tracker volume
            process.EventFilter.minMuonPt       = cms.double(10.)
            process.EventFilter.muonInput = cms.InputTag("selectedPatMuons")
        else:
            process.EventFilter.minMuonPt       = cms.double(20.)#triggers are 17GeV
            process.EventFilter.maxAbsMuonEta   = cms.double(2.1)#new triggers have this restriction anyway
            process.EventFilter.muonInput = cms.InputTag("selectedPatMuonsLoosePFlow")
    
    if 'lepton' in skim:
        process.EventFilter.counteitherleptontype = cms.untracked.bool(True)
 
    #jet skim
    #unprescaled triggers are >=3/>=2 jets for electron/muon triggers
    if 'jet' in skim:
        find = skim.find('jet')
        nJets = int(skim[find - 1])
        process.EventFilter.jetInput = cms.InputTag("selectedPatJetsPFlow")
        process.EventFilter.minNJets = cms.int32(nJets)
        process.EventFilter.minJetPt = cms.double(30.)# identical (within JEC) to trigger
        process.EventFilter.maxAbsJetEta = cms.double(2.6)# identical to trigger
    
    
    if not (skim == '' or skim == 'noskim'):
        print '='*10, 'Skim definition', '='*10
        print 'Electron skim:'
        print '\t >=', str(process.EventFilter.minNMuons),' electron with ',
        print 'p_T > ', str(process.EventFilter.minElectronPt),
        print '|eta| < ' , str(process.EventFilter.maxAbsElectronEta)
        print '\t input collection:', str(process.EventFilter.electronInput)
        print
        print 'Muon skim:'
        print '\t >=', str(process.EventFilter.minNElectrons),' muon with ',
        print 'p_T > ', str(process.EventFilter.minMuonPt),
        print '|eta| < ' , str(process.EventFilter.maxAbsMuonEta)
        print '\t input collection:', str(process.EventFilter.muonInput)
        print
        print 'Use either lepton type:', str(process.EventFilter.counteitherleptontype)
        print
        print 'Jet skim:'
        print '\t >=', str(process.EventFilter.minNJets),' jet with ',
        print 'p_T > ', str(process.EventFilter.minJetPt),
        print '|eta| < ' , str(process.EventFilter.maxAbsJetEta)
        print '\t input collection:', str(process.EventFilter.jetInput)
    else:
        print 'No skim used.'

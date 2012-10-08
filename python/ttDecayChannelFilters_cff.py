import FWCore.ParameterSet.Config as cms

from TopQuarkAnalysis.TopSkimming.TtDecayChannelFilter_cfi import ttDecayChannelFilter

## fully-hadronic decay
ttFullHadronicFilter = ttDecayChannelFilter.clone()
ttFullHadronicFilter.allowedTopDecays.decayBranchA.electron = False
ttFullHadronicFilter.allowedTopDecays.decayBranchA.muon     = False
ttFullHadronicFilter.allowedTopDecays.decayBranchA.tau      = False
ttFullHadronicFilter.allowedTopDecays.decayBranchB.electron = False
ttFullHadronicFilter.allowedTopDecays.decayBranchB.muon     = False
ttFullHadronicFilter.allowedTopDecays.decayBranchB.tau      = False

## full-leptonic decay
ttFullLeptonicFilter = ttFullHadronicFilter.clone()
ttFullLeptonicFilter.allowedTopDecays.decayBranchA.electron = True
ttFullLeptonicFilter.allowedTopDecays.decayBranchA.muon     = True
ttFullLeptonicFilter.allowedTopDecays.decayBranchB.electron = True
ttFullLeptonicFilter.allowedTopDecays.decayBranchB.muon     = True
ttFullLeptonicFilter.allowedTopDecays.decayBranchA.tau      = True
ttFullLeptonicFilter.allowedTopDecays.decayBranchB.tau      = True

## semi-leptonic-tau decay
ttSemiLeptonicElectronFilter = ttFullHadronicFilter.clone()
ttSemiLeptonicElectronFilter.allowedTopDecays.decayBranchA.electron = True
## semi-leptonic-tau decay
ttSemiLeptonicMuonFilter = ttFullHadronicFilter.clone()
ttSemiLeptonicMuonFilter.allowedTopDecays.decayBranchA.muon = True
## semi-leptonic-tau decay
ttSemiLeptonicTauFilter = ttFullHadronicFilter.clone()
ttSemiLeptonicTauFilter.allowedTopDecays.decayBranchA.tau = True

#more di-leptonic filters
ttFullLeptonicEEFilter = ttFullHadronicFilter.clone()
ttFullLeptonicEEFilter.allowedTopDecays.decayBranchA.electron = True
ttFullLeptonicEEFilter.allowedTopDecays.decayBranchB.electron = True

ttFullLeptonicMuMuFilter = ttFullHadronicFilter.clone()
ttFullLeptonicMuMuFilter.allowedTopDecays.decayBranchA.muon = True
ttFullLeptonicMuMuFilter.allowedTopDecays.decayBranchB.muon = True

ttFullLeptonicTauTauFilter = ttFullHadronicFilter.clone()
ttFullLeptonicTauTauFilter.allowedTopDecays.decayBranchA.tau = True
ttFullLeptonicTauTauFilter.allowedTopDecays.decayBranchB.tau = True
#mixed leptons
ttFullLeptonicETauFilter = ttFullHadronicFilter.clone()
ttFullLeptonicETauFilter.allowedTopDecays.decayBranchA.electron = True
ttFullLeptonicETauFilter.allowedTopDecays.decayBranchB.tau = True

ttFullLeptonicEMuFilter = ttFullHadronicFilter.clone()
ttFullLeptonicEMuFilter.allowedTopDecays.decayBranchA.electron = True
ttFullLeptonicEMuFilter.allowedTopDecays.decayBranchB.muon = True
#more di-leptonic filters
ttFullLeptonicMuTauFilter = ttFullHadronicFilter.clone()
ttFullLeptonicMuTauFilter.allowedTopDecays.decayBranchA.muon = True
ttFullLeptonicMuTauFilter.allowedTopDecays.decayBranchB.tau = True


import FWCore.ParameterSet.Config as cms

#
# std filters for specific ttbar decays 
#

import TopQuarkAnalysis.TopSkimming.TtDecayChannelFilter_cfi

## fully-hadronic decay
ttFullHadronicFilter = TopQuarkAnalysis.TopSkimming.TtDecayChannelFilter_cfi.ttDecayChannelFilter.clone()
ttFullHadronicFilter.allowedTopDecays.decayBranchA.electron = False
ttFullHadronicFilter.allowedTopDecays.decayBranchA.muon     = False
ttFullHadronicFilter.allowedTopDecays.decayBranchB.electron = False
ttFullHadronicFilter.allowedTopDecays.decayBranchB.muon     = False

## full-leptonic decay
ttFullLeptonicFilter = TopQuarkAnalysis.TopSkimming.TtDecayChannelFilter_cfi.ttDecayChannelFilter.clone()
ttFullLeptonicFilter.allowedTopDecays.decayBranchA.electron = True
ttFullLeptonicFilter.allowedTopDecays.decayBranchA.muon     = True
ttFullLeptonicFilter.allowedTopDecays.decayBranchB.electron = True
ttFullLeptonicFilter.allowedTopDecays.decayBranchB.muon     = True

## semi-leptonic-tau decay
ttSemiLeptonicElectronFilter = TopQuarkAnalysis.TopSkimming.TtDecayChannelFilter_cfi.ttDecayChannelFilter.clone()
ttSemiLeptonicElectronFilter.allowedTopDecays.decayBranchA.electron = True
## semi-leptonic-tau decay
ttSemiLeptonicMuonFilter = TopQuarkAnalysis.TopSkimming.TtDecayChannelFilter_cfi.ttDecayChannelFilter.clone()
ttSemiLeptonicMuonFilter.allowedTopDecays.decayBranchA.muon = True
## semi-leptonic-tau decay
ttSemiLeptonicTauFilter = TopQuarkAnalysis.TopSkimming.TtDecayChannelFilter_cfi.ttDecayChannelFilter.clone()
ttSemiLeptonicTauFilter.allowedTopDecays.decayBranchA.tau = True
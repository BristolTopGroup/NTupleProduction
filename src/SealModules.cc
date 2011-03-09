#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_CaloJets_Extra.h"
#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_GenJets_Extra.h"
#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_GenMET_Extra.h"
#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_MET_Extra.h"
#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_Muons_Extra.h"
#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_Electrons_Extra.h"
#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_BeamSpot.h"
#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_Tracks.h"
#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_PFJets_Extra.h"
#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_Event_Extra.h"

DEFINE_FWK_MODULE(RootTupleMakerV2_CaloJets_Extra);
DEFINE_FWK_MODULE(RootTupleMakerV2_GenJets_Extra);
DEFINE_FWK_MODULE(RootTupleMakerV2_GenMET_Extra);
DEFINE_FWK_MODULE(RootTupleMakerV2_MET_Extra);
DEFINE_FWK_MODULE(RootTupleMakerV2_Muons_Extra);
DEFINE_FWK_MODULE(RootTupleMakerV2_BeamSpot);
DEFINE_FWK_MODULE(RootTupleMakerV2_Tracks);
DEFINE_FWK_MODULE(RootTupleMakerV2_Electrons_Extra);
DEFINE_FWK_MODULE(RootTupleMakerV2_PFJets_Extra);
DEFINE_FWK_MODULE(RootTupleMakerV2_Event_Extra);

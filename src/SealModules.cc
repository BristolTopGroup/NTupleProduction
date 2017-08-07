#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_Tree.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenJets.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenMET.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_RecoMET.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_MET.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_METcorrections.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Muons.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Electrons.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_PFJets.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Event.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenEventInfo.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Vertex.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Trigger.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_TriggerObjects.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenParticles.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GlobalEventVars.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_PFCandidates.h"

DEFINE_FWK_MODULE(RootTupleMakerV2_Tree);
DEFINE_FWK_MODULE(BristolNTuple_GenJets);
DEFINE_FWK_MODULE(BristolNTuple_GenMET);
DEFINE_FWK_MODULE(BristolNTuple_RecoMET);
DEFINE_FWK_MODULE(BristolNTuple_MET);
DEFINE_FWK_MODULE(BristolNTuple_METcorrections);
DEFINE_FWK_MODULE(BristolNTuple_Muons);
DEFINE_FWK_MODULE(BristolNTuple_Electrons);
DEFINE_FWK_MODULE(BristolNTuple_PFJets);
DEFINE_FWK_MODULE(BristolNTuple_Event);
DEFINE_FWK_MODULE(BristolNTuple_GenEventInfo);
DEFINE_FWK_MODULE(BristolNTuple_Vertex);
DEFINE_FWK_MODULE(BristolNTuple_Trigger);
DEFINE_FWK_MODULE(BristolNTuple_TriggerObjects);
DEFINE_FWK_MODULE(BristolNTuple_GenParticles);
DEFINE_FWK_MODULE(BristolNTuple_GlobalEventVars);
DEFINE_FWK_MODULE(BristolNTuple_PFCandidates);


#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_CaloJets.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenJets.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenMET.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_MET.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Muons.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Electrons.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_BeamSpot.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Tracks.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_PFJets.h"
#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Event.h"

DEFINE_FWK_MODULE(BristolNTuple_CaloJets);
DEFINE_FWK_MODULE(BristolNTuple_GenJets);
DEFINE_FWK_MODULE(BristolNTuple_GenMET);
DEFINE_FWK_MODULE(BristolNTuple_MET);
DEFINE_FWK_MODULE(BristolNTuple_Muons);
DEFINE_FWK_MODULE(BristolNTuple_BeamSpot);
DEFINE_FWK_MODULE(BristolNTuple_Tracks);
DEFINE_FWK_MODULE(BristolNTuple_Electrons);
DEFINE_FWK_MODULE(BristolNTuple_PFJets);
DEFINE_FWK_MODULE(BristolNTuple_Event);

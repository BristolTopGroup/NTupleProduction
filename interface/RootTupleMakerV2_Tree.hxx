#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_Tree.h"
#include "FWCore/Utilities/interface/InputTag.h"

template<class T>
void RootTupleMakerV2_Tree::registerBranch(edm::BranchDescription const* branchDesc, const std::string& type) {
	connectors_.push_back(new TypedBranchConnector<T>(branchDesc, type.c_str(), tree_));
	consumes < T > (edm::InputTag(branchDesc->moduleLabel(), branchDesc->productInstanceName()));
}

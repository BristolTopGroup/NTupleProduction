#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_Tree.h"

template<class T>
void RootTupleMakerV2_Tree::registerBranch(edm::BranchDescription const* branchDesc, const std::string& type) {
	connectors.push_back(new TypedBranchConnector<T>(branchDesc, type.c_str(), tree));
}

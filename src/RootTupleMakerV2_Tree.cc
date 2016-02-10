#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_Tree.h"

#include "FWCore/Framework/interface/ConstProductRegistry.h"
#include "FWCore/Framework/interface/ProductSelector.h"
#include "FWCore/Framework/interface/ProductSelectorRules.h"
#include "DataFormats/Provenance/interface/SelectedProducts.h"
#include "Math/LorentzVector.h"
#include "Math/Vector3D.h"

#include <map>
#include "boost/foreach.hpp"
#include <TBranch.h>
#include <TLorentzVector.h>

RootTupleMakerV2_Tree::RootTupleMakerV2_Tree(const edm::ParameterSet& iConfig) :
				treeName_(iConfig.getParameter < std::string > ("treeName")),
				pset_(iConfig) {
	registerBranches();
}

void RootTupleMakerV2_Tree::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
	for (BranchConnector * connector : connectors_) {
		connector->connect(iEvent);
	}
	tree_->Fill();
}

template<class T>
void RootTupleMakerV2_Tree::TypedBranchConnector<T>::connect(const edm::Event& iEvent) {
	edm::Handle < T > handle;
	iEvent.getByLabel(moduleLabel_, productInstanceName_, handle);
	object_ = *handle;
}

template<class T>
RootTupleMakerV2_Tree::TypedBranchConnector<T>::TypedBranchConnector(edm::BranchDescription const* desc, std::string t,
		TTree * tree) :
				moduleLabel_(desc->moduleLabel()),
				productInstanceName_(desc->productInstanceName()) {
	object_ptr_ = &object_;
	std::string s = productInstanceName_ + t;
	if (t != "") {
		tree->Branch(productInstanceName_.c_str(), object_ptr_, s.c_str());
	} //raw type
	else {
		tree->Branch(productInstanceName_.c_str(), &object_ptr_);
	} //vector<type>
}

void RootTupleMakerV2_Tree::beginJob() {
}

void RootTupleMakerV2_Tree::registerBranches() {
	tree_ = fs_->make < TTree > (treeName_.c_str(), "");

	typedef std::map<std::string, bool> mapStringBool;
	typedef std::map<std::string, int> mapStringInt;
	typedef std::map<std::string, std::string> mapStringString;
	typedef std::map<std::string, std::vector<float> > mapStringDoubles;
	typedef std::vector<std::vector<float> > vectorVectorFloats;
	typedef std::vector<std::vector<int> > vectorVectorInts;
	typedef std::vector<std::vector<bool> > vectorVectorBools;
	typedef std::vector<std::vector<std::string> > vectorVectorStrings;

	std::map < std::string, LEAFTYPE > leafmap;
	leafmap["bool"] = BOOL;
	leafmap["bools"] = BOOL_V;
	leafmap["short int"] = SHORT;
	leafmap["shorts"] = SHORT_V;
	leafmap["ushort int"] = U_SHORT;
	leafmap["ushorts"] = U_SHORT_V;
	leafmap["int"] = INT;
	leafmap["ints"] = INT_V;
	leafmap["uint"] = U_INT;
	leafmap["uints"] = U_INT_V;
	leafmap["float"] = FLOAT;
	leafmap["floats"] = FLOAT_V;
	leafmap["double"] = DOUBLE;
	leafmap["doubles"] = DOUBLE_V;
	leafmap["lint"] = LONG;
	leafmap["longs"] = LONG_V;
	leafmap["ulint"] = U_LONG;
	leafmap["ulongs"] = U_LONG_V;
	leafmap["StringStringstdmap"] = STRING_STRING_M;
	leafmap["Stringboolstdmap"] = STRING_BOOL_M;
	leafmap["Stringintstdmap"] = STRING_INT_M;
	leafmap["Stringfloatsstdmap"] = STRING_FLOAT_V_M;
	leafmap["floatss"] = FLOAT_V_V;
	leafmap["intss"] = INT_V_V;
	leafmap["boolss"] = BOOL_V_V;
	leafmap["Stringss"] = STRING_V_V;
	// leafmap[""] = LORENTZ_V_V;

	//
	leafmap["String"] = STRING;
	leafmap["Strings"] = STRING_V;

	edm::Service < edm::ConstProductRegistry > reg;
	edm::SelectedProducts allBranches = reg->allBranchDescriptions();
	edm::ProductSelectorRules groupSelectorRules_(pset_, "outputCommands", "RootTupleMakerV2_Tree");
	edm::ProductSelector groupSelector_;
	groupSelector_.initialize(groupSelectorRules_, allBranches);

	std::set < std::string > branchnames;

	for (auto const& selection : allBranches) {
		if (groupSelector_.selected(*selection)) {

			//Check for duplicate branch names
			if (branchnames.find(selection->productInstanceName()) != branchnames.end()) {
				throw edm::Exception(edm::errors::Configuration) << "More than one branch named: "
						<< selection->productInstanceName() << std::endl
						<< "Exception thrown from RootTupleMakerV2_Tree::beginJob" << std::endl;
			} else {
				branchnames.insert(selection->productInstanceName());
			}

			//Create RootTupleMakerV2_Tree branch
			switch (leafmap.find(selection->friendlyClassName())->second) {
			case BOOL:
				registerBranch<bool>(selection, "/O");
				break;
			case BOOL_V:
				registerBranch < std::vector<bool> > (selection, "");
				break;
			case INT:
				registerBranch<int>(selection, "/I");
				break;
			case INT_V:
				registerBranch < std::vector<int> > (selection, "");
				break;
			case U_INT:
				registerBranch<unsigned int>(selection, "/i");
				break;
			case U_INT_V:
				registerBranch < std::vector<unsigned int> > (selection, "");
				break;
			case SHORT:
				registerBranch<short>(selection, "/S");
				break;
			case SHORT_V:
				registerBranch < std::vector<short> > (selection, "");
				break;
			case U_SHORT:
				registerBranch<unsigned short>(selection, "/s");
				break;
			case U_SHORT_V:
				registerBranch < std::vector<unsigned short> > (selection, "");
				break;
			case FLOAT:
				registerBranch<float>(selection, "/F");
				break;
			case FLOAT_V:
				registerBranch < std::vector<float> > (selection, "");
				break;
			case DOUBLE:
				registerBranch<double>(selection, "/D");
				break;
			case DOUBLE_V:
				registerBranch < std::vector<double> > (selection, "");
				break;
			case LONG:
				registerBranch<long>(selection, "/L");
				break;
			case LONG_V:
				registerBranch < std::vector<long> > (selection, "");
				break;
			case U_LONG:
				registerBranch<unsigned long>(selection, "/l");
				break;
			case U_LONG_V:
				registerBranch < std::vector<unsigned long> > (selection, "");
				break;
			case STRING:
				registerBranch < std::string > (selection, "");
				break;
			case STRING_V:
				registerBranch < std::vector<std::string> > (selection, "");
				break;

			case STRING_INT_M:
				registerBranch < mapStringInt > (selection, "");
				break;
			case STRING_BOOL_M:
				registerBranch < mapStringBool > (selection, "");
				break;
			case STRING_STRING_M:
				registerBranch < mapStringString > (selection, "");
				break;
			case STRING_FLOAT_V_M:
				registerBranch < mapStringDoubles > (selection, "");
				break;
			case FLOAT_V_V:
				registerBranch < vectorVectorFloats > (selection, "");
				break;
			case INT_V_V:
				registerBranch < vectorVectorInts > (selection, "");
				break;
			case BOOL_V_V:
				registerBranch < vectorVectorBools > (selection, "");
				break;
			case STRING_V_V:
				registerBranch < vectorVectorStrings > (selection, "");
				break;

			default: {
				std::string leafstring = "";
				typedef std::pair<std::string, LEAFTYPE> pair_t;
				for (const pair_t& leaf : leafmap) {
					leafstring += "\t" + leaf.first + "\n";
				}

				throw edm::Exception(edm::errors::Configuration)
						<< "class RootTupleMakerV2_Tree does not handle leaves of type " << selection->className()
						<< " like\n" << selection->friendlyClassName() << "_" << selection->moduleLabel() << "_"
						<< selection->productInstanceName() << "_" << selection->processName() << std::endl
						<< "Valid leaf types are (friendlyClassName):\n" << leafstring
						<< "Exception thrown from RootTupleMakerV2_Tree::beginJob\n";
			}
			}
		}
	}
}



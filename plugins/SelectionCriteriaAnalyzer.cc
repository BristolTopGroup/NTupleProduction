#include "BristolAnalysis/NTupleTools/plugins/SelectionCriteriaAnalyzer.h"
#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"

// system include files
#include <memory>
#include <iostream>



using namespace edm;
using namespace std;


SelectionCriteriaAnalyzer::SelectionCriteriaAnalyzer(const edm::ParameterSet& iConfig) :
		// Input tags
		selectionCriteriaInput_(iConfig.getParameter < std::vector<edm::InputTag> > ("selectionCriteriaInput")) //
{
	produces< vector<unsigned int> >("passesSelection");
}

void SelectionCriteriaAnalyzer::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
}

SelectionCriteriaAnalyzer::~SelectionCriteriaAnalyzer() {

}

bool SelectionCriteriaAnalyzer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	
	std::auto_ptr< vector<unsigned int> > passesSelection(new vector<unsigned int>());


	bool passesAtLeastOneSelection = false;

	for (unsigned short selectionIndex = 0; selectionIndex < selectionCriteriaInput_.size(); ++selectionIndex) {
		bool passesThisSelection = passesFilter(iEvent, selectionCriteriaInput_.at(selectionIndex ));
		passesAtLeastOneSelection = passesAtLeastOneSelection || passesThisSelection;
		if ( passesThisSelection ) {
			passesSelection->push_back(selectionIndex+1);
		}
	}

	iEvent.put(passesSelection, "passesSelection");

	return passesAtLeastOneSelection;
}

// ------------ method called once each job just before starting event loop  ------------
void SelectionCriteriaAnalyzer::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void SelectionCriteriaAnalyzer::endJob() {
}

void SelectionCriteriaAnalyzer::beginRun(edm::Run& iRun, const edm::EventSetup& iSetup) {
}

//define this as a plug-in
DEFINE_FWK_MODULE (SelectionCriteriaAnalyzer);

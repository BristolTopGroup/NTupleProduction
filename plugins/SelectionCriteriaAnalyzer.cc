#include "BristolAnalysis/NTupleTools/plugins/SelectionCriteriaAnalyzer.h"
#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"

// system include files
#include <memory>
#include <iostream>



using namespace edm;
using namespace std;


SelectionCriteriaAnalyzer::SelectionCriteriaAnalyzer(const edm::ParameterSet& iConfig) {

    for (edm::InputTag const & tag : iConfig.getParameter< std::vector<edm::InputTag> > ("offlineSelectionCriteriaInput"))
    offlineSelectionCriteriaInput_.push_back(consumes<bool>(tag));
    for (edm::InputTag const & tag : iConfig.getParameter< std::vector<edm::InputTag> > ("genSelectionCriteriaInput"))
    genSelectionCriteriaInput_.push_back(consumes<bool>(tag));

	produces< vector<unsigned int> >("passesOfflineSelection");
	produces< vector<unsigned int> >("passesGenSelection");	
}

void SelectionCriteriaAnalyzer::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
}

SelectionCriteriaAnalyzer::~SelectionCriteriaAnalyzer() {

}

bool SelectionCriteriaAnalyzer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	
	std::auto_ptr< vector<unsigned int> > passesOfflineSelection(new vector<unsigned int>());
	std::auto_ptr< vector<unsigned int> > passesGenSelection(new vector<unsigned int>());


	bool passesAtLeastOneSelection = false;

	for (unsigned short selectionIndex = 0; selectionIndex < offlineSelectionCriteriaInput_.size(); ++selectionIndex) {
		bool passesSelection = passesFilter(iEvent, offlineSelectionCriteriaInput_.at(selectionIndex ));
		passesAtLeastOneSelection = passesAtLeastOneSelection || passesSelection;
		if ( passesSelection ) {
			passesOfflineSelection->push_back(selectionIndex+1);
		}
	}

	for (unsigned short selectionIndex = 0; selectionIndex < genSelectionCriteriaInput_.size(); ++selectionIndex) {
		bool passesSelection = passesFilter(iEvent, genSelectionCriteriaInput_.at(selectionIndex ));
		passesAtLeastOneSelection = passesAtLeastOneSelection || passesSelection;
		if ( passesSelection ) {
			passesGenSelection->push_back(selectionIndex+1);
		}
	}

	iEvent.put(passesOfflineSelection, "passesOfflineSelection");
	iEvent.put(passesGenSelection, "passesGenSelection");

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

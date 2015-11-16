#include "BristolAnalysis/NTupleTools/plugins/SelectionAnalyser.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"

using namespace edm;
using namespace std;

SelectionAnalyser::SelectionAnalyser(const edm::ParameterSet& iConfig) :
		// PUWeightInput_(iConfig.getParameter < edm::InputTag > ("PUWeightInput")), //
//		BtagWeightInput_(iConfig.getParameter < edm::InputTag > ("BtagWeightInput")), //
		selectionFlags_(iConfig.getParameter < vector<InputTag> > ("selectionFlags")), //
		selectionNames_(iConfig.getParameter < vector<string> > ("selectionNames")), //
		numberOfCuts_(selectionNames_.size()), //
		consecutiveCuts_(), //
		individualCuts_(), //
		consecutiveCuts_unweighted_(), //
		individualCuts_unweighted_() {

}

void SelectionAnalyser::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	// desc.add < InputTag > ("PUWeightInput");
//	desc.add < InputTag > ("BtagWeightInput");
	desc.add < vector<InputTag> > ("selectionFlags");
	desc.add < vector<string> > ("selectionNames");

	descriptions.add("SelectionAnalyser", desc);
}

void SelectionAnalyser::beginJob() {
	edm::Service < TFileService > fs;

	// Histograms for PU Events

	consecutiveCuts_ = fs->make < TH1F
			> ("consecutiveCuts", "Selection cutflow; ;# Events", numberOfCuts_ , -0.5, numberOfCuts_ - 0.5);
	individualCuts_ = fs->make < TH1F
			> ("individualCuts", "Selection cutflow; ;# Events", numberOfCuts_ , -0.5, numberOfCuts_ - 0.5);
	consecutiveCuts_unweighted_ = fs->make < TH1F
			> ("consecutiveCuts_unweighted", "Selection cutflow; ;# Events", numberOfCuts_ , -0.5, numberOfCuts_
					- 0.5);
	individualCuts_unweighted_ = fs->make < TH1F
			> ("individualCuts_unweighted", "Selection cutflow; ;# Events", numberOfCuts_ , -0.5, numberOfCuts_
					- 0.5);

	consecutiveCuts_->Sumw2();
	individualCuts_->Sumw2();
	consecutiveCuts_unweighted_->Sumw2();
	individualCuts_unweighted_->Sumw2();

	//setting bin names
	for (unsigned int cut = 0; cut < numberOfCuts_; ++cut) {
		consecutiveCuts_->GetXaxis()->SetBinLabel(cut + 1, selectionNames_.at(cut).c_str());
		individualCuts_->GetXaxis()->SetBinLabel(cut + 1, selectionNames_.at(cut).c_str());
		consecutiveCuts_unweighted_->GetXaxis()->SetBinLabel(cut + 1, selectionNames_.at(cut).c_str());
		individualCuts_unweighted_->GetXaxis()->SetBinLabel(cut + 1, selectionNames_.at(cut).c_str());
	}
}

void SelectionAnalyser::endJob() {

}

void SelectionAnalyser::analyze(const edm::Event& iEvent, const edm::EventSetup&) {

	edm::Handle < GenEventInfoProduct > genEvtInfoProduct;
	iEvent.getByLabel("generator", genEvtInfoProduct);
	double weight = 1;
	if (genEvtInfoProduct.isValid()) {
		// cout << "Gen weight : " << genEvtInfoProduct->weight() << endl;
		weight = genEvtInfoProduct->weight() / fabs( genEvtInfoProduct->weight() );
	}

	bool passesSelectionUpTo(true);
	for (unsigned int cut = 0; cut < numberOfCuts_; ++cut) {

		bool selectionResult = passesFilter(iEvent, selectionFlags_.at(cut));
		passesSelectionUpTo = passesSelectionUpTo && selectionResult;
		if (selectionResult) {
			individualCuts_->Fill(cut, weight);
			individualCuts_unweighted_->Fill(cut, 1.);
		}
		if (passesSelectionUpTo) {
			consecutiveCuts_->Fill(cut, weight);
			consecutiveCuts_unweighted_->Fill(cut, 1.);
		}
	}
}

DEFINE_FWK_MODULE (SelectionAnalyser);

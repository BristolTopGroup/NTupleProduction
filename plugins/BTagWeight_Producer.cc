#include "BristolAnalysis/NTupleTools/plugins/BTagWeight_Producer.h"
#include "BristolAnalysis/Tools/interface/BTagWeight.h"
#include "BristolAnalysis/Tools/interface/RecoObjects/Jet.h"
#include "BristolAnalysis/Tools/interface/GlobalVariables.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/MakerMacros.h"

using namespace edm;
using namespace std;

BTagWeight_Producer::BTagWeight_Producer(const edm::ParameterSet& iConfig) :
		numberOfTagsInput_(iConfig.getParameter < InputTag > ("numberOfTagsInput")), //
		jetInput_(iConfig.getParameter < InputTag > ("jetInput")), //
		prefix_(iConfig.getParameter < string > ("prefix")), //
		targetBtagMultiplicity_(iConfig.getParameter<unsigned int>("targetBtagMultiplicity")), //
		BJetSystematic_(iConfig.getParameter<int>("BJetSystematic")) {
	produces<double>();
}

void BTagWeight_Producer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	std::vector<double> bjetWeights;

	BAT::Globals::BJetSystematic = BJetSystematic_;

	edm::Handle<unsigned int> numberOfBtags;
	iEvent.getByLabel(numberOfTagsInput_, numberOfBtags);
	unsigned int numberOfBjets(*numberOfBtags);

	if (!iEvent.isRealData()) {
		//get jets and numberOfBtags
		edm::Handle < pat::JetCollection > jets;
		iEvent.getByLabel(jetInput_, jets);
		BAT::JetCollection batJets;
		//setup BAT::JetCollection
		for (unsigned int jetIndex = 0; jetIndex < jets->size(); ++jetIndex) {
			pat::Jet jet(jets->at(jetIndex));
			BAT::JetPointer batJet(new BAT::Jet(jet.energy(), jet.px(), jet.py(), jet.pz()));
			batJet->setPartonFlavour(jet.partonFlavour());
			batJets.push_back(batJet);
		}
		bjetWeights = BAT::BjetWeights(batJets, numberOfBjets);
	} else {
		for (unsigned int btag = 0; btag <= numberOfBjets; ++btag) {
			if (btag == numberOfBjets)
				bjetWeights.push_back(1.);
			else
				bjetWeights.push_back(0);
		}
	}

	double btagWeight(0.);
	//calculate inclusive weights
	for (unsigned int btag = targetBtagMultiplicity_; btag <= numberOfBjets; ++btag) {
		btagWeight += bjetWeights.at(btag);
	}

	std::auto_ptr<double> btagWeightProduct(new double(btagWeight));
	//-----------------------------------------------------------------
	iEvent.put(btagWeightProduct);
}

void BTagWeight_Producer::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add<InputTag> ("numberOfTagsInput");
	desc.add<InputTag> ("jetInput");
	desc.add<string> ("prefix", "BTagWeight_Producer");
	desc.add<unsigned int>("targetBtagMultiplicity", 0);
	desc.add<int>("BJetSystematic", 0);

	descriptions.add("BTagWeight_Producer", desc);
}

DEFINE_FWK_MODULE (BTagWeight_Producer);


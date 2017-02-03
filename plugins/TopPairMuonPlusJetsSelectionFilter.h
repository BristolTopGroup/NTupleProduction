#ifndef BristolTopPairMuonPlusJetsSelectionFilter
#define BristolTopPairMuonPlusJetsSelectionFilter

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include <boost/array.hpp>
#include <string>

namespace TTbarMuPlusJetsReferenceSelection {
enum Step {
	AllEvents,
	EventCleaningAndTrigger,
	ExactlyOneSignalMuon,
	LooseMuonVeto,
	LooseElectronVeto,
	AtLeastOneGoodJet,
	AtLeastTwoGoodJets,
	AtLeastThreeGoodJets,
	AtLeastFourGoodJets,
	AtLeastOneBtag,
	AtLeastTwoBtags,
	NUMBER_OF_SELECTION_STEPS
};

const std::string StringSteps[NUMBER_OF_SELECTION_STEPS] = { //
		"AllEvents", //
				"EventCleaningAndTrigger", //
				"ExactlyOneSignalMuon", //
				"LooseMuonVeto", //
				"LooseElectronVeto", //
				"AtLeastOneGoodJet", //
				"AtLeastTwoGoodJets", //
				"AtLeastThreeGoodJets", //
				"AtLeastFourGoodJets", //
				"AtLeastOneBtag", //
				"AtLeastTwoBtags" //
		};
}

class TopPairMuonPlusJetsSelectionFilter: public edm::EDFilter {
public:
	explicit TopPairMuonPlusJetsSelectionFilter(const edm::ParameterSet&);
	virtual ~TopPairMuonPlusJetsSelectionFilter();

	virtual void beginJob();
	virtual bool filter(edm::Event&, const edm::EventSetup&);
	virtual void endJob();
	virtual void beginRun();

	static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);

	virtual bool passesSelectionStep(edm::Event& iEvent, unsigned int selectionStep) const;

	virtual bool passesEventCleaning(edm::Event& iEvent) const;
	virtual bool passesTriggerSelection() const;
	virtual bool hasExactlyOneSignalMuon() const;
	virtual bool passesLooseMuonVeto() const;
	virtual bool passesLooseElectronVeto() const;
	virtual bool hasAtLeastOneGoodJet() const;
	virtual bool hasAtLeastTwoGoodJets() const;
	virtual bool hasAtLeastThreeGoodJets() const;
	virtual bool hasAtLeastFourGoodJets() const;
   	virtual bool hasExactlyZeroGoodBJet() const;
   	virtual bool hasExactlyOneGoodBJet() const;
	virtual bool hasAtLeastOneGoodBJet() const;
	virtual bool hasAtLeastTwoGoodBJets() const;

private:
	virtual void setupEventContent(edm::Event& iEvent, const edm::EventSetup& iSetup);

	//config
	edm::EDGetTokenT<pat::JetCollection> cleanedJetsToken_;
	edm::EDGetTokenT<pat::JetCollection> cleanedBJetsToken_;
	edm::EDGetToken vetoElectronsToken_;

	edm::EDGetTokenT<pat::MuonCollection> vetoMuonsToken_;
	edm::EDGetTokenT<pat::MuonCollection> goodMuonsToken_;
	edm::EDGetTokenT<pat::MuonCollection> muonsToken_;
	edm::EDGetTokenT<edm::TriggerResults> hltInputTag_;

	bool tagAndProbeStudies_, dropTriggerSelection_;

	std::string prefix_, MCSampleTag_;

	bool debug_, taggingMode_, bSelectionInTaggingMode_;

   	// Control region selections
	bool nonIsolatedMuonSelection1_, nonIsolatedMuonSelection2_;
	double looseMuonIso_, tightMuonIso_;
	//internal
	boost::array<bool, TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS> passes_;
	unsigned int runNumber_, signalMuonIndex_;
	bool isRealData_, hasSignalMuon_;
	pat::JetCollection cleanedJets_, cleanedBJets_;
	pat::ElectronCollection vetoElectrons_;
	pat::MuonCollection muons_, goodIsolatedMuons_, vetoMuons_;
	pat::Muon signalMuon_;
	HLTConfigProvider hltConfig_;
	edm::TriggerResults triggerResults_;

};

#endif


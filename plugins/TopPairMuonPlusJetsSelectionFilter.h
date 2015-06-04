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
#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
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
	virtual bool beginRun(edm::Run &, const edm::EventSetup &);

	static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);

	virtual bool isGoodJet(const pat::Jet& jet) const;
	virtual bool isGoodMuon(const pat::Muon& muon) const;
	//definitions of loose objects
	virtual bool isLooseElectron(const edm::Ptr<pat::Electron>& electron) const;
	virtual bool isLooseMuon(const pat::Muon& muon) const;
	virtual void getLooseElectrons();
	virtual void getLooseMuons();
	virtual void goodIsolatedMuons();
	virtual void cleanedJets();
	virtual void cleanedBJets();

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
	edm::InputTag jetInput_, electronInput_, muonInput_, hltInputTag_, VertexInput_;

	double minSignalMuonPt_, maxSignalMuonEta_;
	double minLooseMuonPt_, maxLooseMuonEta_, minLooseElectronPt_, maxLooseElectronEta_;
	edm::EDGetTokenT<edm::ValueMap<bool> > looseElectronIDMapToken_;
	double minLooseElectronID_;
	double min1JetPt_, min2JetPt_, min3JetPt_, min4JetPt_;
	double minBJetPt_;
	double minJetPtInNtuples_;

	double cleaningDeltaR_;

	const bool applyJEC_;
	const std::string jetCorrectionService_;
	const JetCorrector* corrector_;
	
	std::string bJetDiscriminator_;
	double minBJetDiscriminator_;

	double tightMuonIso_, controlMuonIso_;

	bool tagAndProbeStudies_, dropTriggerSelection_;

	std::string prefix_, MCSampleTag_;

	bool debug_, taggingMode_, bSelectionInTaggingMode_;

   	// Control region selections
	bool nonIsolatedMuonSelection_;

	//internal
	boost::array<bool, TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS> passes_;
	unsigned int runNumber_, signalMuonIndex_;
	bool isRealData_, hasSignalMuon_, hasGoodPV_;
	std::vector< unsigned int> cleanedJetIndex_, cleanedBJetIndex_;
	pat::JetCollection jets_, cleanedJets_, cleanedBJets_;
	edm::Handle <edm::View<pat::Electron> > electrons_;
	pat::ElectronCollection looseElectrons_;
    edm::ValueMap<bool> looseElectronIDDecisions_;
	pat::MuonCollection muons_, goodIsolatedMuons_, looseMuons_;
	pat::Muon signalMuon_;
	HLTConfigProvider hltConfig_;
	edm::TriggerResults triggerResults_;
	reco::Vertex primaryVertex_;

};

#endif


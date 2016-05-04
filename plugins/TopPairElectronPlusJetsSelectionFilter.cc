#include "BristolAnalysis/NTupleTools/plugins/TopPairElectronPlusJetsSelectionFilter.h"
#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
// system include files
#include <memory>
#include <iostream>
// user include files
#include "DataFormats/RecoCandidate/interface/IsoDepositDirection.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositVetos.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"
#include "EgammaAnalysis/ElectronTools/interface/ElectronEffectiveArea.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/METReco/interface/BeamHaloSummary.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"

using namespace edm;
using namespace std;
using namespace reco;
using namespace isodeposit;
using namespace pat;

TopPairElectronPlusJetsSelectionFilter::TopPairElectronPlusJetsSelectionFilter(const edm::ParameterSet& iConfig) :
		jetInput_(consumes<pat::JetCollection>(iConfig.getParameter < edm::InputTag > ("jetInput"))), //
		// electronInput_(consumes<pat::ElectronCollection>(iConfig.getParameter < edm::InputTag > ("electronInput"))), //
  		electronInput_(consumes<edm::View<pat::Electron>>(iConfig.getParameter < edm::InputTag > ("electronInput"))),			
		muonInput_(consumes<pat::MuonCollection>(iConfig.getParameter < edm::InputTag > ("muonInput"))), //
		hltInputTag_(consumes<edm::TriggerResults>(iConfig.getParameter < edm::InputTag > ("HLTInput"))), //
		vertexInputTag_(consumes<reco::VertexCollection>(iConfig.getParameter < edm::InputTag > ("VertexInputTag"))), //

		// Selection criteria
		minSignalElectronPt_(iConfig.getParameter<double>("minSignalElectronPt")), //
		maxSignalElectronEta_(iConfig.getParameter<double>("maxSignalElectronEta")), //
  		signalElectronIDMapToken_(consumes<ValueMap<bool> >(iConfig.getParameter<edm::InputTag>("signalElectronIDMap"))),
  		eleMediumIdFullInfoMapToken_(consumes<edm::ValueMap<vid::CutFlowResult> >(iConfig.getParameter<edm::InputTag>("signalElectronIDMap"))),		 

		minSignalElectronID_(iConfig.getParameter<double>("minSignalElectronID")), //
		minLooseMuonPt_(iConfig.getParameter<double>("minLooseMuonPt")), //
		maxLooseMuonEta_(iConfig.getParameter<double>("maxLooseMuonEta")), //
		minLooseElectronPt_(iConfig.getParameter<double>("minLooseElectronPt")), //
		maxLooseElectronEta_(iConfig.getParameter<double>("maxLooseElectronEta")), //
  		looseElectronIDMapToken_(consumes<ValueMap<bool> >(iConfig.getParameter<edm::InputTag>("looseElectronIDMap"))),

		minLooseElectronID_(iConfig.getParameter<double>("minLooseElectronID")), //

		min1JetPt_(iConfig.getParameter<double>("min1JetPt")), //
		min2JetPt_(iConfig.getParameter<double>("min2JetPt")), //
		min3JetPt_(iConfig.getParameter<double>("min3JetPt")), //
		min4JetPt_(iConfig.getParameter<double>("min4JetPt")), //
		minBJetPt_(iConfig.getParameter<double>("minBJetPt")), //
		minJetPtInNtuples_(iConfig.getParameter<double>("minJetPtInNtuples")), //

		cleaningDeltaR_(iConfig.getParameter<double>("cleaningDeltaR")), //

		applyJEC_(iConfig.getParameter < bool > ("applyJEC")), //
		jetCorrectionService_(iConfig.getParameter<std::string> ("JetCorrectionService")), //
		corrector_(0), //

		bJetDiscriminator_(iConfig.getParameter<std::string>("bJetDiscriminator")), //
		minBJetDiscriminator_(iConfig.getParameter<double>("minBJetDiscriminator")), //

		tightElectronIso_EB_(iConfig.getParameter<double>("tightElectronIsolation_EB")), //
		tightElectronIso_EE_(iConfig.getParameter<double>("tightElectronIsolation_EE")), //
		controlElectronIso_(iConfig.getParameter<double>("controlElectronIsolation")), //

        looseMuonIso_(iConfig.getParameter<double>("looseMuonIsolation")), //

		tagAndProbeStudies_(iConfig.getParameter<bool>("tagAndProbeStudies")), //
		dropTriggerSelection_(iConfig.getParameter<bool>("dropTriggerSelection")), //
		prefix_(iConfig.getUntrackedParameter < std::string > ("prefix")), //
		MCSampleTag_(iConfig.getParameter < std::string > ("MCSampleTag")), //
		debug_(iConfig.getUntrackedParameter<bool>("debug")), //
		taggingMode_(iConfig.getParameter<bool>("taggingMode")), //
		jetSelectionInTaggingMode_(iConfig.getParameter<bool>("jetSelectionInTaggingMode")), //
		bSelectionInTaggingMode_(iConfig.getParameter<bool>("bSelectionInTaggingMode")), //

		nonIsolatedElectronSelection_(iConfig.getParameter<bool>("nonIsolatedElectronSelection")), //
		invertedConversionSelection_(iConfig.getParameter<bool>("invertedConversionSelection")), //
		passes_(), //
		runNumber_(0), //
		signalElectronIndex_(999), //
		isRealData_(false), //
		hasSignalElectron_(false), //
		cleanedJetIndex_(),
		cleanedBJetIndex_(),
		jets_(), //,
		cleanedJets_(), //
		cleanedBJets_(), //
		electrons_(), //
		goodIsolatedElectrons_(), //
		looseElectrons_(), //
		muons_(), //
		looseMuons_(), //
		signalElectron_(), //
		vertices_(), //
		hltConfig_(), //
		triggerResults_() {
	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		passes_.at(step) = 0;
		produces<bool>(prefix_ + TTbarEPlusJetsReferenceSelection::StringSteps[step]);
	}
	produces<bool>(prefix_ + "FullSelection");
	produces<bool>(prefix_ + "FullSelectionNoB");
	produces<unsigned int>(prefix_ + "NumberOfJets");
	produces<unsigned int>(prefix_ + "NumberOfBtags");
	produces<std::vector<unsigned int> >(prefix_ + "cleanedJetIndex");
	produces<std::vector<unsigned int> >(prefix_ + "cleanedBJetIndex");
	// produces < pat::JetCollection > (prefix_ + "cleanedJets");
	produces<unsigned int>(prefix_ + "signalElectronIndex");
}

void TopPairElectronPlusJetsSelectionFilter::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("jetInput");
	desc.add < InputTag > ("electronInput");
	desc.add < InputTag > ("muonInput");
	desc.add < InputTag > ("HLTInput");
	desc.add < InputTag > ("VertexInputTag");

	desc.add<double>("minSignalElectronPt",0.);
	desc.add<double>("maxSignalElectronEta",10.);
	desc.add<double>("minSignalElectronID",0);
	desc.add < InputTag > ("signalElectronIDMap");
	desc.add < InputTag > ("looseElectronIDMap");
	desc.add<double>("minLooseMuonPt",0.);
	desc.add<double>("maxLooseMuonEta",10.);
	desc.add<double>("minLooseElectronPt",0.);
	desc.add<double>("maxLooseElectronEta",10.);
	desc.add<double>("minLooseElectronID",0);

	desc.add<double>("min1JetPt", 30.0);
	desc.add<double>("min2JetPt", 30.0);
	desc.add<double>("min3JetPt", 30.0);
	desc.add<double>("min4JetPt", 30.0);
	desc.add<double>("minBJetPt", 30.0);
	desc.add<double>("minJetPtInNtuples", 30.0);

	desc.add<double>("cleaningDeltaR", 0.3 );

	desc.add<bool>("applyJEC", false);
	desc.add<std::string>("JetCorrectionService", "");

	desc.add < std::string > ("bJetDiscriminator", "combinedSecondaryVertexBJetTags");
	desc.add<double>("minBJetDiscriminator", 0.679 );

	desc.add<double>("tightElectronIsolation_EB", 0.14);
	desc.add<double>("tightElectronIsolation_EE", 0.1649);

	desc.add<double>("controlElectronIsolation", 0.3);

	desc.add<double>("looseMuonIsolation", 0.2);

	desc.add<bool>("tagAndProbeStudies", false);
	desc.add<bool>("dropTriggerSelection", false);

	desc.add < std::string > ("MCSampleTag", "Summer12");
	desc.addUntracked < std::string > ("prefix", "TopPairElectronPlusJetsSelection.");
	desc.addUntracked<bool>("debug", false);
	desc.add<bool>("taggingMode", false);
	desc.add<bool>("bSelectionInTaggingMode", false);
	desc.add<bool>("jetSelectionInTaggingMode", false);
   	desc.add<bool>("nonIsolatedElectronSelection", false);
   	desc.add<bool>("invertedConversionSelection", false);
	descriptions.add("applyTopPairElectronPlusJetsSelection", desc);
}

TopPairElectronPlusJetsSelectionFilter::~TopPairElectronPlusJetsSelectionFilter() {

}

bool TopPairElectronPlusJetsSelectionFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	// Get content from event
	// Including selecting a signal electron, loose leptons, jets and bjets
	setupEventContent(iEvent, iSetup);
	
	bool passesSelection(true);
	bool passesSelectionExceptJetRequirements(true);
	bool passesSelectionExceptBtagging(true);

	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		TTbarEPlusJetsReferenceSelection::Step stepName = TTbarEPlusJetsReferenceSelection::Step(step);
		if (debug_)
			cout << "Doing selection step: " << TTbarEPlusJetsReferenceSelection::StringSteps[step] << endl;

		bool passesStep(passesSelectionStep(iEvent, step));

		// Require exactly zero b jets for QCD control region
		// Or exactly one b jet, as e.g. angle(b,l) only makes sense if there is at least one b jet
		if ( nonIsolatedElectronSelection_ || invertedConversionSelection_ ) {
			if ( stepName == TTbarEPlusJetsReferenceSelection::AtLeastOneBtag || stepName == TTbarEPlusJetsReferenceSelection::AtLeastTwoBtags ) {
				passesStep = hasExactlyZeroGoodBJet() || hasExactlyOneGoodBJet() ;
			}
		}

		passesSelection = passesSelection && passesStep;
		passes_.at(step) = passesStep;

		if ( step < TTbarEPlusJetsReferenceSelection::AtLeastOneGoodJet )
			passesSelectionExceptJetRequirements = passesSelectionExceptJetRequirements && passesStep;

		if ( step < TTbarEPlusJetsReferenceSelection::AtLeastOneBtag )
			passesSelectionExceptBtagging = passesSelectionExceptBtagging && passesStep;

		// if doesn't pass selection and not in tagging mode, stop here to save CPU time
		if ( !(taggingMode_ || passesSelection) )
			break;
	}
	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		std::auto_ptr<bool> passesStep(new bool(passes_.at(step)));
		iEvent.put(passesStep, prefix_ + TTbarEPlusJetsReferenceSelection::StringSteps[step]);
	}
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelection)), prefix_ + "FullSelection");
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelectionExceptBtagging)), prefix_ + "FullSelectionNoB");

	// Store number of cleaned jets in events
	unsigned int numberOfJets(cleanedJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfJets)), prefix_ + "NumberOfJets");

	// Store indices of cleaned jets in event
	iEvent.put(std::auto_ptr<std::vector<unsigned int> >(new std::vector<unsigned int>(cleanedJetIndex_)), prefix_ + "cleanedJetIndex");
	
	unsigned int numberOfBtags(cleanedBJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfBtags)), prefix_ + "NumberOfBtags");
	iEvent.put(std::auto_ptr<std::vector<unsigned int> >(new std::vector<unsigned int>(cleanedBJetIndex_)), prefix_ + "cleanedBJetIndex");
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(signalElectronIndex_)),prefix_ + "signalElectronIndex");

	if ( bSelectionInTaggingMode_ )
		return taggingMode_ || passesSelectionExceptBtagging;
	else if ( jetSelectionInTaggingMode_ )
		return taggingMode_ || passesSelectionExceptJetRequirements;
	else
		return taggingMode_ || passesSelection;
}

void TopPairElectronPlusJetsSelectionFilter::setupEventContent(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	if (debug_)
		cout << "Setting up the event content" << endl;

	// Event info
	runNumber_ = iEvent.run();
	isRealData_ = iEvent.isRealData();

	// Vertices (for re calculating electron ID)
	if ( nonIsolatedElectronSelection_ || invertedConversionSelection_ ) {
		edm::Handle < reco::VertexCollection > verticesHandle;
	   	iEvent.getByToken(vertexInputTag_, verticesHandle);
	   	vertices_ = *verticesHandle;
	}
	
	// Trigger info
	edm::Handle < edm::TriggerResults > triggerResults;
	iEvent.getByToken(hltInputTag_, triggerResults);
	triggerResults_ = *triggerResults;

	// Jets
	edm::Handle < pat::JetCollection > jets;
	iEvent.getByToken(jetInput_, jets);
	jets_ = *jets;

	if ( applyJEC_ ) {
		corrector_ = JetCorrector::getJetCorrector (jetCorrectionService_, iSetup);
		jets_ = applyNewJec( jets_, corrector_, iEvent, iSetup );
	}

	// Electrons
	iEvent.getByToken(electronInput_, electrons_);

	// Electron VID Decisions
	Handle<edm::ValueMap<bool> > medium_id_decisions;
	iEvent.getByToken(signalElectronIDMapToken_,medium_id_decisions);
	signalElectronIDDecisions_ = *medium_id_decisions;

	Handle<edm::ValueMap<bool> > loose_id_decisions;
	iEvent.getByToken(looseElectronIDMapToken_,loose_id_decisions);
	looseElectronIDDecisions_ = *loose_id_decisions;

  	edm::Handle<edm::ValueMap<vid::CutFlowResult> > medium_id_cutflow_data;
  	iEvent.getByToken(eleMediumIdFullInfoMapToken_, medium_id_cutflow_data);
	medium_id_cutflow_data_ = *medium_id_cutflow_data;

	// Muons (for veto)
	edm::Handle < pat::MuonCollection > muons;
	iEvent.getByToken(muonInput_, muons);
	muons_ = *muons;

	// Choose electrons that pass loose selection
	if (debug_)
		cout << "Getting loose electrons" << endl;
	getLooseElectrons();

	// Choose muons that pass loose selection
	if (debug_)
		cout << "Getting loose muons" << endl;
	getLooseMuons();

	// Choose electrons that pass full selection
	if (debug_)
		cout << "Getting isolated electrons" << endl;
	goodIsolatedElectrons();

	// Get the highest pt, signal electron
	if (debug_)
		cout << "Getting signal electron" << endl;
	hasSignalElectron_ = goodIsolatedElectrons_.size() > 0;
	if (hasSignalElectron_)
		signalElectron_ = goodIsolatedElectrons_.front();

	// Clean jets against signal electron
	if (debug_)
		cout << "Getting clean jets" << endl;
	cleanedJets();

	// Get b jets from cleaned jets
	if (debug_)
		cout << "Getting clean B jets" << endl;
	cleanedBJets();
}

void TopPairElectronPlusJetsSelectionFilter::getLooseElectrons() {
	looseElectrons_.clear();

	// Loop through electrons and store those that pass a loose selection
	for (size_t index = 0; index < electrons_->size(); ++index){
		const auto electron = electrons_->ptrAt(index);		
		if (isLooseElectron(electron))
			looseElectrons_.push_back(*electron);
	}
}

bool TopPairElectronPlusJetsSelectionFilter::isLooseElectron(const edm::Ptr<pat::Electron>& electron) const {
	bool passesPtAndEta = electron->pt() > minLooseElectronPt_ && fabs(electron->eta()) < maxLooseElectronEta_;
	bool passesID = looseElectronIDDecisions_[electron];
	bool passesIso = true; // FIXME Iso already applied in ID (check in AT)
	return passesPtAndEta && passesID && passesIso;
}

void TopPairElectronPlusJetsSelectionFilter::getLooseMuons() {
	looseMuons_.clear();

	// Loop through muons and store those that pass a loose selection
	for (unsigned index = 0; index < muons_.size(); ++index) {
		const pat::Muon muon = muons_.at(index);
		if (isLooseMuon(muon))
			looseMuons_.push_back(muon);
	}
}

bool TopPairElectronPlusJetsSelectionFilter::isLooseMuon(const pat::Muon& muon) const {
	bool passesPtAndEta = muon.pt() > minLooseMuonPt_ && fabs(muon.eta()) < maxLooseMuonEta_;
	bool passesID = muon.isLooseMuon();
	bool passesIso = getRelativeIsolation(muon, 0.4, true) < looseMuonIso_;
	// bool passesIso = muon.trackIso() / muon.pt() < 0.1;;

	return passesPtAndEta && passesID && passesIso;
}

void TopPairElectronPlusJetsSelectionFilter::goodIsolatedElectrons() {
	goodIsolatedElectrons_.clear();

	// Loop over electrons and select those that satisfy full selection
	// for (unsigned index = 0; index < electrons_.size(); ++index) {
	for (size_t index = 0; index < electrons_->size(); ++index){

		// const pat::Electron electron = electrons_.at(index);
		const auto electron = electrons_->ptrAt(index);

		if (isGoodElectron(electron)) {
			goodIsolatedElectrons_.push_back(*electron);
			//Check if this is the first, and therefore the signal, electron
			if ( goodIsolatedElectrons_.size()==1 ) signalElectronIndex_ = index;
		}
	}
}

bool TopPairElectronPlusJetsSelectionFilter::isGoodElectron(const edm::Ptr<pat::Electron>& electron) const {
	bool passesPtAndEta = electron->pt() > minSignalElectronPt_ && fabs(electron->eta()) < maxSignalElectronEta_;
	bool notInCrack = fabs(electron->superCluster()->eta()) < 1.4442 || fabs(electron->superCluster()->eta()) > 1.5660;
	bool inECAL = fabs(electron->superCluster()->eta()) < 2.5;
	bool passesID = false;

	// ID Cuts
	// Index : Name
	//----------------------------------------- 
	//   0   : MinPtCut
	//   1   : GsfEleSCEtaMultiRangeCut
	//   2   : GsfEleDEtaInCut
	//   3   : GsfEleDPhiInCut
	//   4   : GsfEleFull5x5SigmaIEtaIEtaCut
	//   5   : GsfEleHadronicOverEMCut
	//   6   : GsfEleDxyCut
	//   7   : GsfEleDzCut 
	//   8   : GsfEleEInverseMinusPInverseCut
	//   9   : GsfEleEffAreaPFIsoCut
	//   10  : GsfEleConversionVetoCut
	//   11  : GsfEleMissingHitsCut

	if ( nonIsolatedElectronSelection_ ) {
		if ( returnInvertedSelection(electron, 9) ) {
			passesID = true;
		}
	}
	else if ( invertedConversionSelection_ ) {
		if ( returnInvertedSelection(electron, 10) ){
			passesID = true;
		}
	}
	else {
		passesID = signalElectronIDDecisions_[electron];
	}

	return passesPtAndEta && notInCrack && inECAL && passesID;
}

double TopPairElectronPlusJetsSelectionFilter::electronIsolation(const pat::Electron& electron) const {
	reco::GsfElectron::PflowIsolationVariables pfIso = electron.pfIsolationVariables();
	// Compute isolation with delta beta correction for PU
	float absiso = pfIso.sumChargedHadronPt 
	  + std::max(0.0 , pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - 0.5 * pfIso.sumPUPt );
	return absiso/electron.pt();
}

bool TopPairElectronPlusJetsSelectionFilter::returnInvertedSelection(const edm::Ptr<pat::Electron>& electron, uint invertedSelection) const {

	vid::CutFlowResult fullCutFlowData = medium_id_cutflow_data_[electron];
	bool passesFullSelection = true;
	// printf("\nDEBUG CutFlow, full info for cand with pt=%f:\n", electron->pt());
	// printf("    CutFlow name= %s    decision is %d\n", fullCutFlowData.cutFlowName().c_str(), (int) fullCutFlowData.cutFlowPassed());
	// printf(" Index                               cut name              isMasked    value-cut-upon     pass?\n");
	for(uint icut = 0; icut < fullCutFlowData.cutFlowSize(); icut++){
        // printf("  %2d      %50s    %d        %f          %d\n", 
		// icut, fullCutFlowData.getNameAtIndex(icut).c_str(), (int)fullCutFlowData.isCutMasked(icut), fullCutFlowData.getValueCutUpon(icut), (int)fullCutFlowData.getCutResultByIndex(icut));
    	bool passesThisCut = fullCutFlowData.getCutResultByIndex(icut);
    	if ( icut==invertedSelection ) passesThisCut = !passesThisCut;
    	if ( !passesThisCut ) {
            passesFullSelection = false;
            break;
        }		
	}
	return passesFullSelection;
}

void TopPairElectronPlusJetsSelectionFilter::cleanedJets() {
	cleanedJets_.clear();
	cleanedJetIndex_.clear();

	// Loop over jets
	unsigned int indexInNtuple = 0;
	for (unsigned index = 0; index < jets_.size(); ++index) {
		const pat::Jet jet = jets_.at(index);

		// Only jets with pt> ~20 end up in the ntuple
		// isGoodJet also requires other selection, so have to check pt here first
		// to get index of cleaned jets in jets that end up in ntuple
		if ( jet.pt() <= minJetPtInNtuples_ ) {
			continue;
		}

		// Check jet passes selection criteria
		if (!isGoodJet(jet)){
			indexInNtuple++;
			continue;
		}

		// Check if jet overlaps with the signal muon
		bool overlaps(false);
		if (tagAndProbeStudies_) {
			// Clean against all leptons for tag and probe studies
			if (goodIsolatedElectrons_.size() >= 1)
				for (unsigned index = 0; index < goodIsolatedElectrons_.size(); ++index) {
					double dR = deltaR(goodIsolatedElectrons_.at(index), jet);
					if (dR < cleaningDeltaR_) overlaps = true;
				}
		}
		else {
			if (hasSignalElectron_ && goodIsolatedElectrons_.size() == 1) {
				double dR = deltaR(signalElectron_, jet);
				overlaps = dR < cleaningDeltaR_;
			}
		}

		// Keep jet if it doesn't overlap with the signal electron
		if (!overlaps){
			cleanedJets_.push_back(jet);
			cleanedJetIndex_.push_back(indexInNtuple);
		}
		indexInNtuple++;
	}
}

void TopPairElectronPlusJetsSelectionFilter::cleanedBJets() {
	cleanedBJets_.clear();
	cleanedBJetIndex_.clear();

	// Loop over cleaned jets
	for (unsigned index = 0; index < cleanedJets_.size(); ++index) {
		const pat::Jet jet = cleanedJets_.at(index);

		// Check b jet passes pt requirement (probably same as min jet pt unless assymmetric)
		if ( jet.pt()<= minBJetPt_ ) continue;

		// Does jet pass b tag selection
		if (jet.bDiscriminator(bJetDiscriminator_) > minBJetDiscriminator_) {
			// Keep if it does
			cleanedBJets_.push_back(jet);
			cleanedBJetIndex_.push_back(index);
		}
	}
}

bool TopPairElectronPlusJetsSelectionFilter::isGoodJet(const pat::Jet& jet) const {
	//both cuts are done at PAT config level (selectedPATJets) this is just for safety
	// double smearFactor = getSmearedJetPtScale(jet, 0);
	// bool passesPtAndEta(smearFactor*jet.pt() > 20. && fabs(jet.eta()) < 2.5);

	bool passesPtAndEta(jet.pt() > minJetPtInNtuples_ && fabs(jet.eta()) < 2.4);
	bool passesJetID(false);
	bool passNOD = jet.numberOfDaughters() > 1;
	bool passNHF = jet.neutralHadronEnergyFraction() + jet.HFHadronEnergyFraction() < 0.99;
	bool passNEF = jet.neutralEmEnergyFraction() < 0.99;
	bool passCHF = true;
	bool passNCH = true;
	bool passCEF = true;
	if (fabs(jet.eta()) < 2.4) {
		passCEF = jet.chargedEmEnergyFraction() < 0.99;
		passCHF = jet.chargedHadronEnergyFraction() > 0;
		passNCH = jet.chargedMultiplicity() > 0;
	}
	passesJetID = passNOD && passCEF && passNHF && passNEF && passCHF && passNCH;

	return passesPtAndEta && passesJetID;
}

bool TopPairElectronPlusJetsSelectionFilter::passesSelectionStep(edm::Event& iEvent,
		unsigned int selectionStep) const {
	TTbarEPlusJetsReferenceSelection::Step step = TTbarEPlusJetsReferenceSelection::Step(selectionStep);
	switch (step) {
	case TTbarEPlusJetsReferenceSelection::AllEvents:
		return true;
	case TTbarEPlusJetsReferenceSelection::EventCleaningAndTrigger:
		return passesEventCleaning(iEvent) && passesTriggerSelection();
	case TTbarEPlusJetsReferenceSelection::ExactlyOneSignalElectron:
		return hasExactlyOneSignalElectron();
	case TTbarEPlusJetsReferenceSelection::LooseMuonVeto:
		return passesLooseMuonVeto();
	case TTbarEPlusJetsReferenceSelection::LooseElectronVeto:
		return passesLooseElectronVeto();
	case TTbarEPlusJetsReferenceSelection::ConversionVeto:
		return passesConversionVeto();
	case TTbarEPlusJetsReferenceSelection::AtLeastOneGoodJet:
		return hasAtLeastOneGoodJet();
	case TTbarEPlusJetsReferenceSelection::AtLeastTwoGoodJets:
		return hasAtLeastTwoGoodJets();
	case TTbarEPlusJetsReferenceSelection::AtLeastThreeGoodJets:
		return hasAtLeastThreeGoodJets();
	case TTbarEPlusJetsReferenceSelection::AtLeastFourGoodJets:
		return hasAtLeastFourGoodJets();
	case TTbarEPlusJetsReferenceSelection::AtLeastOneBtag:
		return hasAtLeastOneGoodBJet();
	case TTbarEPlusJetsReferenceSelection::AtLeastTwoBtags:
		return hasAtLeastTwoGoodBJets();
	default:
		break;
	}

	return false;
}

bool TopPairElectronPlusJetsSelectionFilter::passesEventCleaning(edm::Event& iEvent) const {
	return true;
}

bool TopPairElectronPlusJetsSelectionFilter::passesTriggerSelection() const {
	// if (dropTriggerSelection_)
	// 	return true;
	// else if (isRealData_) {
	// 	//2011 data: run 160404 to run 180252
	// 	if (runNumber_ >= 160404 && runNumber_ <= 163869)
	// 		return triggerFired("HLT_Ele25_CaloIdVT_TrkIdT_CentralTriJet30", hltConfig_, triggerResults_);
	// 	else if (runNumber_ > 163869 && runNumber_ <= 165633)
	// 		return triggerFired("HLT_Ele25_CaloIdVT_TrkIdT_TriCentralJet30", hltConfig_, triggerResults_);
	// 	else if (runNumber_ > 165633 && runNumber_ <= 178380)
	// 		return triggerFired("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30", hltConfig_,
	// 				triggerResults_);
	// 	else if (runNumber_ > 178380 && runNumber_ <= 180252)
	// 		return triggerFired("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralPFJet30", hltConfig_,
	// 				triggerResults_);
	// 	//2012 data: run 190456 to run 208686
	// 	else if (runNumber_ >= 190456 && runNumber_ <= 208686) //2012 data
	// 		return triggerFired("HLT_Ele27_WP80_v", hltConfig_, triggerResults_);

	// } else {
	// 	if (MCSampleTag_ == "Fall11") {	//Fall11 MC
	// 		return triggerFired("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30", hltConfig_, triggerResults_);
	// 	} else if (MCSampleTag_ == "Summer12") { //Summer12 MC
	// 		return triggerFired("HLT_Ele27_WP80_v", hltConfig_, triggerResults_);
	// 	} else if (MCSampleTag_ == "Summer11Leg") { //7TeV legacy MC
	// 		return true; // to be updated once we have trigger efficiencies
	// 	} else
	// 		return false;
	// }
	// return false;
	return true;
}

bool TopPairElectronPlusJetsSelectionFilter::hasExactlyOneSignalElectron() const {
	if (tagAndProbeStudies_)
		return goodIsolatedElectrons_.size() >= 1;
	else {
		return goodIsolatedElectrons_.size() == 1;
	}
}

bool TopPairElectronPlusJetsSelectionFilter::passesLooseMuonVeto() const {
	// Require no electrons in the event
	return looseMuons_.size() == 0;
}

bool TopPairElectronPlusJetsSelectionFilter::passesLooseElectronVeto() const {
	double invariantMass = 0;
	bool isZEvent = false;

	if (tagAndProbeStudies_) {
		if ( (looseElectrons_.size() >= 1) && hasSignalElectron_ ) {
			for (unsigned int index = 0; index < electrons_->size(); ++index) {
				const pat::Electron probeElectron_ = electrons_->at(index);
				// skip the tag electron itself
				if (probeElectron_.p4() == signalElectron_.p4())
					continue;
				invariantMass = (signalElectron_.p4()+probeElectron_.p4()).mass();
				bool passesLowerLimit = invariantMass > 60;
				bool passesUpperLimit = invariantMass < 120;
				if (passesLowerLimit && passesUpperLimit)
					isZEvent = true;
			}
		}
		return isZEvent == true;
	}
	else
		// Require only one loose electron, which is the signal electron
		return looseElectrons_.size() < 2;
}

bool TopPairElectronPlusJetsSelectionFilter::passesConversionVeto() const {
	if (!hasExactlyOneSignalElectron())
		return false;

	bool passVeto = signalElectron_.passConversionVeto();

   if ( invertedConversionSelection_ )
           return !passVeto;
   else
           return passVeto;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastOneGoodJet() const {
	if (cleanedJets_.size() > 0)
		return cleanedJets_.at(0).pt() > min1JetPt_;
		// return getSmearedJetPtScale(cleanedJets_.at(0), 0)*cleanedJets_.at(0).pt() > min1JetPt_;

	return false;

}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastTwoGoodJets() const {
	if (cleanedJets_.size() > 1)
		return cleanedJets_.at(1).pt() > min2JetPt_;
		// return getSmearedJetPtScale(cleanedJets_.at(1), 0)*cleanedJets_.at(1).pt() > min2JetPt_;

	return false;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastThreeGoodJets() const {
	if (cleanedJets_.size() > 2)
		return cleanedJets_.at(2).pt() > min3JetPt_;
		// return getSmearedJetPtScale(cleanedJets_.at(2), 0)*cleanedJets_.at(2).pt() > min3JetPt_;

	return false;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastFourGoodJets() const {
	if (cleanedJets_.size() > 3)
		return cleanedJets_.at(3).pt() > min4JetPt_;
		// return getSmearedJetPtScale(cleanedJets_.at(3), 0)*cleanedJets_.at(3).pt() > min4JetPt_;

	return false;
}

bool TopPairElectronPlusJetsSelectionFilter::hasExactlyZeroGoodBJet() const {
       return cleanedBJets_.size() == 0;
}

bool TopPairElectronPlusJetsSelectionFilter::hasExactlyOneGoodBJet() const {
       return cleanedBJets_.size() == 1;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastOneGoodBJet() const {
	return cleanedBJets_.size() > 0;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastTwoGoodBJets() const {
	return cleanedBJets_.size() > 1;
}







// ------------ method called once each job just before starting event loop  ------------
void TopPairElectronPlusJetsSelectionFilter::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void TopPairElectronPlusJetsSelectionFilter::endJob() {
}

void TopPairElectronPlusJetsSelectionFilter::beginRun() {
}

//define this as a plug-in
DEFINE_FWK_MODULE (TopPairElectronPlusJetsSelectionFilter);

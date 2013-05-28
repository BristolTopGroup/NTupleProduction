#include "BristolAnalysis/NTupleTools/plugins/EtaAnalyser.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETFwd.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include <iostream>
using namespace edm;
using namespace std;

//since TH*F constructors are stupid and don't take std::string (or don't know how to convert it via c_str())
// one has to use this thing.
#include "TString.h"

EtaAnalyser::EtaAnalyser(const edm::ParameterSet& iConfig) :		
		pu_weight_input_(iConfig.getParameter < edm::InputTag > ("pu_weight_input")), //
		b_tag_weight_input(iConfig.getParameter < edm::InputTag > ("b_tag_weight_input")), //
		gen_part_input_(iConfig.getParameter < edm::InputTag > ("gen_part_input")), //
		reco_MET_input_(iConfig.getParameter < edm::InputTag > ("reco_MET_Input")), //	
		reco_jet_input_(iConfig.getParameter < edm::InputTag > ("reco_jet_input")), //
		electron_input_(iConfig.getParameter < edm::InputTag > ("electron_input")), //
		muon_input_(iConfig.getParameter < edm::InputTag > ("muon_input")), //
		vertex_input_(iConfig.getParameter < edm::InputTag > ("vertex_input")), //
		gen_event_input_(iConfig.getParameter < edm::InputTag > ("gen_event_input")), //
		selection_flag_input_(iConfig.getParameter < edm::InputTag > ("selection_flag_input")), //
		is_fully_hadronic_ttbar_flag_(iConfig.getParameter < edm::InputTag > ("is_fully_hadronic_flag")), //
		is_dileptonic_ttbar_flag_(iConfig.getParameter < edm::InputTag > ("is_dileptonic_flag")), //
		is_semileptonic_tau_flag_(iConfig.getParameter < edm::InputTag > ("is_semileptonic_tau_flag")), //
		is_semileptonic_electron_flag_(iConfig.getParameter < edm::InputTag > ("is_semileptonic_electron_flag")), //
		is_semileptonic_muon_flag_(iConfig.getParameter < edm::InputTag > ("is_semileptonic_muon_flag")), //
		do_electron_channel_(iConfig.getUntrackedParameter<bool>("do_electron_channel")), //
		variable_under_analysis_(iConfig.getParameter < string > ("variable_under_analysis")), //
		variable_min_(iConfig.getParameter<double>("variable_min")), //
		variable_max_(iConfig.getParameter<double>("variable_max")), //
		variable_n_bins_(iConfig.getParameter<unsigned int>("variable_n_bins")), 
		bin_edges_(iConfig.getParameter < vector<double> > ("bin_edges")), //
		bin_edge_names_(iConfig.getParameter < vector<std::string> > ("bin_edge_names")), //
		is_semileptonic_(false), //
		truth_(), //
		measured_() {

}

void EtaAnalyser::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("pu_weight_input");
	desc.add < InputTag > ("b_tag_weight_input");
	desc.add < InputTag > ("gen_part_input");
	desc.add < InputTag > ("reco_MET_Input");
	desc.add < InputTag > ("reco_jet_input");
	desc.add < InputTag > ("electron_input");
	desc.add < InputTag > ("muon_input");
	desc.add < InputTag > ("vertex_input");
	desc.add < InputTag > ("gen_event_input");
	desc.add < InputTag > ("selection_flag_input");
	desc.add < InputTag > ("is_fully_hadronic_flag");
	desc.add < InputTag > ("is_dileptonic_flag");
	desc.add < InputTag > ("is_semileptonic_tau_flag");
	desc.add < InputTag > ("is_semileptonic_electron_flag");
	desc.add < InputTag > ("is_semileptonic_muon_flag");
	desc.add < string > ("variable_under_analysis");
	desc.add<double>("variable_min");
	desc.add<double>("variable_max");
	desc.add<unsigned int>("variable_n_bins");
	desc.add < vector<double> > ("bin_edges");
	desc.add < vector<string> > ("bin_edge_names");
	desc.addUntracked<bool>("do_electron_channel", false);

	descriptions.add("EtaAnalyser", desc);
}

void EtaAnalyser::beginJob() {
	edm::Service < TFileService > fs;
	if (!fs) {
		throw edm::Exception(edm::errors::Configuration, "TFile Service is not registered in cfg file");
	}
	
	int n_asym_bins = bin_edges_.size() - 1;

	for(int i = 0; i < n_asym_bins; i++){	

	std::string true_title = 	"truth"+bin_edge_names_[i];
	std::string meas_title = 	"measured"+bin_edge_names_[i];		

	TH1F * eta_true	=
			fs->make < TH1F	> (true_title.c_str(), TString("GEN(eta);# Events"), 300, 0, 3);

	TH1F * eta_meas =
			fs->make < TH1F	> (meas_title.c_str(), TString("RECO(eta);# Events"), 300, 0, 3);

	truth_.push_back(eta_true);
	measured_.push_back(eta_meas);	

	truth_.at(i)->Sumw2();
	measured_.at(i)->Sumw2();

	}

}

void EtaAnalyser::endJob() {

}

void EtaAnalyser::analyze(const edm::Event& iEvent, const edm::EventSetup&) {
	if (iEvent.isRealData()) { //this analysis should only be done on MC
		return;
	}

	edm::Handle<double> puWeightHandle;
	iEvent.getByLabel(pu_weight_input_, puWeightHandle);

	edm::Handle<double> btagWeightHandle;
	iEvent.getByLabel(b_tag_weight_input, btagWeightHandle);

	double puWeight(*puWeightHandle);

	bool is_semileptonic_tau(passesFilter(iEvent, is_semileptonic_tau_flag_));
	bool is_semileptonic_electron(passesFilter(iEvent, is_semileptonic_electron_flag_));
	bool is_semileptonic_muon(passesFilter(iEvent, is_semileptonic_muon_flag_));
	is_semileptonic_ = is_semileptonic_tau || is_semileptonic_electron || is_semileptonic_muon;
	
	float reco_variable(get_reco_variable(iEvent));
	float reco_eta(get_reco_eta(iEvent));
	float gen_eta(get_gen_eta(iEvent));

	int n_asym_bins = bin_edges_.size() - 1;
	
	if (do_electron_channel_) {
	
		if (is_semileptonic_electron) {

			for(int i = 0; i < n_asym_bins; i++){
			
			  //find correct bin to fill
			  if(reco_variable >= bin_edges_.at(i) && reco_variable < bin_edges_.at(i+1)){
			  //PU weight only (no btag-weight) as no b-tagging is applied
			  truth_.at(i)->Fill(gen_eta, puWeight);
			  measured_.at(i)->Fill(reco_eta, puWeight);
			  }
			}

		}

	} else { //muon channel
	
		if (is_semileptonic_muon) {

			for(int i = 0; i < n_asym_bins; i++){
			
			 	//find correct bin to fill
			 	if(reco_variable >= bin_edges_.at(i) && reco_variable < bin_edges_.at(i+1)){
				//PU weight only (no btag-weight) as no b-tagging is applied
				truth_.at(i)->Fill(gen_eta, puWeight);
				measured_.at(i)->Fill(reco_eta, puWeight);
				}
			}
		}

	}
}


float EtaAnalyser::get_reco_variable(const edm::Event& iEvent) const {
	if (variable_under_analysis_ == "MET")
		return get_reco_met(iEvent);
	else if (variable_under_analysis_ == "HT")
		return get_reco_ht(iEvent);
	else if (variable_under_analysis_ == "ST")
		return get_reco_st(iEvent);
	else if (variable_under_analysis_ == "MT")
		return get_reco_mt(iEvent);
	else if (variable_under_analysis_ == "WPT")
		return get_reco_wpt(iEvent);
	else {
		throw "Unknown variable type '" + variable_under_analysis_ + "'!";
	}
	return 0.;
}

float EtaAnalyser::get_reco_met(const edm::Event& iEvent) const {
	edm::Handle < std::vector<pat::MET> > recoMETs;
	iEvent.getByLabel(reco_MET_input_, recoMETs);

	pat::MET recoMETObject(recoMETs->at(0));
	return recoMETObject.pt();
}

float EtaAnalyser::get_reco_ht(const edm::Event& iEvent) const {
	edm::Handle < pat::JetCollection > jets;
	iEvent.getByLabel(reco_jet_input_, jets);
	float ht(0.);

	//Take ALL the jets!
	for (unsigned int index = 0; index < jets->size(); ++index) {
		const pat::Jet jet = jets->at(index);
		ht += jets->at(index).pt();
	}
	return ht;
}

float EtaAnalyser::get_reco_st(const edm::Event& iEvent) const {
	// ST = HT + MET + lepton pt
	float ht = get_reco_ht(iEvent);
	float met = get_reco_met(iEvent);
	//get lepton
	const reco::Candidate* lepton = get_reco_lepton(iEvent);
	return ht + met + lepton->pt();
}

float EtaAnalyser::get_reco_mt(const edm::Event& iEvent) const {
	//get electron/muon
	const reco::Candidate* lepton = get_reco_lepton(iEvent);
	//get MET
	edm::Handle < std::vector<pat::MET> > recoMETs;
	iEvent.getByLabel(reco_MET_input_, recoMETs);

	pat::MET met(recoMETs->at(0));

	//combine their x & y momenta to get the transverse W boson mass
	double energy_squared = pow(lepton->et() + met.et(), 2);
	double momentum_squared = pow(lepton->px() + met.px(), 2) + pow(lepton->py() + met.py(), 2);
	double MT_squared = energy_squared - momentum_squared;

	if (MT_squared > 0)
		return sqrt(MT_squared);
	else
		return -1;
}

float EtaAnalyser::get_reco_wpt(const edm::Event& iEvent) const {
	//get electron/muon
	const reco::Candidate* lepton = get_reco_lepton(iEvent);
	//get MET
	edm::Handle < std::vector<pat::MET> > recoMETs;
	iEvent.getByLabel(reco_MET_input_, recoMETs);

	pat::MET met(recoMETs->at(0));

	return sqrt(pow(lepton->px()+met.px(),2)+pow(lepton->py()+met.py(),2)); 
}

float EtaAnalyser::get_reco_eta(const edm::Event& iEvent) const {
	//get electron/muon
	const reco::Candidate* lepton = get_reco_lepton(iEvent);

	return fabs(lepton->eta()); 
}

float EtaAnalyser::get_gen_eta(const edm::Event& iEvent) const {


	if (!is_semileptonic_)
		return -1.;
	//get electron/muon
	const reco::GenParticle* lepton = get_gen_lepton(iEvent);

	return fabs(lepton->eta());

}

const reco::GenParticle* EtaAnalyser::get_gen_lepton(const edm::Event& iEvent) const {
	edm::Handle < TtGenEvent > genEvt;
	iEvent.getByLabel(gen_event_input_, genEvt);

	return genEvt->singleLepton()->clone();
}

const reco::Candidate* EtaAnalyser::get_reco_lepton(const edm::Event& iEvent) const {
	if (do_electron_channel_) {
		edm::Handle < pat::ElectronCollection > signalElectron;
		iEvent.getByLabel(electron_input_, signalElectron);
		return signalElectron->at(0).clone();
	} else {
		edm::Handle < pat::MuonCollection > signalMuon;
		iEvent.getByLabel(muon_input_, signalMuon);
		return signalMuon->at(0).clone();
	}
	return 0;
}

DEFINE_FWK_MODULE (EtaAnalyser);

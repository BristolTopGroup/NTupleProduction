#include "BristolAnalysis/NTupleTools/plugins/UnfoldingAnalyser.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETFwd.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"

#include <iostream>
using namespace edm;
using namespace std;

//since TH*F constructors are stupid and don't take std::string (or don't know how to convert it via c_str())
// one has to use this thing.
#include "TString.h"

UnfoldingAnalyser::UnfoldingAnalyser(const edm::ParameterSet& iConfig) :
		pu_weight_input_(iConfig.getParameter < edm::InputTag > ("PUWeightInput")), //
		b_tag_weight_input(iConfig.getParameter < edm::InputTag > ("BtagWeightInput")), //
		gen_MET_input_(iConfig.getParameter < edm::InputTag > ("genMetInput")), //
		reco_MET_input_(iConfig.getParameter < edm::InputTag > ("recoMetInput")), //
		gen_jet_input_(iConfig.getParameter < edm::InputTag > ("gen_jet_input")), //
		jet_input_(iConfig.getParameter < edm::InputTag > ("jet_input")), //
		electron_input_(iConfig.getParameter < edm::InputTag > ("electron_input")), //
		muon_input_(iConfig.getParameter < edm::InputTag > ("muon_input")), //
		vertex_input_(iConfig.getParameter < edm::InputTag > ("vertex_input")), //
		gen_event_input_(iConfig.getParameter < edm::InputTag > ("gen_event_input")), //
		selection_flag_input_(iConfig.getParameter < edm::InputTag > ("selectionFlagInput")), //
		is_fully_hadronic_ttbar_flag_(iConfig.getParameter < edm::InputTag > ("is_fully_hadronicFlag")), //
		is_dileptonic_ttbar_flag_(iConfig.getParameter < edm::InputTag > ("is_dileptonicFlag")), //
		is_semileptonic_tau_flag_(iConfig.getParameter < edm::InputTag > ("is_semileptonic_tauFlag")), //
		is_semileptonic_electron_flag_(iConfig.getParameter < edm::InputTag > ("is_semileptonic_electronFlag")), //
		is_semileptonic_muon_flag_(iConfig.getParameter < edm::InputTag > ("is_semileptonic_muonFlag")), //
		do_electron_channel_(iConfig.getUntrackedParameter<bool>("doElectronChannel")), //
		variable_under_analysis_(iConfig.getParameter < string > ("variable_under_analysis")), //
		variable_min_(iConfig.getParameter<double>("variable_min")), //
		variable_max_(iConfig.getParameter<double>("variable_max")), //
		variable_n_bins_(iConfig.getParameter<unsigned int>("variable_n_bins")), //
		bin_edges_(iConfig.getParameter < vector<double> > ("bin_edges")), //
		is_semileptonic_(false), //
		truth_(), //
		measured_(), //
		fake_(), //
		contamination_in_gen_variable_(), //
		contamination_in_reco_variable_(), //
		response_(), //
		response_without_fakes_(), //
		//
		truth_asym_bins_(), //
		measured_asym_bins_(), //
		fake_asym_bins_(), //
		contamination_asym_bins_in_gen_variable_(), //
		contamination_asym_bins_in_reco_variable_(), //
		response_asym_bins_(), //
		response_without_fakes_asym_bins_() {

}

void UnfoldingAnalyser::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("PUWeightInput");
	desc.add < InputTag > ("BtagWeightInput");
	desc.add < InputTag > ("genMetInput");
	desc.add < InputTag > ("recoMetInput");
	desc.add < InputTag > ("gen_jet_input");
	desc.add < InputTag > ("jet_input");
	desc.add < InputTag > ("electron_input");
	desc.add < InputTag > ("muon_input");
	desc.add < InputTag > ("vertex_input");
	desc.add < InputTag > ("gen_event_input");
	desc.add < InputTag > ("selectionFlagInput");
	desc.add < InputTag > ("is_fully_hadronicFlag");
	desc.add < InputTag > ("is_dileptonicFlag");
	desc.add < InputTag > ("is_semileptonic_tauFlag");
	desc.add < InputTag > ("is_semileptonic_electronFlag");
	desc.add < InputTag > ("is_semileptonic_muonFlag");
	desc.add < string > ("variable_under_analysis");
	desc.add<double>("variable_min");
	desc.add<double>("variable_max");
	desc.add<unsigned int>("variable_n_bins");
	desc.add < vector<double> > ("bin_edges");
	desc.addUntracked<bool>("doElectronChannel", false);

	descriptions.add("UnfoldingAnalyser", desc);
}

void UnfoldingAnalyser::beginJob() {
	edm::Service < TFileService > fs;
	if (!fs) {
		throw edm::Exception(edm::errors::Configuration, "TFile Service is not registered in cfg file");
	}
	cout << "This is not how you debug" << endl;
	truth_ =
			fs->make < TH1F
					> ("truth", TString("True distribution;GEN(" + variable_under_analysis_ + ");# Events"), variable_n_bins_, variable_min_, variable_max_);
	measured_ =
			fs->make < TH1F
					> ("measured", TString("Measured distribution;RECO(" + variable_under_analysis_ + ");# Events"), variable_n_bins_, variable_min_, variable_max_);
	fake_ =
			fs->make < TH1F
					> ("fake", TString("background distribution;RECO(" + variable_under_analysis_ + ");# Events"), variable_n_bins_, variable_min_, variable_max_);
	contamination_in_gen_variable_ =
			fs->make < TH1F
					> ("contamination_inGenMET", TString(
							"background distribution;GEN(" + variable_under_analysis_ + ");# Events"), variable_n_bins_, variable_min_, variable_max_);
	contamination_in_reco_variable_ =
			fs->make < TH1F
					> ("contamination_inRecoMET", TString(
							"background distribution;RECO(" + variable_under_analysis_ + ");# Events"), variable_n_bins_, variable_min_, variable_max_);

	response_ =
			fs->make < TH2F
					> ("response", TString(
							"response;RECO(" + variable_under_analysis_ + ");GEN(" + variable_under_analysis_ + ")"), variable_n_bins_, variable_min_, variable_max_, variable_n_bins_, variable_min_, variable_max_);
	response_without_fakes_ =
			fs->make < TH2F
					> ("response_withoutFakes", TString(
							"response;RECO(" + variable_under_analysis_ + ");GEN(" + variable_under_analysis_ + ")"), variable_n_bins_, variable_min_, variable_max_, variable_n_bins_, variable_min_, variable_max_);

//histograms with asymmetric bins (final measurement)
	cout << "But what other options do I have?" << endl;
	double* METBinEdges = &bin_edges_[0];
	unsigned int n_asym_bins = bin_edges_.size() - 1;
	truth_asym_bins_ =
			fs->make < TH1F
					> ("truth_AsymBins", TString("True distribution;GEN(" + variable_under_analysis_ + ");# Events"), n_asym_bins, METBinEdges);
	measured_asym_bins_ =
			fs->make < TH1F
					> ("measured_AsymBins", TString(
							"Measured distribution;RECO(" + variable_under_analysis_ + ");# Events"), n_asym_bins, METBinEdges);
	fake_asym_bins_ =
			fs->make < TH1F
					> ("fake_AsymBins", TString(
							"background distribution;RECO(" + variable_under_analysis_ + ");# Events"), n_asym_bins, METBinEdges);
	contamination_asym_bins_in_gen_variable_ =
			fs->make < TH1F
					> ("contamination_asym_bins_inGenMET", TString(
							"background distribution;GEN(" + variable_under_analysis_ + ");# Events"), n_asym_bins, METBinEdges);
	contamination_asym_bins_in_reco_variable_ =
			fs->make < TH1F
					> ("contamination_asym_bins_inRecoMET", TString(
							"background distribution;RECO(" + variable_under_analysis_ + ");# Events"), n_asym_bins, METBinEdges);
	response_asym_bins_ =
			fs->make < TH2F
					> ("response_AsymBins", TString(
							"response;RECO(" + variable_under_analysis_ + ");GEN(" + variable_under_analysis_ + ")"), n_asym_bins, METBinEdges, n_asym_bins, METBinEdges);
	response_without_fakes_asym_bins_ =
			fs->make < TH2F
					> ("response_without_fakes_AsymBins", TString(
							"response;RECO(" + variable_under_analysis_ + ");GEN(" + variable_under_analysis_ + ")"), n_asym_bins, METBinEdges, n_asym_bins, METBinEdges);

	cout << "Well, you could use 'scram b' as a compiler on your machine within an IDE" << endl;
	truth_->Sumw2();
	measured_->Sumw2();
	fake_->Sumw2();
	contamination_in_gen_variable_->Sumw2();
	contamination_in_reco_variable_->Sumw2();
	response_->Sumw2();
	response_without_fakes_->Sumw2();

	truth_asym_bins_->Sumw2();
	measured_asym_bins_->Sumw2();
	fake_asym_bins_->Sumw2();
	contamination_asym_bins_in_gen_variable_->Sumw2();
	contamination_asym_bins_in_reco_variable_->Sumw2();
	response_asym_bins_->Sumw2();
	response_without_fakes_asym_bins_->Sumw2();

	cout << "However, you need to be able to install CMSSW on your machine." << endl;
}

void UnfoldingAnalyser::endJob() {

}

void UnfoldingAnalyser::analyze(const edm::Event& iEvent, const edm::EventSetup&) {
	if (iEvent.isRealData()) { //this analysis should only be done on MC
		return;
	}

	edm::Handle<double> puWeightHandle;
	iEvent.getByLabel(pu_weight_input_, puWeightHandle);

	edm::Handle<double> btagWeightHandle;
	iEvent.getByLabel(b_tag_weight_input, btagWeightHandle);

	double puWeight(*puWeightHandle);
	double btagWeight(*btagWeightHandle);
	double weight(puWeight * btagWeight);

	bool passes_selection(passesFilter(iEvent, selection_flag_input_));
	bool is_fully_hadronic(passesFilter(iEvent, is_fully_hadronic_ttbar_flag_));
	bool is_dileptonic(passesFilter(iEvent, is_dileptonic_ttbar_flag_));
	bool is_semileptonic_tau(passesFilter(iEvent, is_semileptonic_tau_flag_));
	bool is_semileptonic_electron(passesFilter(iEvent, is_semileptonic_electron_flag_));
	bool is_semileptonic_muon(passesFilter(iEvent, is_semileptonic_muon_flag_));
	is_semileptonic_ = is_semileptonic_tau || is_semileptonic_electron || is_semileptonic_muon;

	float gen_variable(get_gen_variable(iEvent));
	float reco_variable(get_gen_variable(iEvent));

	if (do_electron_channel_) {
		if (is_semileptonic_electron) {
			//PU weight only (no btag-weight) as no b-tagging is applied
			truth_->Fill(gen_variable, puWeight);
			truth_asym_bins_->Fill(gen_variable, puWeight);
		}

		if (passes_selection) {
			measured_->Fill(reco_variable, weight);
			measured_asym_bins_->Fill(reco_variable, weight);
			response_->Fill(reco_variable, gen_variable, weight);
			response_asym_bins_->Fill(reco_variable, gen_variable, weight);

			if (is_semileptonic_electron) {
				response_without_fakes_->Fill(reco_variable, gen_variable, weight);
				response_without_fakes_asym_bins_->Fill(reco_variable, gen_variable, weight);
			} else {
				fake_->Fill(reco_variable, weight);
				fake_asym_bins_->Fill(reco_variable, weight);
				//contamination from other ttbar processes
				if (is_fully_hadronic || is_dileptonic || is_semileptonic_tau || is_semileptonic_muon) {
					contamination_in_reco_variable_->Fill(reco_variable, weight);
					contamination_asym_bins_in_reco_variable_->Fill(reco_variable, weight);
					contamination_in_gen_variable_->Fill(gen_variable, weight);
					contamination_asym_bins_in_gen_variable_->Fill(gen_variable, weight);
				}
			}

		}

	} else { //muon channel
		if (is_semileptonic_muon) {
			//PU weight only (no btag-weight) as no b-tagging is applied
			truth_->Fill(gen_variable, puWeight);
			truth_asym_bins_->Fill(gen_variable, puWeight);
		}

		if (passes_selection) {
			measured_->Fill(reco_variable, weight);
			measured_asym_bins_->Fill(reco_variable, weight);
			response_->Fill(reco_variable, gen_variable, weight);
			response_asym_bins_->Fill(reco_variable, gen_variable, weight);

			if (is_semileptonic_muon) {
				response_without_fakes_->Fill(reco_variable, gen_variable, weight);
				response_without_fakes_asym_bins_->Fill(reco_variable, gen_variable, weight);
			} else {
				fake_->Fill(reco_variable, weight);
				fake_asym_bins_->Fill(reco_variable, weight);
				if (is_fully_hadronic || is_dileptonic || is_semileptonic_tau || is_semileptonic_electron) {
					contamination_in_reco_variable_->Fill(reco_variable, weight);
					contamination_asym_bins_in_reco_variable_->Fill(reco_variable, weight);
					contamination_in_gen_variable_->Fill(gen_variable, weight);
					contamination_asym_bins_in_gen_variable_->Fill(gen_variable, weight);
				}
			}
		}
	}
}

float UnfoldingAnalyser::get_gen_variable(const edm::Event& iEvent) const {
	if (variable_under_analysis_ == "MET")
		return get_gen_met(iEvent);
	else if (variable_under_analysis_ == "HT")
		return get_gen_ht(iEvent);
	else if (variable_under_analysis_ == "ST")
		return get_gen_st(iEvent);
	else if (variable_under_analysis_ == "MT")
		return get_gen_mt(iEvent);
	else {
		throw "Unknown variable type '" + variable_under_analysis_ + "'!";
	}
	return 0.;
}

float UnfoldingAnalyser::get_gen_met(const edm::Event& iEvent) const {
	edm::Handle < reco::GenMETCollection > genMETs;
	iEvent.getByLabel(gen_MET_input_, genMETs);
	reco::GenMET genMETObject(genMETs->at(0));
	return genMETObject.pt();
}

float UnfoldingAnalyser::get_gen_ht(const edm::Event& iEvent) const {
	edm::Handle < reco::GenJetCollection > jets;
	iEvent.getByLabel(gen_jet_input_, jets);
	float ht(0.);

	//HT = first 5 jets == 5 most energetic jets
	for (unsigned int index = 0; index < jets->size() && index < 6; ++index) {
		ht += jets->at(index).pt();
	}
	return ht;
}

float UnfoldingAnalyser::get_gen_st(const edm::Event& iEvent) const {
	if (!is_semileptonic_)
		return -1.;
	// ST = HT + MET + lepton pt
	float ht = get_gen_ht(iEvent);
	float met = get_gen_met(iEvent);
	//get lepton
	const reco::GenParticle* lepton = get_gen_lepton(iEvent);
	return ht + met + lepton->pt();
}

float UnfoldingAnalyser::get_gen_mt(const edm::Event& iEvent) const {
	if (!is_semileptonic_)
		return -1.;
	//get electron/muon
	const reco::GenParticle* lepton = get_gen_lepton(iEvent);
	//get MET
	edm::Handle < reco::GenMETCollection > genMETs;
	iEvent.getByLabel(gen_MET_input_, genMETs);
	reco::GenMET met(genMETs->at(0));

	//combine their x & y momenta to get the transverse W boson mass
	double energy_squared = pow(lepton->et() + met.et(), 2);
	double momentum_squared = pow(lepton->px() + met.px(), 2) + pow(lepton->py() + met.py(), 2);
	double MT_squared = energy_squared - momentum_squared;

	if (MT_squared > 0)
		return sqrt(MT_squared);
	else
		return -1;
}

float UnfoldingAnalyser::get_reco_variable(const edm::Event& iEvent) const {
	if (variable_under_analysis_ == "MET")
		return get_reco_met(iEvent);
	else if (variable_under_analysis_ == "HT")
		return get_reco_ht(iEvent);
	else if (variable_under_analysis_ == "ST")
		return get_reco_st(iEvent);
	else if (variable_under_analysis_ == "MT")
		return get_reco_mt(iEvent);
	else {
		throw "Unknown variable type '" + variable_under_analysis_ + "'!";
	}
	return 0.;
}

float UnfoldingAnalyser::get_reco_met(const edm::Event& iEvent) const {
	edm::Handle < std::vector<pat::MET> > recoMETs;
	iEvent.getByLabel(reco_MET_input_, recoMETs);

	pat::MET recoMETObject(recoMETs->at(0));
	return recoMETObject.pt();
}

float UnfoldingAnalyser::get_reco_ht(const edm::Event& iEvent) const {
	edm::Handle < pat::JetCollection > jets;
	iEvent.getByLabel(jet_input_, jets);
	float ht(0.);

	//HT = first 5 jets == 5 most energetic jets
	for (unsigned int index = 0; index < jets->size() && index < 6; ++index) {
		const pat::Jet jet = jets->at(index);
		ht += jets->at(index).pt();
	}
	return ht;
}

float UnfoldingAnalyser::get_reco_st(const edm::Event& iEvent) const {
	// ST = HT + MET + lepton pt
	float ht = get_reco_ht(iEvent);
	float met = get_reco_met(iEvent);
	//get lepton
	const reco::Candidate* lepton = get_reco_lepton(iEvent);
	return ht + met + lepton->pt();
}

float UnfoldingAnalyser::get_reco_mt(const edm::Event& iEvent) const {
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

const reco::GenParticle* UnfoldingAnalyser::get_gen_lepton(const edm::Event& iEvent) const {
	edm::Handle < TtGenEvent > genEvt;
	iEvent.getByLabel(gen_event_input_, genEvt);

	return genEvt->singleLepton()->clone();
}

const reco::Candidate* UnfoldingAnalyser::get_reco_lepton(const edm::Event& iEvent) const {
	if (do_electron_channel_) {
		edm::Handle < pat::ElectronCollection > electrons;
		iEvent.getByLabel(electron_input_, electrons);
		for (unsigned index = 0; index < electrons->size(); ++index) {
			const pat::Electron electron = electrons->at(index);
			bool passes_pt_and_eta = electron.pt() > 30. && fabs(electron.eta()) < 2.5;
			bool not_in_crack = fabs(electron.superCluster()->eta()) < 1.4442
					|| fabs(electron.superCluster()->eta()) > 1.5660;
			//2D impact w.r.t primary vertex
			bool passes_d0 = electron.dB(pat::Electron::PV2D) < 0.02; //cm
			bool passes_id = electron.electronID("mvaTrigV0") > 0.0;
			bool is_good_electron = passes_pt_and_eta && not_in_crack && passes_d0 && passes_id;

			edm::Handle<double> rhoH;
			iEvent.getByLabel(edm::InputTag("kt6PFJets", "rho"), rhoH);
			double rho = *rhoH.product();

			bool passes_iso = getRelativeIsolation(electron, 0.3, rho, iEvent.isRealData(), false, true) < 0.1;

			if (is_good_electron && passes_iso) { //since we check for signal selection, there should be really just one electron
				return electron.clone();
			}
		}
	} else {
		edm::Handle < pat::MuonCollection > muons;
		iEvent.getByLabel(muon_input_, muons);
		edm::Handle < reco::VertexCollection > primary_vertices;
		iEvent.getByLabel(vertex_input_, primary_vertices);
		reco::Vertex primary_vertex = primary_vertices->at(0);

		for (unsigned index = 0; index < muons->size(); ++index) {
			const pat::Muon muon = muons->at(index);
			bool passes_pt_and_eta = muon.pt() > 26. && fabs(muon.eta()) < 2.1;
			//2D impact w.r.t primary vertex
			bool passes_d0 = muon.dB(pat::Muon::PV2D) < 0.02 && fabs(muon.vertex().z() - primary_vertex.z()) < 0.5; //cm
			bool passes_id = muon.isPFMuon() && muon.isGlobalMuon();
			bool track_quality = muon.globalTrack()->normalizedChi2() < 10
					&& muon.track()->hitPattern().trackerLayersWithMeasurement() > 5
					&& muon.globalTrack()->hitPattern().numberOfValidMuonHits() > 0
					&& muon.innerTrack()->hitPattern().numberOfValidPixelHits() > 0
					&& muon.numberOfMatchedStations() > 1;
			bool is_good_muon = passes_pt_and_eta && passes_d0 && passes_id && track_quality;

			bool passes_iso = getRelativeIsolation(muon, 0.4, true) < 0.12;
			if (is_good_muon && passes_iso) {
				return muon.clone();
			}
		}
	}
	return 0;
}

DEFINE_FWK_MODULE (UnfoldingAnalyser);


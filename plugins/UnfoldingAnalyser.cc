/**
 * @deprecated
 */

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
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include <iostream>
using namespace edm;
using namespace std;

//since TH*F constructors are stupid and don't take std::string (or don't know how to convert it via c_str())
// one has to use this thing.
#include "TString.h"

UnfoldingAnalyser::UnfoldingAnalyser(const edm::ParameterSet& iConfig) :		
		pu_weight_input_(iConfig.getParameter < edm::InputTag > ("pu_weight_input")), //
		b_tag_weight_input(iConfig.getParameter < edm::InputTag > ("b_tag_weight_input")), //
		gen_part_input_(iConfig.getParameter < edm::InputTag > ("gen_part_input")), //
		gen_MET_input_(iConfig.getParameter < edm::InputTag > ("gen_MET_input")), //
		reco_MET_input_(iConfig.getParameter < edm::InputTag > ("reco_MET_Input")), //	
		gen_jet_input_(iConfig.getParameter < edm::InputTag > ("gen_jet_input")), //
		reco_jet_input_(iConfig.getParameter < edm::InputTag > ("reco_jet_input")), //
		electron_input_(iConfig.getParameter < edm::InputTag > ("electron_input")), //
		muon_input_(iConfig.getParameter < edm::InputTag > ("muon_input")), //
		vertex_input_(iConfig.getParameter < edm::InputTag > ("vertex_input")), //
		gen_event_input_(iConfig.getParameter < edm::InputTag > ("gen_event_input")), //
		selection_flag_input_(consumes<bool>(iConfig.getParameter < edm::InputTag > ("selection_flag_input"))), //
		is_fully_hadronic_ttbar_flag_(consumes<bool>(iConfig.getParameter < edm::InputTag > ("is_fully_hadronic_flag"))), //
		is_dileptonic_ttbar_flag_(consumes<bool>(iConfig.getParameter < edm::InputTag > ("is_dileptonic_flag"))), //
		is_semileptonic_tau_flag_(consumes<bool>(iConfig.getParameter < edm::InputTag > ("is_semileptonic_tau_flag"))), //
		is_semileptonic_electron_flag_(consumes<bool>(iConfig.getParameter < edm::InputTag > ("is_semileptonic_electron_flag"))), //
		is_semileptonic_muon_flag_(consumes<bool>(iConfig.getParameter < edm::InputTag > ("is_semileptonic_muon_flag"))), //
		do_electron_channel_(iConfig.getUntrackedParameter<bool>("do_electron_channel")), //
		variable_under_analysis_(iConfig.getParameter < string > ("variable_under_analysis")), //
		variable_min_(iConfig.getParameter<double>("variable_min")), //
		variable_max_(iConfig.getParameter<double>("variable_max")), //
		variable_n_bins_(iConfig.getParameter<unsigned int>("variable_n_bins")), //
		bin_edges_(iConfig.getParameter < vector<double> > ("bin_edges")), //
		centre_of_mass_energy_(iConfig.getParameter<double>("centre_of_mass_energy")), //
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
	desc.add < InputTag > ("pu_weight_input");
	desc.add < InputTag > ("b_tag_weight_input");
	desc.add < InputTag > ("gen_part_input");
	desc.add < InputTag > ("gen_MET_input");
	desc.add < InputTag > ("reco_MET_Input");
	desc.add < InputTag > ("gen_jet_input");
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
	desc.addUntracked<bool>("do_electron_channel", false);
	desc.add<double>("centre_of_mass_energy");

	descriptions.add("UnfoldingAnalyser", desc);
}

void UnfoldingAnalyser::beginJob() {
	edm::Service < TFileService > fs;
	if (!fs) {
		throw edm::Exception(edm::errors::Configuration, "TFile Service is not registered in cfg file");
	}
	//cout << "This is not how you debug" << endl;
//histograms with 1 GeV binning
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
 					> ("response_without_fakes", TString(
 							"response;RECO(" + variable_under_analysis_ + ");GEN(" + variable_under_analysis_ + ")"), variable_n_bins_, variable_min_, variable_max_, variable_n_bins_, variable_min_, variable_max_);

//histograms with asymmetric bins (final measurement)
	//cout << "But what other options do I have?" << endl;
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

	//cout << "Well, you could use 'scram b' as a compiler on your machine within an IDE" << endl;
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

	//cout << "However, you need to be able to install CMSSW on your machine." << endl;
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
	
		
	float gen_variable(0);
	gen_variable = get_gen_variable(iEvent);

	if (do_electron_channel_) {
		if (is_semileptonic_electron) {
			//PU weight only (no btag-weight) as no b-tagging is applied
			truth_->Fill(gen_variable, puWeight);
			truth_asym_bins_->Fill(gen_variable, puWeight);
		}

		double electronCorrection = get_electron_correction(iEvent, centre_of_mass_energy_);

		if (passes_selection) {
			float reco_variable(get_reco_variable(iEvent));

			weight *= electronCorrection;

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

		double muonCorrection = get_muon_correction(iEvent, centre_of_mass_energy_);

		if (passes_selection) {
			float reco_variable(get_reco_variable(iEvent));

			weight *= muonCorrection;
			
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
	else if (variable_under_analysis_ == "MET_nu")
		return get_gen_met_nu(iEvent);
	else if (variable_under_analysis_ == "HT")
		return get_gen_ht(iEvent);
	else if (variable_under_analysis_ == "HT_nocuts")
		return get_gen_ht_nocuts(iEvent);
	else if (variable_under_analysis_ == "HT_parton")
		return get_gen_ht_parton(iEvent);
	else if (variable_under_analysis_ == "ST")
		return get_gen_st(iEvent);
	else if (variable_under_analysis_ == "ST_nocuts")
		return get_gen_st_nocuts(iEvent);
	else if (variable_under_analysis_ == "ST_parton")
		return get_gen_st_parton(iEvent);
	else if (variable_under_analysis_ == "MT")
		return get_gen_mt(iEvent);
	else if (variable_under_analysis_ == "MT_nu")
		return get_gen_mt_nu(iEvent);	
	else if (variable_under_analysis_ == "WPT")
		return get_gen_wpt(iEvent);
	else if (variable_under_analysis_ == "WPT_nu")
		return get_gen_wpt_nu(iEvent);
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

float UnfoldingAnalyser::get_gen_met_nu(const edm::Event& iEvent) const {
	
	if (!is_semileptonic_)
		return -1.;
	
	edm::Handle < TtGenEvent > genEvt;
        iEvent.getByLabel(gen_event_input_, genEvt);
	
	return genEvt->singleNeutrino()->et();
}

float UnfoldingAnalyser::get_gen_ht(const edm::Event& iEvent) const {
	edm::Handle < reco::GenJetCollection > jets;
	iEvent.getByLabel(gen_jet_input_, jets);

    //get lepton
    const reco::GenParticle* lepton = 0;
    if ( is_semileptonic_ )
    	lepton = get_gen_lepton(iEvent);

    float ht(0.);

    //Take ALL the jets!
    for (unsigned int index = 0; index < jets->size(); ++index) {
            if (jets->at(index).pt() > 20) {
            	if ( lepton != 0 ) {
                    double dR = deltaR(*lepton, jets->at(index));
                    if (dR > 0.3)
                            ht += jets->at(index).pt();
            	}
            	else {
            		ht += jets->at(index).pt();
            	}
            }
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

float UnfoldingAnalyser::get_gen_ht_nocuts(const edm::Event& iEvent) const {
	edm::Handle < reco::GenJetCollection > jets;
	iEvent.getByLabel(gen_jet_input_, jets);
	float ht(0.);

    //get lepton
    const reco::GenParticle* lepton = 0;
    if ( is_semileptonic_ )
    	lepton = get_gen_lepton(iEvent);

	//Take ALL the jets!
	for (unsigned int index = 0; index < jets->size(); ++index) {
		if ( lepton != 0 ) {
			double dR = deltaR(*lepton, jets->at(index));
			if (dR > 0.3)
				ht += jets->at(index).pt();
		}
		else {
			ht += jets->at(index).pt();
		}
	}
	return ht;
}

float UnfoldingAnalyser::get_gen_ht_parton(const edm::Event& iEvent) const {
	if (!is_semileptonic_)
		return -1.;

	edm::Handle < TtGenEvent > genEvt;
    iEvent.getByLabel(gen_event_input_, genEvt);
	
	//radiation from leptonic top
	double leptTopRad = 0;
	for(unsigned int i = 0; i < genEvt->leptonicDecayTopRadiation().size(); i++){
	leptTopRad += genEvt->leptonicDecayTopRadiation().at(i)->pt();	
	}
	
	//radiation from hadronic top
	double hadTopRad = 0;
	for(unsigned int i = 0; i < genEvt->hadronicDecayTopRadiation().size(); i++){
	hadTopRad += genEvt->hadronicDecayTopRadiation().at(i)->pt();	
	}
	
	double HT_parton=genEvt->hadronicDecayQuark()->pt()+genEvt->hadronicDecayQuarkBar()->pt()+genEvt->leptonicDecayB()->pt()+genEvt->hadronicDecayB()->pt()+leptTopRad+hadTopRad;

	return HT_parton;
}

float UnfoldingAnalyser::get_gen_st_nocuts(const edm::Event& iEvent) const {
	if (!is_semileptonic_)
		return -1.;
	// ST = HT + MET + lepton pt
	float ht = get_gen_ht_nocuts(iEvent);
	float met = get_gen_met(iEvent);
	
	//get lepton
	const reco::GenParticle* lepton = get_gen_lepton(iEvent);
	return ht + met + lepton->pt();
}

float UnfoldingAnalyser::get_gen_st_parton(const edm::Event& iEvent) const {
	if (!is_semileptonic_)
		return -1.;

	edm::Handle < TtGenEvent > genEvt;
    iEvent.getByLabel(gen_event_input_, genEvt);

	float ht = get_gen_ht_parton(iEvent);
	
	double ST_parton=genEvt->singleLepton()->pt()+genEvt->singleNeutrino()->pt()+ht;

	return ST_parton;
}

float UnfoldingAnalyser::get_gen_mt(const edm::Event& iEvent) const {
	if (!is_semileptonic_)
		return -1.;
	//get electron/muon
	const reco::GenParticle* lepton = get_gen_lepton(iEvent);
	//get Gen MET
	edm::Handle < reco::GenMETCollection > genMETs;
	iEvent.getByLabel(gen_MET_input_, genMETs);
	reco::GenMET met(genMETs->at(0));

	//combine their x & y momenta to get the transverse W boson mass
	double energy_squared = pow(lepton->et() + met.pt(), 2);
	double momentum_squared = pow(lepton->px() + met.px(), 2) + pow(lepton->py() + met.py(), 2);
	double MT_squared = energy_squared - momentum_squared;
	
	if (MT_squared > 0)
		return sqrt(MT_squared);
	else
		return -1;
}

float UnfoldingAnalyser::get_gen_mt_nu(const edm::Event& iEvent) const {
    if (!is_semileptonic_)
	return -1.;
    
    edm::Handle < TtGenEvent > genEvt;
    iEvent.getByLabel(gen_event_input_, genEvt);

	//need to use lepton and neutrino for this!
	
	double energy_squared = pow(genEvt->singleLepton()->et() + genEvt->singleNeutrino()->et(), 2);
	double momentum_squared = pow(genEvt->singleLepton()->px() + genEvt->singleNeutrino()->px(), 2) + pow(genEvt->singleLepton()->py() + genEvt->singleNeutrino()->py(), 2);
	double MT_squared = energy_squared - momentum_squared;
	
	if (MT_squared > 0)
		return sqrt(MT_squared);
	else
		return -1;
}


float UnfoldingAnalyser::get_gen_wpt(const edm::Event& iEvent) const {
	if (!is_semileptonic_)
		return -1.;

	//get electron/muon
	const reco::GenParticle* lepton = get_gen_lepton(iEvent);

	//get Gen MET
	edm::Handle < reco::GenMETCollection > genMETs;
	iEvent.getByLabel(gen_MET_input_, genMETs);
	reco::GenMET met(genMETs->at(0));

	return sqrt(pow(lepton->px()+met.px(),2)+pow(lepton->py()+met.py(),2));
}

float UnfoldingAnalyser::get_gen_wpt_nu(const edm::Event& iEvent) const {
	if (!is_semileptonic_)
		return -1.;
		
        edm::Handle < TtGenEvent > genEvt;
    	iEvent.getByLabel(gen_event_input_, genEvt);

	return genEvt->leptonicDecayW()->pt();
}

float UnfoldingAnalyser::get_reco_variable(const edm::Event& iEvent) const {
	if (variable_under_analysis_ == "MET" || variable_under_analysis_ == "MET_nu")
		return get_reco_met(iEvent);
	else if (variable_under_analysis_ == "HT" || variable_under_analysis_ == "HT_nocuts" || variable_under_analysis_ == "HT_parton")
		return get_reco_ht(iEvent);
	else if (variable_under_analysis_ == "ST" || variable_under_analysis_ == "ST_nocuts" || variable_under_analysis_== "ST_parton")
		return get_reco_st(iEvent);
	else if (variable_under_analysis_ == "MT" || variable_under_analysis_ == "MT_nu")
		return get_reco_mt(iEvent);
	else if (variable_under_analysis_ == "WPT" || variable_under_analysis_ == "WPT_nu")
		return get_reco_wpt(iEvent);
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
	iEvent.getByLabel(reco_jet_input_, jets);
	float ht(0.);
	
	//Take ALL the jets!
	for (unsigned int index = 0; index < jets->size(); ++index) {
		const pat::Jet jet = jets->at(index);
		ht += getSmearedJetPtScale(jets->at(index), 0)*jets->at(index).pt();
	}
	return ht;
}

float UnfoldingAnalyser::get_reco_st(const edm::Event& iEvent) const {
	// ST = HT + MET + lepton pt
	float ht = get_reco_ht(iEvent);
	float met = get_reco_met(iEvent);
	//get lepton
	const reco::Candidate* lepton = get_reco_lepton(iEvent);
	if ( lepton == 0 )
		return -1;

	return ht + met + lepton->pt();
}

float UnfoldingAnalyser::get_reco_mt(const edm::Event& iEvent) const {
	//get electron/muon
	const reco::Candidate* lepton = get_reco_lepton(iEvent);
	if ( lepton == 0 )
		return -1;

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

float UnfoldingAnalyser::get_reco_wpt(const edm::Event& iEvent) const {
	//get electron/muon
	const reco::Candidate* lepton = get_reco_lepton(iEvent);
	if ( lepton == 0 )
		return -1;

	//get MET
	edm::Handle < std::vector<pat::MET> > recoMETs;
	iEvent.getByLabel(reco_MET_input_, recoMETs);

	pat::MET met(recoMETs->at(0));
	
	return sqrt(pow(lepton->px()+met.px(),2)+pow(lepton->py()+met.py(),2)); 
}

const reco::GenParticle* UnfoldingAnalyser::get_gen_lepton(const edm::Event& iEvent) const {
	edm::Handle < TtGenEvent > genEvt;
	iEvent.getByLabel(gen_event_input_, genEvt);

	return genEvt->singleLepton();
}

const reco::Candidate* UnfoldingAnalyser::get_reco_lepton(const edm::Event& iEvent) const {
	if (do_electron_channel_) {
		edm::Handle < pat::ElectronCollection > signalElectron;
		iEvent.getByLabel(electron_input_, signalElectron);
		if ( signalElectron->size() > 0 )
			return &(signalElectron->at(0));
		else
			return 0;
	} else {
		edm::Handle < pat::MuonCollection > signalMuon;
		iEvent.getByLabel(muon_input_, signalMuon);
		if ( signalMuon->size() > 0 )
			return &(signalMuon->at(0));
		else
			return 0;
	}
	return 0;
}

float UnfoldingAnalyser::get_electron_correction(const edm::Event& iEvent, double centre_of_mass_energy_) const {
	double correction(1.);

	edm::Handle < pat::ElectronCollection > signalElectron;
	iEvent.getByLabel(electron_input_, signalElectron);

	double electronEta = fabs(signalElectron->at(0).eta());
	double electronPt = signalElectron->at(0).pt();

//	if(centre_of_mass_energy == 7){
//		// hard coded values since pickle file not available...not updated because I couldn't find any values on twikis!
//		if (electronEta < -1.5)
//			correction = 1.003;
//		else if (electronEta >= -1.5 && electronEta < -1.2)
//			correction = 0.980;
//		else if (electronEta >= -1.2 && electronEta < -0.9)
//			correction = 0.941;
//		else if (electronEta >= -0.9 && electronEta < 0)
//			correction = 0.974;
//		else if (electronEta >= 0 && electronEta < 0.9)
//			correction = 0.977;
//		else if (electronEta >= 0.9 && electronEta < 1.2)
//			correction = 0.939;
//		else if (electronEta >= 1.2 && electronEta < 1.5)
//			correction = 0.967;
//		else if (electronEta >= 1.5)
//			correction = 1.023;
//	}
	//8TeV scale factors from https://twiki.cern.ch/twiki/bin/viewauth/CMS/KoPFAElectronTagAndProbe
	//Only factors from PromptReco available (in the "Efficiency for e+jet channel (promptreco)" section)
	//Specifically: ID & Iso: "ID/Isolation efficiency" sub-section
	//Specifically: Trigger: "Trigger efficiency" sub-section
	//These values are hard coded because, unlike for Muons, there is no pickle file provided.
//	else if(centre_of_mass_energy == 8){ //corrections for (ID & Iso) and Trigger respectively
		if(fabs(electronEta)<0.8) {
			if(20<=electronPt && electronPt<30) {  //Note: Trigger scale factors only provided down to electron electronPt of 30GeV in the link above, so I have used the same as for the 30GeV-40GeV range.
				correction = 0.949*0.987;
			}
			else if(30<=electronPt && electronPt<40) {
				correction = 0.939*0.987;
			}
			else if(40<=electronPt && electronPt<50) {
				correction = 0.950*0.997;
			}
			else if(50<=electronPt && electronPt<=200) {
				correction = 0.957*0.998;
			}
		}
		else if(fabs(electronEta)>=0.8 && fabs(electronEta)<1.478) {
			if(20<=electronPt && electronPt<30) { //Note: Trigger scale factors only provided down to electron pt of 30GeV in the link above, so I have used the same as for the 30GeV-40GeV range.
				correction = 0.900*0.964;
			}
			if(30<=electronPt && electronPt<40) {
				correction = 0.920*0.964;
			}
			if(40<=electronPt && electronPt<50) {
				correction = 0.949*0.980;
			}
			if(50<=electronPt && electronPt<=200) {
				correction = 0.959*0.988;
			}
		}
		else if(fabs(electronEta)>=1.478 && fabs(electronEta)<2.5) {
			if(20<=electronPt && electronPt<30) { //Note: Trigger scale factors only provided down to electron pt of 30GeV in the link above, so I have used the same as for the 30GeV-40GeV range.
				correction = 0.857*1.004;
			}
			if(30<=electronPt && electronPt<40) {
				correction = 0.907*1.004;
			}
			if(40<=electronPt && electronPt<50) {
				correction = 0.937*1.033;
			}
			if(50<=electronPt && electronPt<=200) {
				correction = 0.954*0.976;
			}
		}
//	}
	return correction;
}

//old get_muon_correction method
//float UnfoldingAnalyser::get_muon_correction(const edm::Event& iEvent) const {
//	//ID, iso and trigger correction respectively from:  https://indico.cern.ch/getFile.py/access?contribId=3&resId=0&materialId=slides&confId=214870
//
//	double correction(1.);
//
//	edm::Handle < pat::MuonCollection > signalMuon;
//	iEvent.getByLabel(muon_input_, signalMuon);
//
//	double muEta = signalMuon->at(0).eta();
//
//	if(fabs(muEta)<0.9)
//		correction = 0.9941*0.9923*0.9560;
//	else if(fabs(muEta)>=0.9 && fabs(muEta)<1.2)
//		correction = 0.9917*0.9979*0.9528;
//	else if(fabs(muEta)>=1.2)
//		correction = 0.9982*1.0019*0.9809;
//
//	return correction;
//}

float UnfoldingAnalyser::get_muon_correction(const edm::Event& iEvent, double centre_of_mass_energy_) const {
	double correction(1.);

	edm::Handle < pat::MuonCollection > signalMuon;
	iEvent.getByLabel(muon_input_, signalMuon);

	double muEta = fabs(signalMuon->at(0).eta());
	double muonPt = signalMuon->at(0).pt();
	double id_correction(0), iso_correction(0), trigger_correction(0), correction_A(0), correction_B(0), lumi_2011A(0), lumi_2011B(0), lumi_2011(0);

	// 7TeV scale factors from https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonReferenceEffs#2011_data (from 44X pickle file)
	if (centre_of_mass_energy_ == 7) { //Luminosity weighted average of 'combRelPFISO12_2011A' and 'combRelPFISO12_2011B' from pickle file
		//get scale factors based on muon eta bin
		if (fabs(muEta) <= 1.2) { // 'pt_abseta<1.2' in pickle file
			//get scale factors based on muon pt
			if ((10 <= muonPt) && (muonPt < 20)) {
				correction_A = 0.97187329075;
				correction_B = 0.958160663139;
			}
			else if ((20 <= muonPt) && (muonPt < 30)) {
				correction_A = 0.984568503228;
				correction_B = 0.975536117201;
			}
			else if ((30 <= muonPt) && (muonPt < 40)) {
				correction_A = 0.992423030756;
				correction_B = 0.984073788145;
			}
			else if ((40 <= muonPt) && (muonPt < 50)) {
				correction_A = 0.99535554365;
				correction_B = 0.990656279301;
			}
			else if ((50 <= muonPt) && (muonPt < 60)) {
				correction_A = 0.992170058662;
				correction_B = 0.991084452935;
			}
			else if ((60 <= muonPt) && (muonPt < 80)) {
				correction_A = 0.993872313396;
				correction_B = 0.98892037777;
			}
			else if ((80 <= muonPt) && (muonPt < 250)) {
				correction_A = 0.993271247496;
				correction_B = 0.999774630941;
			}
		}
		else if (fabs(muEta) > 1.2) { // 'pt_abseta>1.2' in pickle file
			//get scale factors based on muon pt
			if ((10 <= muonPt) && (muonPt < 20)) {
				correction_A = 0.989190191868;
				correction_B = 0.999006216758;
			}
			else if ((20 <= muonPt) && (muonPt < 30)) {
				correction_A = 1.00271480782;
				correction_B = 1.00043597215;
			}
			else if ((30 <= muonPt) && (muonPt < 40)) {
				correction_A = 1.00274598636;
				correction_B = 1.0019607868;
			}
			else if ((40 <= muonPt) && (muonPt < 50)) {
				correction_A = 1.00158789661;
				correction_B = 1.00242767691;
			}
			else if ((50 <= muonPt) && (muonPt < 60)) {
				correction_A = 0.99539699871;
				correction_B = 1.00113878923;
			}
			else if ((60 <= muonPt) && (muonPt < 80)) {
				correction_A = 0.995568584925;
				correction_B = 0.993575837027;
			}
			else if ((80 <= muonPt) && (muonPt < 250)) {
				correction_A = 0.988039073331;
				correction_B = 0.993270235255;
			}
		}
		//luminosity weighted average of correction_A and correction_B:
		lumi_2011A = 2.311; //fb^-1
		lumi_2011B = 2.739; //fb^-1
		lumi_2011 = 5.050; //fb^-1
		correction = ((lumi_2011A/lumi_2011) * correction_A) + ((lumi_2011B/lumi_2011)*correction_B);

		//8TeV scale factors from https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonReferenceEffs#22Jan2013_ReReco_of_2012_data_re (from pickle files)
	} else if (centre_of_mass_energy_ == 8){ //corrections for ID ('Tight'), Iso ('combRelIsoPF04dBeta<012_Tight') and Trigger ('IsoMu24', 'TightID_IsodB') respectively (keys used in pickle file)
		if (fabs(muEta) < 0.9) { // 'ptabseta<0.9' in pickle file
			if ((10 <= muonPt) && (muonPt < 20)) {
				id_correction = 0.9702748917248193;
				iso_correction = 0.9403381500487888;
				trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((20 <= muonPt) && (muonPt < 25)) {
				id_correction = 0.9888647105027486;
				iso_correction = 0.9767384928595166;
				trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((25 <= muonPt) && (muonPt < 30)) {
				id_correction = 0.9923382289443887;
				iso_correction = 0.9961727553245637;
				trigger_correction = 0.9837252438433461;
			}
			else if ((30 <= muonPt) && (muonPt < 35)) {
				id_correction = 0.9932832435710769;
				iso_correction = 0.9932276697519965;
				trigger_correction = 0.9840634431547701;
			}
			else if ((35 <= muonPt) && (muonPt < 40)) {
				id_correction = 0.9936619045236875;
				iso_correction = 0.993713125125077;
				trigger_correction = 0.9839165818168554;
			}
			else if ((40 <= muonPt) && (muonPt < 50)) {
				id_correction = 0.9923918872503162;
				iso_correction = 0.9940841647892507;
				trigger_correction = 0.9834525270057036;
			}
			else if ((50 <= muonPt) && (muonPt < 60)) {
				id_correction = 0.9911899786643166;
				iso_correction = 0.9964353940407351;
				trigger_correction = 0.9842917703915748;
			}
			else if ((60 <= muonPt) && (muonPt < 90)) {
				id_correction = 0.9894167956611032;
				iso_correction = 0.9986584316076454;
				trigger_correction = 0.9846720184248945;
			}
			else if ((90 <= muonPt) && (muonPt < 140)) {
				id_correction = 1.0037489877154855;
				iso_correction = 1.0003297152126076;
				trigger_correction = 0.9809171165806959;
			}
			else if ((140 <= muonPt) && (muonPt < 300)) {
				id_correction = 1.0185025540365602;
				iso_correction = 0.998812853360961;
				trigger_correction = 0.9804174981053351; // given for pt '140_500' in pickle file
			}
		} else if ((fabs(muEta) >= 0.9 && fabs(muEta) < 1.2)) { // 'ptabseta0.9-1.2' in pickle file
			if ((10 <= muonPt) && (muonPt < 20)) {
				id_correction = 1.0017313093647269;
				iso_correction = 0.9484342057793206;
				trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((20 <= muonPt) && (muonPt < 25)) {
				id_correction = 0.9939466451892177;
				iso_correction = 0.9863669311896185;
				trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((25 <= muonPt) && (muonPt < 30)) {
				id_correction = 0.9947219657132994;
				iso_correction = 1.0003560413214891;
				trigger_correction = 0.9683812755993191;
			}
			else if ((30 <= muonPt) && (muonPt < 35)) {
				id_correction = 0.9933913481874554;
				iso_correction = 1.0000867333890535;
				trigger_correction = 0.965380548896101;
			}
			else if ((35 <= muonPt) && (muonPt < 40)) {
				id_correction = 0.9922848270630622;
				iso_correction = 0.9990915568314974;
				trigger_correction = 0.9669651415167049;
			}
			else if ((40 <= muonPt) && (muonPt < 50)) {
				id_correction = 0.9918700391817427;
				iso_correction = 0.9988684367869946;
				trigger_correction = 0.966679581608325;
			}
			else if ((50 <= muonPt) && (muonPt < 60)) {
				id_correction = 0.995010062219747;
				iso_correction = 0.9978903999478148;
				trigger_correction = 0.9627395755250187;
			}
			else if ((60 <= muonPt) && (muonPt < 90)) {
				id_correction = 0.99040605451701;
				iso_correction = 0.9992149992903525;
				trigger_correction = 0.9595241683475331;
			}
			else if ((90 <= muonPt) && (muonPt < 140)) {
				id_correction = 1.0090275981046186;
				iso_correction = 1.0014212099113895;
				trigger_correction = 0.9644418246112644;
			}
			else if ((140 <= muonPt) && (muonPt < 300)) {
				id_correction = 1.010956056270124;
				iso_correction = 1.0018540386614887;
				trigger_correction = 0.9712789619617556; // given for pt '140_500' in pickle file
			}
		} else if ((fabs(muEta) >= 1.2 && fabs(muEta) < 2.1)) { // 'ptabseta1.2-2.1' in pickle file
			if ((10 <= muonPt) && (muonPt < 20)) {
				id_correction = 1.0180184284620057;
				iso_correction = 0.9724367240900078;
				trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((20 <= muonPt) && (muonPt < 25)) {
				id_correction = 1.0003513994342943;
				iso_correction = 0.9900544131155273;
				trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((25 <= muonPt) && (muonPt < 30)) {
				id_correction = 0.9984860359215375;
				iso_correction = 1.0028199004178158;
				trigger_correction = 1.0051991254438037;
			}
			else if ((30 <= muonPt) && (muonPt < 35)) {
				id_correction = 0.9965584500063546;
				iso_correction = 1.0040456735929117;
				trigger_correction = 1.0013781590159485;
			}
			else if ((35 <= muonPt) && (muonPt < 40)) {
				id_correction = 0.996026448928709;
				iso_correction = 1.0021465355614672;
				trigger_correction = 0.99616640424792;
			}
			else if ((40 <= muonPt) && (muonPt < 50)) {
				id_correction = 0.9960618126306268;
				iso_correction = 1.0009158373782485;
				trigger_correction = 0.9942541014104305;
			}
			else if ((50 <= muonPt) && (muonPt < 60)) {
				id_correction = 0.9951827274866013;
				iso_correction = 1.0004039805545037;
				trigger_correction = 0.990544673012178;
			}
			else if ((60 <= muonPt) && (muonPt < 90)) {
				id_correction = 0.9924861810666658;
				iso_correction = 1.00050232016842;
				trigger_correction = 0.9882937419288585;
			}
			else if ((90 <= muonPt) && (muonPt < 140)) {
				id_correction = 1.023129380083607;
				iso_correction = 0.9991578234416382;
				trigger_correction = 0.9818759899390823;
			}
			else if ((140 <= muonPt) && (muonPt < 300)) {
				id_correction = 0.9747541719440429;
				iso_correction = 0.9964395746067783;
				trigger_correction = 0.9941686682904833; // given for pt '140_500' in pickle file
			}
		} else if (fabs(muEta) >= 2.1 && fabs(muEta) <= 2.4) { // 'ptabseta2.1-2.4' in pickle file. Note: Trigger scale factors only provided up to absolute eta of 2.1 in the link above, so I have used the same as for the 1.2 to 2.1 eta range.
			if ((10 <= muonPt) && (muonPt < 20)) {
				id_correction = 1.0050443332472756;
				iso_correction = 1.1167270384985806;
				trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((20 <= muonPt) && (muonPt < 25)) {
				id_correction = 0.9980890826544107;
				iso_correction = 1.1155400869984835;
				trigger_correction = 1.0; // corrections only provided for pt>=25 so 1.0 used
			}
			else if ((25 <= muonPt) && (muonPt < 30)) {
				id_correction = 0.9961828904505218;
				iso_correction = 1.096718301830121;
				trigger_correction = 1.0051991254438037;
			}
			else if ((30 <= muonPt) && (muonPt < 35)) {
				id_correction = 1.000551051988681;
				iso_correction = 1.074812169170078;
				trigger_correction = 1.0013781590159485;
			}
			else if ((35 <= muonPt) && (muonPt < 40)) {
				id_correction = 0.9925634188516349;
				iso_correction = 1.0605853576108657;
				trigger_correction = 0.99616640424792;
			}
			else if ((40 <= muonPt) && (muonPt < 50)) {
				id_correction = 0.9951441282077462;
				iso_correction = 1.0377065931130076;
				trigger_correction = 0.9942541014104305;
			}
			else if ((50 <= muonPt) && (muonPt < 60)) {
				id_correction = 0.993590319966609;
				iso_correction = 1.0252924559186363;
				trigger_correction = 0.990544673012178;
			}
			else if ((60 <= muonPt) && (muonPt < 90)) {
				id_correction = 0.9894841861002339;
				iso_correction = 1.0149496896687298;
				trigger_correction = 0.9882937419288585;
			}
			else if ((90 <= muonPt) && (muonPt < 140)) {
				id_correction = 1.0601733432927236;
				iso_correction = 1.0081292468302308;
				trigger_correction = 0.9818759899390823;
			}
			else if ((140 <= muonPt) && (muonPt < 300)) {
				id_correction = 0.890546814737379;
				iso_correction = 1.0106204522044593;
				trigger_correction = 0.9941686682904833; // given for pt '140_500' in pickle file
			}
		}
		correction = id_correction * iso_correction * trigger_correction;
	}
	return correction;
}


DEFINE_FWK_MODULE (UnfoldingAnalyser);


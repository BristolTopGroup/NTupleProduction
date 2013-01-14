#ifndef UNFOLDINGANALYSER
#define UNFOLDINGANALYSER

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "TH1F.h"
#include "TH2F.h"

#include <vector>
#include <string>

class UnfoldingAnalyser: public edm::EDAnalyzer {
public:
	UnfoldingAnalyser(const edm::ParameterSet& iConfig);
	static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);

	virtual void analyze(const edm::Event&, const edm::EventSetup&);
	virtual void beginJob();
	virtual void endJob();

private:
	//non-global event weights (global = i.e. lumi-weight)
	edm::InputTag pu_weight_input_, b_tag_weight_input;
	//distributions
	edm::InputTag gen_MET_input_, reco_MET_input_;
	edm::InputTag gen_jet_input_, jet_input_;
	edm::InputTag electron_input_, muon_input_;
	edm::InputTag vertex_input_, gen_event_input_;
	edm::InputTag selection_flag_input_;
	edm::InputTag is_fully_hadronic_ttbar_flag_, is_dileptonic_ttbar_flag_;
	edm::InputTag is_semileptonic_tau_flag_, is_semileptonic_electron_flag_, is_semileptonic_muon_flag_;
	bool do_electron_channel_; //if false do muon channel
	std::string variable_under_analysis_;
	double variable_min_;
	double variable_max_;
	unsigned int variable_n_bins_;
	std::vector<double> bin_edges_;
	bool is_semileptonic_;
	//in order to be able to create a RooResponse object one needs
	//Does not pass selection
	// - fill truth distribution (1D)
	//passes selection:
	// - fill truth (1D)
	// - fill measured (1D)
	// - fill response (2D): x= measured, y = truth
	//Fake - not really applicable for us and optional for the object creation
	// - fill measured (1D)
	// - fill fake (1D)
	//histograms with 1 GeV binning
	TH1F* truth_, *measured_, *fake_, *contamination_in_gen_variable_, *contamination_in_reco_variable_;
	TH2F* response_, *response_without_fakes_;
	//histograms with analysis binning: [0,25,45,70,100, inf]
	TH1F* truth_asym_bins_, *measured_asym_bins_, *fake_asym_bins_, *contamination_asym_bins_in_gen_variable_,
			*contamination_asym_bins_in_reco_variable_;
	TH2F* response_asym_bins_, *response_without_fakes_asym_bins_;

	//functions
	float get_gen_variable(const edm::Event& iEvent) const;
	float get_reco_variable(const edm::Event& iEvent) const;

	float get_gen_met(const edm::Event& iEvent) const;
	float get_reco_met(const edm::Event& iEvent) const;

	float get_gen_ht(const edm::Event& iEvent) const;
	float get_reco_ht(const edm::Event& iEvent) const;

	float get_gen_st(const edm::Event& iEvent) const;
	float get_reco_st(const edm::Event& iEvent) const;

	float get_gen_mt(const edm::Event& iEvent) const;
	float get_reco_mt(const edm::Event& iEvent) const;

	const reco::GenParticle* get_gen_lepton(const edm::Event& iEvent) const;
	const reco::Candidate* get_reco_lepton(const edm::Event& iEvent) const;

};
#endif


#ifndef UNFOLDINGPRODUCER
#define UNFOLDINGPRODUCER

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"


#include <vector>
#include <TTree.h>

class UnfoldingProducer: public edm::EDProducer {
public:
	UnfoldingProducer(const edm::ParameterSet&);
	static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);

	virtual void produce( edm::Event&, const edm::EventSetup&);
	virtual void beginJob();

private:

	//non-global event weights (global = i.e. lumi-weight)
	edm::InputTag pu_weight_input_, b_tag_weight_input, pdfWeightsInputTag_;
	edm::InputTag leptonWeightsInputTag_;
	//distributions	
	edm::InputTag gen_part_input_;
	edm::InputTag gen_MET_input_, reco_MET_input_;
	edm::InputTag gen_jet_input_, reco_jet_input_;
	edm::InputTag electron_input_, muon_input_;
	edm::InputTag electronIndex_input_, muonIndex_input_;
	edm::InputTag vertex_input_, gen_event_input_;
	edm::InputTag selection_flag_input_;
	edm::InputTag is_fully_hadronic_ttbar_flag_, is_dileptonic_ttbar_flag_;
	edm::InputTag is_semileptonic_tau_flag_, is_semileptonic_electron_flag_, is_semileptonic_muon_flag_;
	bool do_electron_channel_; //if false do muon channel
	bool is_semileptonic_;

	const std::string prefix, suffix, MCSampleTag_;

	bool storePDFWeights_;


	float get_gen_met(const edm::Event& iEvent) const;
	float get_reco_met(const edm::Event& iEvent) const;
	
	float get_gen_ht(const edm::Event& iEvent) const;
	float get_reco_ht(const edm::Event& iEvent, std::string MCSampleTag_) const;

	float get_gen_st(const edm::Event& iEvent) const;
	float get_reco_st(const edm::Event& iEvent, std::string MCSampleTag_) const;

	float get_gen_mt(const edm::Event& iEvent) const;
	float get_reco_mt(const edm::Event& iEvent) const;
	
	float get_gen_wpt(const edm::Event& iEvent) const;
	float get_reco_wpt(const edm::Event& iEvent) const;
	
	const reco::GenParticle* get_gen_lepton(const edm::Event& iEvent) const;
	const reco::Candidate* get_reco_lepton(const edm::Event& iEvent) const;

	const reco::GenParticle* get_gen_leptonicDecayingTop(const edm::Event& iEvent) const;
	const reco::GenParticle* get_gen_hadronicDecayingTop(const edm::Event& iEvent) const;
};
#endif


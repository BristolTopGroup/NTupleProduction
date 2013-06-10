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

	descriptions.add("UnfoldingAnalyser", desc);
}

void UnfoldingAnalyser::beginJob() {
	edm::Service < TFileService > fs;
	if (!fs) {
		throw edm::Exception(edm::errors::Configuration, "TFile Service is not registered in cfg file");
	}
	//cout << "This is not how you debug" << endl;
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

	float gen_variable(get_gen_variable(iEvent));

	if (do_electron_channel_) {
		if (is_semileptonic_electron) {
			//PU weight only (no btag-weight) as no b-tagging is applied
			truth_->Fill(gen_variable, puWeight);
			truth_asym_bins_->Fill(gen_variable, puWeight);
		}

		if (passes_selection) {
			float reco_variable(get_reco_variable(iEvent));

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

		double muonCorrection = get_muon_correction(iEvent);

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
	else if (variable_under_analysis_ == "HT")
		return get_gen_ht(iEvent);
	else if (variable_under_analysis_ == "ST")
		return get_gen_st(iEvent);
	else if (variable_under_analysis_ == "MT")
		return get_gen_mt(iEvent);
	else if (variable_under_analysis_ == "WPT")
		return get_gen_wpt(iEvent);
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

	//Take ALL the jets!
	for (unsigned int index = 0; index < jets->size(); ++index) {
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
	//get Gen MET
	edm::Handle < reco::GenMETCollection > genMETs;
	iEvent.getByLabel(gen_MET_input_, genMETs);
	reco::GenMET met(genMETs->at(0));

//	double En = met.energy();
//	double mom = sqrt(pow(met.px(),2)+pow(met.py(),2)+pow(met.pz(),2));
	
// 	cout << "GEN lep px,y: " <<  lepton->px() << ", " <<   lepton->py() << ") , met px,y,z: " << met.px() << ", " << met.py() << ", "<< met.pz()<<")" << endl;
// 	cout << "missing mass is either: " << pow(En,2)-pow(mom,2) << endl;
// 	//cout << "or: " << 
// 	
// 	cout << "Gen lepE: " <<  lepton->et() << " , metE: " <<  met.et() << endl;
// 	cout << "MET pt: " <<  met.pt() << " , mass: " << met.mass() << endl;
	
	//combine their x & y momenta to get the transverse W boson mass
	double energy_squared = pow(lepton->et() + met.pt(), 2);
	double momentum_squared = pow(lepton->px() + met.px(), 2) + pow(lepton->py() + met.py(), 2);
	double MT_squared = energy_squared - momentum_squared;
//	cout << "MTgen: " << sqrt(MT_squared) << endl;

	if (MT_squared > 0)
		return sqrt(MT_squared);
	else
		return -1;
}

float UnfoldingAnalyser::get_gen_wpt(const edm::Event& iEvent) const {


	if (!is_semileptonic_)
		return -1.;
	//get electron/muon
	//const reco::GenParticle* lepton = get_gen_lepton(iEvent);
	
	//get Gen MET
	edm::Handle < reco::GenMETCollection > genMETs;
	iEvent.getByLabel(gen_MET_input_, genMETs);
	reco::GenMET met(genMETs->at(0));
	
	
	edm::Handle < reco::GenParticleCollection > genParticles;
	iEvent.getByLabel(gen_part_input_, genParticles);
	
	int num = 0;
        std::auto_ptr < std::vector<double> > pt(new std::vector<double>());
	std::auto_ptr < std::vector<int> > pdgId(new std::vector<int>());
	double W_genpt = 0;
	
	
		if (genParticles.isValid()) {
			edm::LogInfo("BristolNTuple_GenParticlesInfo") << "Total # GenParticles: " << genParticles->size();

			for (reco::GenParticleCollection::const_iterator it = genParticles->begin(); it != genParticles->end();
					++it) {
				// exit from loop when you reach the required number of GenParticles
				if (pt->size() >= 24)
					break;
				
					
				num++;
				

				
				
				int idx = -1;
				for (reco::GenParticleCollection::const_iterator mit = genParticles->begin();
						mit != genParticles->end(); ++mit) {
					if (it->mother() == &(*mit)) {
						idx = std::distance(genParticles->begin(), mit);
						break;
					}
				}
				
				
				//cout  << num <<  " ,part: " <<it->pdgId() << " ,px read: " << it->px()  << " ,mother: " << idx << endl;

				// fill in all the vectors
				pt->push_back(it->pt());
 				pdgId->push_back(it->pdgId());
				
				if((fabs(it->pdgId()) == 11 || fabs(it->pdgId()) == 13) && fabs(pdgId->at(idx)) == 24){
				W_genpt = pt->at(idx);
				}
				
	
				}
			} else {
			edm::LogError("BristolNTuple_GenParticlesError") << "Error! Can't get the product " << gen_part_input_;
			}

//	cout << "or from gen met and lepton: " << sqrt(pow(lepton->px()+met.px(),2)+pow(lepton->py()+met.py(),2)) << endl;
//     	return sqrt(pow(lepton->px()+met.px(),2)+pow(lepton->py()+met.py(),2)); 

	return W_genpt;

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
	else if (variable_under_analysis_ == "WPT")
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
	return ht + met + lepton->pt();
}

float UnfoldingAnalyser::get_reco_mt(const edm::Event& iEvent) const {
	//get electron/muon
	const reco::Candidate* lepton = get_reco_lepton(iEvent);
	//get MET
	edm::Handle < std::vector<pat::MET> > recoMETs;
	iEvent.getByLabel(reco_MET_input_, recoMETs);

	pat::MET met(recoMETs->at(0));
	
        //cout << "RECO lep py: " <<  lepton->py() << " , met px: " << met.px() << endl;
	
	
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
	//get MET
	edm::Handle < std::vector<pat::MET> > recoMETs;
	iEvent.getByLabel(reco_MET_input_, recoMETs);

	pat::MET met(recoMETs->at(0));
	
	return sqrt(pow(lepton->px()+met.px(),2)+pow(lepton->py()+met.py(),2)); 
}

const reco::GenParticle* UnfoldingAnalyser::get_gen_lepton(const edm::Event& iEvent) const {
	edm::Handle < TtGenEvent > genEvt;
	iEvent.getByLabel(gen_event_input_, genEvt);

	return genEvt->singleLepton()->clone();
}

const reco::Candidate* UnfoldingAnalyser::get_reco_lepton(const edm::Event& iEvent) const {
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

float UnfoldingAnalyser::get_muon_correction(const edm::Event& iEvent) const {
	//ID, iso and trigger correction respectively from:  https://indico.cern.ch/getFile.py/access?contribId=3&resId=0&materialId=slides&confId=214870
	
	double correction(1.);
	
	edm::Handle < pat::MuonCollection > signalMuon;
	iEvent.getByLabel(muon_input_, signalMuon);
	
	double muEta = signalMuon->at(0).eta();

	if(abs(muEta)<0.9)
		correction = 0.9941*0.9923*0.9560;
	else if(abs(muEta)>=0.9 && abs(muEta)<1.2)
		correction = 0.9917*0.9979*0.9528;
	else if(abs(muEta)>=1.2)
		correction = 0.9982*1.0019*0.9809;
	
	return correction; 
}

DEFINE_FWK_MODULE (UnfoldingAnalyser);


#include "BristolAnalysis/NTupleTools/plugins/UnfoldingAnalyser.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETFwd.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
#include <iostream>
using namespace edm;
using namespace std;

UnfoldingAnalyser::UnfoldingAnalyser(const edm::ParameterSet& iConfig) :
		PUWeightInput_(iConfig.getParameter < edm::InputTag > ("PUWeightInput")), //
		BtagWeightInput_(iConfig.getParameter < edm::InputTag > ("BtagWeightInput")), //
		genMetInput_(iConfig.getParameter < edm::InputTag > ("genMetInput")), //
		recoMetInput_(iConfig.getParameter < edm::InputTag > ("recoMetInput")), //
		selectionFlagInput_(iConfig.getParameter < edm::InputTag > ("selectionFlagInput")), //
		isFullyHadronicTtbarFlag_(iConfig.getParameter < edm::InputTag > ("isFullyHadronicTtbarFlag")), //
		isDiLeptonicTtbarFlag_(iConfig.getParameter < edm::InputTag > ("isDiLeptonicTtbarFlag")), //
		isSemiLeptonicTauFlag_(iConfig.getParameter < edm::InputTag > ("isSemiLeptonicTauFlag")), //
		isSemiLeptonicElectronFlag_(iConfig.getParameter < edm::InputTag > ("isSemiLeptonicElectronFlag")), //
		isSemiLeptonicMuonFlag_(iConfig.getParameter < edm::InputTag > ("isSemiLeptonicMuonFlag")), //
		doElectronChannel_(iConfig.getUntrackedParameter<bool>("doElectronChannel")), //
		truth_(), //
		measured_(), //
		fake_(), //
		contamination_inGenMET_(), //
		contamination_inRecoMET_(), //
		response_(), //
		truth_AsymBins_(), //
		measured_AsymBins_(), //
		fake_AsymBins_(), //
		contamination_AsymBins_inGenMET_(), //
		contamination_AsymBins_inRecoMET_(), //
		response_AsymBins_() {

}

void UnfoldingAnalyser::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("PUWeightInput");
	desc.add < InputTag > ("BtagWeightInput");
	desc.add < InputTag > ("genMetInput");
	desc.add < InputTag > ("recoMetInput");
	desc.add < InputTag > ("selectionFlagInput");
	desc.add < InputTag > ("isFullyHadronicTtbarFlag");
	desc.add < InputTag > ("isDiLeptonicTtbarFlag");
	desc.add < InputTag > ("isSemiLeptonicTauFlag");
	desc.add < InputTag > ("isSemiLeptonicElectronFlag");
	desc.add < InputTag > ("isSemiLeptonicMuonFlag");
	desc.addUntracked<bool>("doElectronChannel", false);

	descriptions.add("UnfoldingAnalyser", desc);
}

void UnfoldingAnalyser::beginJob() {
	edm::Service < TFileService > fs;
	if (!fs) {
		throw edm::Exception(edm::errors::Configuration, "TFile Service is not registered in cfg file");
	}
	cout << "This is not how you debug" << endl;
	truth_ = fs->make < TH1F > ("truth", "True distribution;GEN(MET);# Events", 2000, 0., 2000.);
	measured_ = fs->make < TH1F > ("measured", "Measured distribution;RECO(MET);# Events", 2000, 0., 2000.);
	fake_ = fs->make < TH1F > ("fake", "background distribution;RECO(MET);# Events", 2000, 0., 2000.);
	contamination_inGenMET_ = fs->make < TH1F
			> ("contamination_inGenMET", "background distribution;GEN(MET);# Events", 2000, 0., 2000.);
	contamination_inRecoMET_ = fs->make < TH1F
			> ("contamination_inRecoMET", "background distribution;RECO(MET);# Events", 2000, 0., 2000.);

	response_ = fs->make < TH2F > ("response", "response;RECO(MET);GEN(MET)", 2000, 0., 2000., 2000, 0., 2000.);
	
//histograms with asymmetric bins (final measurement)
	cout << "But what other options do I have?" << endl;
float METBinEdges[6] = { 0, 25, 45, 70, 100, 2000 };

	truth_AsymBins_ = fs->make < TH1F > ("truth_AsymBins", "True distribution;GEN(MET);# Events", 5, METBinEdges);
	measured_AsymBins_ = fs->make < TH1F > ("measured_AsymBins", "Measured distribution;RECO(MET);# Events", 5, METBinEdges);
	fake_AsymBins_ = fs->make < TH1F > ("fake_AsymBins", "background distribution;RECO(MET);# Events", 5, METBinEdges);
	contamination_AsymBins_inGenMET_ = fs->make < TH1F
			> ("contamination_AsymBins_inGenMET", "background distribution;GEN(MET);# Events", 5, METBinEdges);
	contamination_AsymBins_inRecoMET_ = fs->make < TH1F
			> ("contamination_AsymBins_inRecoMET", "background distribution;RECO(MET);# Events", 5, METBinEdges);
	response_AsymBins_ = fs->make < TH2F > ("response_AsymBins", "response;RECO(MET);GEN(MET)", 5, METBinEdges, 5, METBinEdges);

cout << "Well, you could use 'scram b' as a compiler on your machine within an IDE" << endl;
	truth_->Sumw2();
	measured_->Sumw2();
	fake_->Sumw2();
	contamination_inGenMET_->Sumw2();
	contamination_inRecoMET_->Sumw2();
	response_->Sumw2();

	truth_AsymBins_->Sumw2();
	measured_AsymBins_->Sumw2();
	fake_AsymBins_->Sumw2();
	contamination_AsymBins_inGenMET_->Sumw2();
	contamination_AsymBins_inRecoMET_->Sumw2();
	response_AsymBins_->Sumw2();
cout << "However, you need to be able to install CMSSW on your machine." << endl;
}

void UnfoldingAnalyser::endJob() {

}

void UnfoldingAnalyser::analyze(const edm::Event& iEvent, const edm::EventSetup&) {
	if (iEvent.isRealData()) { //this analysis should only be done on MC
		return;
	}

	edm::Handle<double> puWeightHandle;
	iEvent.getByLabel(PUWeightInput_, puWeightHandle);

	edm::Handle<double> btagWeightHandle;
	iEvent.getByLabel(BtagWeightInput_, btagWeightHandle);

	double puWeight(*puWeightHandle);
	double btagWeight(*btagWeightHandle);
	double weight(puWeight * btagWeight);

	bool passesSelection(passesFilter(iEvent, selectionFlagInput_));
	bool isFullyHadronicTtbar(passesFilter(iEvent, isFullyHadronicTtbarFlag_));
	bool isDiLeptonicTtbar(passesFilter(iEvent, isDiLeptonicTtbarFlag_));
	bool isSemiLeptonicTau(passesFilter(iEvent, isSemiLeptonicTauFlag_));
	bool isSemiLeptonicElectron(passesFilter(iEvent, isSemiLeptonicElectronFlag_));
	bool isSemiLeptonicMuon(passesFilter(iEvent, isSemiLeptonicMuonFlag_));

	edm::Handle < reco::GenMETCollection > genMETs;
	iEvent.getByLabel(genMetInput_, genMETs);

	edm::Handle < std::vector<pat::MET> > recoMETs;
	iEvent.getByLabel(recoMetInput_, recoMETs);

	reco::GenMET genMETObject(genMETs->at(0));
	pat::MET recoMETObject(recoMETs->at(0));
	double genMET(genMETObject.pt());
	double recoMET(recoMETObject.pt());

	if (doElectronChannel_) {
		if (isSemiLeptonicElectron) {
			//PU weight only (no btag-weight) as no b-tagging is applied
			truth_->Fill(genMET, puWeight);
			truth_AsymBins_->Fill(genMET, puWeight);
		}

		if (passesSelection) {
			measured_->Fill(recoMET, weight);
			measured_AsymBins_->Fill(recoMET, weight);
			response_->Fill(recoMET, genMET, weight);
			response_AsymBins_->Fill(recoMET, genMET, weight);

			if (!isSemiLeptonicElectron) {
				fake_->Fill(recoMET, weight);
				fake_AsymBins_->Fill(recoMET, weight);
				//contamination from other ttbar processes
				if (isFullyHadronicTtbar || isDiLeptonicTtbar || isSemiLeptonicTau || isSemiLeptonicMuon) {
					contamination_inRecoMET_->Fill(recoMET, weight);
					contamination_AsymBins_inRecoMET_->Fill(recoMET, weight);
					contamination_inGenMET_->Fill(genMET, weight);
					contamination_AsymBins_inGenMET_->Fill(genMET, weight);
				}
			}

		}

	} else { //muon channel
		if (isSemiLeptonicMuon) {
			truth_->Fill(genMET, weight);
			truth_AsymBins_->Fill(genMET, weight);
		}

		if (passesSelection) {
			measured_->Fill(recoMET, weight);
			measured_AsymBins_->Fill(recoMET, weight);
			response_->Fill(recoMET, genMET, weight);
			response_AsymBins_->Fill(recoMET, genMET, weight);

			if (!isSemiLeptonicMuon) {
				fake_->Fill(recoMET, weight);
				fake_AsymBins_->Fill(recoMET, weight);
				if (isFullyHadronicTtbar || isDiLeptonicTtbar || isSemiLeptonicTau || isSemiLeptonicElectron) {
					contamination_inRecoMET_->Fill(recoMET, weight);
					contamination_AsymBins_inRecoMET_->Fill(recoMET, weight);
					contamination_inGenMET_->Fill(genMET, weight);
					contamination_AsymBins_inGenMET_->Fill(genMET, weight);
				}
			}
		}
	}
}

DEFINE_FWK_MODULE (UnfoldingAnalyser);


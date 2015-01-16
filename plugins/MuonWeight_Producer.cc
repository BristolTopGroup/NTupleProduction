#include "BristolAnalysis/NTupleTools/plugins/MuonWeight_Producer.h"
#include "BristolAnalysis/NTupleTools/interface/MuonWeight.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include <boost/filesystem.hpp>
#include <boost/scoped_ptr.hpp>
#include <TFile.h>

using namespace edm;
using namespace std;

MuonWeight_Producer::MuonWeight_Producer(const edm::ParameterSet& iConfig) :
		muonInput_(iConfig.getParameter < InputTag > ("muonInput")), //
		prefix_(iConfig.getParameter < string > ("prefix")), //
		MCSampleTag_(iConfig.getParameter < std::string > ("MCSampleTag")) , //
		Systematic_(iConfig.getParameter<int>("MuonSystematic")),
		muonScaleFactorsFile_(iConfig.getParameter < edm::FileInPath > ("muonScaleFactorsFile")) {
	produces<std::vector<double> >();

	if (!boost::filesystem::exists(muonScaleFactorsFile_.fullPath())) {
		cerr << "ConfigFile::getMuonIdIsoScaleFactorsHistogram(" << muonScaleFactorsFile_ << "): could not find file" << endl;
	throw "Could not find muon ID & iso scale factors histogram file in " + muonScaleFactorsFile_.fullPath();
	}

	boost::scoped_ptr<TFile> file(TFile::Open(muonScaleFactorsFile_.fullPath().c_str()));
	muonIdIsoScaleFactorsHistogram_ = (boost::shared_ptr<TH2F>) (TH2F*) file->Get("SF_2011_TIGHT_ISO_PT25_PtrgL_eta_pt_PLOT")->Clone() ;
	muonTriggerScaleFactorsHistogram_ = (boost::shared_ptr<TH3F>) (TH3F*) file->Get("SF_2011_HLT_TisoMu24eta2p1_IsoMu24_eta2p1_charge_eta_pt_PLOT")->Clone() ;
	file->Close();
}

void MuonWeight_Producer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	std::vector<double> muonWeights;

	if (!iEvent.isRealData()) {
		//get jets and numberOfBtags
		edm::Handle < pat::MuonCollection > muons;
		iEvent.getByLabel(muonInput_, muons);
		muonWeights = MuonWeights(*muons, &*muonIdIsoScaleFactorsHistogram_, &*muonTriggerScaleFactorsHistogram_, Systematic_, MCSampleTag_);
	}

	std::auto_ptr<std::vector<double> > muonWeightProduct(new std::vector<double>(muonWeights));
	//-----------------------------------------------------------------
	iEvent.put(muonWeightProduct);
}

void MuonWeight_Producer::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("muonInput");
	desc.add < string > ("prefix", "MuonWeight_Producer");
	desc.add < string > ("MCSampleTag");
	desc.add<int>("MuonSystematic", 0);
	desc.add < edm::FileInPath > ("muonScaleFactorsFile");

	descriptions.add("MuonWeight_Producer", desc);
}

DEFINE_FWK_MODULE (MuonWeight_Producer);


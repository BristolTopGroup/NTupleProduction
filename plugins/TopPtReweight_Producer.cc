#include "BristolAnalysis/NTupleTools/plugins/TopPtReweight_Producer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"

using namespace edm;
using namespace std;

TopPtReweight_Producer::TopPtReweight_Producer(const edm::ParameterSet& iConfig) :
		gen_event_input_(iConfig.getParameter < InputTag > ("gen_event_input")),
		genParticles_(iConfig.getParameter < InputTag > ("genParticles")),
		prefix_(iConfig.getParameter < string > ("prefix")) {
		//TopPtSystematic_(iConfig.getParameter<int>("TopPtSystematic")) {
		produces <double>();
}

void TopPtReweight_Producer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {


/*	suppose to do it this way, but it doesn't seem to work because it seems to pick up pt values of 0 for the leptonic and hadronic tops:

	std::vector<double> topPtWeights;
	double topPtReweight(1.0);
	double leptonicTopPt = 0.0;
	double hadronicTopPt = 0.0;
	double scaleFactorLeptonicTop = 0.0;
	double scaleFactorHadronicTop = 0.0;

	//carry out top pt reweighting only if monte carlo
	if (!iEvent.isRealData()) {
		//get the generated event
		edm::Handle < TtGenEvent > genEvt;
		iEvent.getByLabel(gen_event_input_, genEvt);

		if (genEvt -> leptonicDecayTop()) {
			leptonicTopPt = genEvt -> leptonicDecayTop() -> pt();
		}
		if (genEvt -> hadronicDecayTop()) {
			hadronicTopPt = genEvt -> hadronicDecayTop() -> pt();
		}

		// calculate scale factors (using info from:
		// https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting#MC_SFs_Reweighting)
		scaleFactorLeptonicTop = exp(0.159 - 0.00141*leptonicTopPt);
		scaleFactorHadronicTop = exp(0.159 - 0.00141*hadronicTopPt);

		//calculate the event weight
		topPtReweight = sqrt(scaleFactorLeptonicTop * scaleFactorHadronicTop);
	}

*/

	//so now doing the pt reweighting as in the analysis tools by going through all the particles in the gen event and
	//identifying the top and antitop using their pdgids.
	std::vector<double> topPtWeights;
	double topPtReweight(1.0);
	double topPt = 0.0;
	double antiTopPt = 0.0;
	double scaleFactorTop = 0.0;
	double scaleFactorAntiTop = 0.0;

	//carry out top pt reweighting only if monte carlo
	if (!iEvent.isRealData()) {
		//get the generated event
		edm::Handle < reco::GenParticleCollection > genParticles;
		iEvent.getByLabel(genParticles_, genParticles);

		topPt = 0;
		antiTopPt = 0;
		for (size_t i = 0; i < genParticles->size(); i++) {
			const reco::Candidate & particle = (*genParticles)[i];
			if (particle.pdgId() == 6) topPt = particle.pt();
			if (particle.pdgId() == -6) antiTopPt = particle.pt();
		}

		// calculate scale factors (using info from:
		// https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting#MC_SFs_Reweighting)

		scaleFactorTop = exp(0.159 - 0.00141*topPt);
		scaleFactorAntiTop = exp(0.159 - 0.00141*antiTopPt);

		//calculate the event weight
		topPtReweight = sqrt(scaleFactorTop * scaleFactorAntiTop);
	}

	std::auto_ptr<double> topPtReweightPointer(new double(topPtReweight));
	iEvent.put(topPtReweightPointer);

}

void TopPtReweight_Producer::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("gen_event_input");
	desc.add < InputTag > ("genParticles");
	desc.add < string > ("prefix");
	//desc.add < int > ("TopPtSystematic");

	descriptions.add("TopPtReweight_Producer", desc);
}


DEFINE_FWK_MODULE (TopPtReweight_Producer);

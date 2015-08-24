#include "BristolAnalysis/NTupleTools/plugins/UnfoldingProducer.h"
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

UnfoldingProducer::UnfoldingProducer(const edm::ParameterSet& iConfig) :
		pu_weight_input_(iConfig.getParameter < edm::InputTag > ("pu_weight_input")), //
		b_tag_weight_input(iConfig.getParameter < edm::InputTag > ("b_tag_weight_input")), //
		pdfWeightsInputTag_(iConfig.getParameter < edm::InputTag > ("PDFWeightsInputTag")), //
		leptonWeightsInputTag_(iConfig.getParameter < edm::InputTag > ("leptonWeightsInputTag")), //
		gen_part_input_(iConfig.getParameter < edm::InputTag > ("gen_part_input")), //
		gen_MET_input_(iConfig.getParameter < edm::InputTag > ("gen_MET_input")), //
		reco_MET_input_(iConfig.getParameter < edm::InputTag > ("reco_MET_Input")), //	
		gen_jet_input_(iConfig.getParameter < edm::InputTag > ("gen_jet_input")), //
		reco_jet_input_(iConfig.getParameter < edm::InputTag > ("reco_jet_input")), //
		electron_input_(iConfig.getParameter < edm::InputTag > ("electron_input")), //
		muon_input_(iConfig.getParameter < edm::InputTag > ("muon_input")), //
		electronIndex_input_(iConfig.getParameter < edm::InputTag > ("electronIndex_input")), //
		muonIndex_input_(iConfig.getParameter < edm::InputTag > ("muonIndex_input")), //
		vertex_input_(iConfig.getParameter < edm::InputTag > ("vertex_input")), //
		gen_event_input_(iConfig.getParameter < edm::InputTag > ("gen_event_input")), //
		selection_flag_input_(iConfig.getParameter < edm::InputTag > ("selection_flag_input")), //
		is_semileptonic_electron_flag_(iConfig.getParameter < edm::InputTag > ("is_semileptonic_electron_flag")), //
		is_semileptonic_muon_flag_(iConfig.getParameter < edm::InputTag > ("is_semileptonic_muon_flag")), //
		do_electron_channel_(iConfig.getUntrackedParameter<bool>("do_electron_channel")), //
		is_semileptonic_(false), //
		prefix(iConfig.getParameter < std::string > ("Prefix")), //
		suffix(iConfig.getParameter < std::string > ("Suffix")), //
		MCSampleTag_(iConfig.getParameter < std::string > ("MCSampleTag")), //
		storePDFWeights_(iConfig.getParameter < bool > ("storePDFWeights")) //
		{
	produces<double>(prefix+"puWeight"+suffix);
	produces<double>(prefix+"bTagWeight"+suffix);
	if ( storePDFWeights_ ) {
		produces < std::vector<double> > (prefix + "PDFWeights" + suffix);
	}
	produces<double>(prefix+"leptonWeight"+suffix);
	produces<double>(prefix+"leptonEta"+suffix);
	produces<double>(prefix+"leptonPt"+suffix);
	produces< std::vector<double> >(prefix+"jetPt"+suffix);
	produces< std::vector<double> >(prefix+"jetEta"+suffix);
	produces< std::vector<int> >(prefix+"jetPartonFlavour"+suffix);
	produces<double>(prefix+"leptonicTopPt"+suffix);
	produces<double>(prefix+"hadronicTopPt"+suffix);
	produces<double>(prefix+"genMET"+suffix);
	produces<double>(prefix+"genST"+suffix);
	produces<double>(prefix+"genHT"+suffix);
	produces<double>(prefix+"genWPT"+suffix);
	produces<double>(prefix+"genMT"+suffix);
	produces<double>(prefix+"recoMET"+suffix);
	produces<double>(prefix+"recoST"+suffix);
	produces<double>(prefix+"recoHT"+suffix);
	produces<double>(prefix+"recoWPT"+suffix);
	produces<double>(prefix+"recoMT"+suffix);
	produces<bool>(prefix+"GenSelection"+suffix);
	produces<bool>(prefix+"OfflineSelection"+suffix);
}

void UnfoldingProducer::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("pu_weight_input");
	desc.add < InputTag > ("b_tag_weight_input");
	desc.add < InputTag > ("PDFWeightsInputTag");
	desc.add < InputTag > ("leptonWeightsInputTag");
	desc.add < InputTag > ("gen_part_input");
	desc.add < InputTag > ("gen_MET_input");
	desc.add < InputTag > ("reco_MET_Input");
	desc.add < InputTag > ("gen_jet_input");
	desc.add < InputTag > ("reco_jet_input");
	desc.add < InputTag > ("electron_input");
	desc.add < InputTag > ("muon_input");
	desc.add < InputTag > ("electronIndex_input");
	desc.add < InputTag > ("muonIndex_input");
	desc.add < InputTag > ("vertex_input");
	desc.add < InputTag > ("gen_event_input");
	desc.add < InputTag > ("selection_flag_input");
	desc.add < InputTag > ("is_semileptonic_electron_flag");
	desc.add < InputTag > ("is_semileptonic_muon_flag");
	desc.addUntracked<bool>("do_electron_channel", false);
	desc.add < string > ("Prefix");
	desc.add < string > ("Suffix");
	desc.add < bool > ("storePDFWeights");
	desc.add < std::string > ("MCSampleTag", "Summer12");

	descriptions.add("UnfoldingProducer", desc);
}

void UnfoldingProducer::beginJob() {
}

void UnfoldingProducer::produce( edm::Event& iEvent, const edm::EventSetup&) {
	if (iEvent.isRealData()) { //this analysis should only be done on MC
		return;
	}

	edm::Handle<double> puWeightHandle;
	iEvent.getByLabel(pu_weight_input_, puWeightHandle);

	edm::Handle<double> btagWeightHandle;
	iEvent.getByLabel(b_tag_weight_input, btagWeightHandle);

	// Store pu and btag weights
	std::auto_ptr<double> puWeight(new double(*puWeightHandle));
	iEvent.put(puWeight, prefix+"puWeight"+suffix);
	std::auto_ptr<double> bTagWeight(new double(*btagWeightHandle));
	iEvent.put(bTagWeight, prefix+"bTagWeight"+suffix);


	// Store pdf weights
	if ( storePDFWeights_ ) {
		std::auto_ptr < std::vector<double> > pdfWeights(new std::vector<double>());

		edm::Handle < std::vector<double> > pdfWeightsHandle;
		iEvent.getByLabel(pdfWeightsInputTag_, pdfWeightsHandle);
		*pdfWeights.get() = *pdfWeightsHandle;
		iEvent.put(pdfWeights, prefix + "PDFWeights" + suffix);
	}

	// Store lepton eta and pt
	// For muon scale factors/corrections
	const reco::Candidate*  signalLepton = get_reco_lepton( iEvent );
	std::auto_ptr<double> leptonEta(new double(-99));
	std::auto_ptr<double> leptonPt(new double(-1));
	if ( signalLepton != 0 ) {
		*leptonEta = signalLepton->eta();
		*leptonPt = signalLepton->pt();
	}
	iEvent.put(leptonEta, prefix+"leptonEta"+suffix);
	iEvent.put(leptonPt, prefix+"leptonPt"+suffix);

	edm::Handle<std::vector<double> > leptonWeightHandle;
	iEvent.getByLabel(leptonWeightsInputTag_, leptonWeightHandle);
	edm::Handle<unsigned int> leptonIndexHandle;
	if (do_electron_channel_) {
		iEvent.getByLabel(muonIndex_input_, leptonIndexHandle);
	}
	else {
		iEvent.getByLabel(electronIndex_input_, leptonIndexHandle);
	}

	std::auto_ptr<double> leptonWeight(new double(0));

	if ( *leptonIndexHandle < leptonWeightHandle->size() ) {
		*leptonWeight = leptonWeightHandle->at(*leptonIndexHandle);
	}
	iEvent.put(leptonWeight,prefix+"leptonWeight"+suffix);

	// Store jet pt, eta and parton
	// To allow different b tag scale factors to be applied
	edm::Handle < pat::JetCollection > jets;
	iEvent.getByLabel(reco_jet_input_, jets);

	std::auto_ptr<std::vector<double> > jetEta(new std::vector<double>());
	std::auto_ptr<std::vector<double> > jetPt(new std::vector<double>());
	std::auto_ptr<std::vector<int> > jetParton(new std::vector<int>());
	for (unsigned int index = 0; index < jets->size(); ++index) {
		const pat::Jet jet = jets->at(index);
		jetEta->push_back( jet.eta() );
		jetPt->push_back( jet.pt() );
		jetParton->push_back( jet.partonFlavour() );
	}

	iEvent.put( jetEta, prefix+"jetEta"+suffix );
	iEvent.put( jetPt, prefix+"jetPt"+suffix );
	iEvent.put( jetParton, prefix+"jetPartonFlavour"+suffix );

	// Store top pt
	const reco::GenParticle* leptonicTop = get_gen_leptonicDecayingTop(iEvent);
	std::auto_ptr<double> leptonicTopPt(new double(-1));
	if ( leptonicTop != 0 )
		*leptonicTopPt = leptonicTop->pt();
	iEvent.put(leptonicTopPt, prefix+"leptonicTopPt"+suffix);

	const reco::GenParticle* hadronicTop = get_gen_hadronicDecayingTop(iEvent);
	std::auto_ptr<double> hadronicTopPt(new double(-1));
	if ( hadronicTop != 0 )
		*hadronicTopPt = hadronicTop->pt();
	iEvent.put(hadronicTopPt, prefix+"hadronicTopPt"+suffix);

	// Store selection flags
	std::auto_ptr<bool> passes_selection(new bool(passesFilter(iEvent, selection_flag_input_)));
	std::auto_ptr<bool> is_semileptonic_electron(new bool(passesFilter(iEvent, is_semileptonic_electron_flag_)));
	std::auto_ptr<bool> is_semileptonic_muon(new bool(passesFilter(iEvent, is_semileptonic_muon_flag_)));
	is_semileptonic_ = ( *is_semileptonic_electron || *is_semileptonic_muon );

	iEvent.put(passes_selection, prefix+"OfflineSelection"+suffix);
	if ( do_electron_channel_ )
		iEvent.put(is_semileptonic_electron, prefix+"GenSelection"+suffix);
	else
		iEvent.put(is_semileptonic_muon, prefix+"GenSelection"+suffix);


	// Store gen variables
	// MET
	std::auto_ptr<double> genMET(new double(get_gen_met(iEvent)));
	iEvent.put(genMET, prefix+"genMET"+suffix);

	// ST
	std::auto_ptr<double> genST(new double(get_gen_st(iEvent)));
	iEvent.put(genST, prefix+"genST"+suffix);

	//HT
	std::auto_ptr<double> genHT(new double(get_gen_ht(iEvent)));
	iEvent.put(genHT, prefix+"genHT"+suffix);

	//WPT
	std::auto_ptr<double> genWPT(new double(get_gen_wpt(iEvent)));
	iEvent.put(genWPT, prefix+"genWPT"+suffix);

	//MT
	std::auto_ptr<double> genMT(new double(get_gen_mt(iEvent)));
	iEvent.put(genMT, prefix+"genMT"+suffix);

	// Store reco variables
	// MET
	std::auto_ptr<double> recoMET(new double(get_reco_met(iEvent)));
	iEvent.put(recoMET, prefix+"recoMET"+suffix);

	// ST
	std::auto_ptr<double> recoST(new double(get_reco_st(iEvent, MCSampleTag_)));
	iEvent.put(recoST, prefix+"recoST"+suffix);

	//HT
	std::auto_ptr<double> recoHT(new double(get_reco_ht(iEvent, MCSampleTag_)));
	iEvent.put(recoHT, prefix+"recoHT"+suffix);

	//WPT
	std::auto_ptr<double> recoWPT(new double(get_reco_wpt(iEvent)));
	iEvent.put(recoWPT, prefix+"recoWPT"+suffix);

	//MT
	std::auto_ptr<double> recoMT(new double(get_reco_mt(iEvent)));
	iEvent.put(recoMT, prefix+"recoMT"+suffix);
}
float UnfoldingProducer::get_gen_met(const edm::Event& iEvent) const {
	
	edm::Handle < reco::GenMETCollection > genMETs;
	iEvent.getByLabel(gen_MET_input_, genMETs);
	reco::GenMET genMETObject(genMETs->at(0));
	
	return genMETObject.pt();
}

float UnfoldingProducer::get_gen_ht(const edm::Event& iEvent) const {
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

float UnfoldingProducer::get_gen_st(const edm::Event& iEvent) const {
	if (!is_semileptonic_)
		return -1.;
	// ST = HT + MET + lepton pt
	float ht = get_gen_ht(iEvent);
	float met = get_gen_met(iEvent);
	
	//get lepton
	const reco::GenParticle* lepton = get_gen_lepton(iEvent);
	return ht + met + lepton->pt();
}


float UnfoldingProducer::get_gen_mt(const edm::Event& iEvent) const {
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
//	cout << "MTgen: " << sqrt(MT_squared) << endl;
	
	if (MT_squared > 0)
		return sqrt(MT_squared);
	else
		return -1;
}

float UnfoldingProducer::get_gen_wpt(const edm::Event& iEvent) const {
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

float UnfoldingProducer::get_reco_met(const edm::Event& iEvent) const {
	edm::Handle < std::vector<pat::MET> > recoMETs;
	iEvent.getByLabel(reco_MET_input_, recoMETs);


	pat::MET recoMETObject(recoMETs->at(0));

	return recoMETObject.pt();
}

float UnfoldingProducer::get_reco_ht(const edm::Event& iEvent, std::string MCSampleTag_) const {
	edm::Handle < pat::JetCollection > jets;
	iEvent.getByLabel(reco_jet_input_, jets);
	float ht(0.);

	//Take ALL the jets!
	for (unsigned int index = 0; index < jets->size(); ++index) {
		const pat::Jet jet = jets->at(index);
		ht += getSmearedJetPtScale(jets->at(index), 0, MCSampleTag_)*jets->at(index).pt();
	}
	return ht;
}

float UnfoldingProducer::get_reco_st(const edm::Event& iEvent, std::string MCSampleTag_) const {
	// ST = HT + MET + lepton pt
	float ht = get_reco_ht(iEvent, MCSampleTag_);
	float met = get_reco_met(iEvent);
	//get lepton
	const reco::Candidate* lepton = get_reco_lepton(iEvent);
	if ( lepton == 0 )
		return -1;

	return ht + met + lepton->pt();
}

float UnfoldingProducer::get_reco_mt(const edm::Event& iEvent) const {
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

float UnfoldingProducer::get_reco_wpt(const edm::Event& iEvent) const {
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

const reco::GenParticle* UnfoldingProducer::get_gen_lepton(const edm::Event& iEvent) const {
	edm::Handle < TtGenEvent > genEvt;
	iEvent.getByLabel(gen_event_input_, genEvt);

	return genEvt->singleLepton();
}

const reco::Candidate* UnfoldingProducer::get_reco_lepton(const edm::Event& iEvent) const {
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

const reco::GenParticle* UnfoldingProducer::get_gen_leptonicDecayingTop(const edm::Event& iEvent) const {
	edm::Handle < TtGenEvent > genEvt;
	iEvent.getByLabel(gen_event_input_, genEvt);

	if ( genEvt->isSemiLeptonic() )
		return genEvt->leptonicDecayTop();
	else return 0;
}

const reco::GenParticle* UnfoldingProducer::get_gen_hadronicDecayingTop(const edm::Event& iEvent) const {
	edm::Handle < TtGenEvent > genEvt;
	iEvent.getByLabel(gen_event_input_, genEvt);

	if ( genEvt->isSemiLeptonic() )
		return genEvt->hadronicDecayTop();
	else return 0;
}

DEFINE_FWK_MODULE (UnfoldingProducer);


#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenEventInfo.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "boost/filesystem.hpp"

#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"

#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"


#include <iostream>

using namespace std;

const double LARGE_NEGATIVE_INIT_VALUE = -9999.9;

BristolNTuple_GenEventInfo::BristolNTuple_GenEventInfo(const edm::ParameterSet& iConfig) : //
		genEvtInfoInputTag(consumes< GenEventInfoProduct > (iConfig.getParameter<edm::InputTag>("GenEventInfoInputTag"))),
		lheEventProductToken_(consumes< LHEEventProduct > (iConfig.getParameter<edm::InputTag>("LHEEventInfoInputTag"))),
	    genJetsInputTag_(consumes<reco::GenJetCollection > (iConfig.getParameter<edm::InputTag>("GenJetsInputTag"))),
		puWeightsInputTag_(iConfig.getParameter < edm::InputTag > ("PUWeightsInputTag")), //
		storePDFWeights_(iConfig.getParameter<bool>("StorePDFWeights")), //
		isTTbarMC_(iConfig.getParameter<bool>("isTTbarMC")), //
		pdfWeightsInputTag_(iConfig.getParameter < edm::InputTag > ("PDFWeightsInputTag")), //
		pileupInfoSrc_(consumes< std::vector< PileupSummaryInfo> > (iConfig.getParameter < edm::InputTag > ("pileupInfo"))), //
		tt_gen_event_input_(consumes<TtGenEvent > (iConfig.getParameter < edm::InputTag > ("tt_gen_event_input"))), //
	    minGenJetPt_ (iConfig.getParameter<double> ("minGenJetPt")),
	    maxGenJetAbsoluteEta_ (iConfig.getParameter<double> ("maxGenJetAbsoluteEta")),
		prefix_(iConfig.getParameter < std::string > ("Prefix")), //
		suffix_(iConfig.getParameter < std::string > ("Suffix")), //
		prunedGenToken_(consumes<edm::View<reco::GenParticle> >(iConfig.getParameter<edm::InputTag>("prunedGenParticles"))), //
		packedGenToken_(consumes<edm::View<pat::PackedGenParticle> >(iConfig.getParameter<edm::InputTag>("packedGenParticles")))
		{

    for (edm::InputTag const & tag : iConfig.getParameter< std::vector<edm::InputTag> > ("ttbarDecayFlags"))
    ttbarDecayFlags_.push_back(consumes<bool>(tag));
			
	produces<unsigned int>(prefix_ + "ProcessID" + suffix_);
	produces<double>(prefix_ + "PtHat" + suffix_);
	produces<double>(prefix_ + "PUWeight" + suffix_);
	produces<double>(prefix_ + "generatorWeight" + suffix_);
	produces<double>(prefix_ + "centralLHEWeight" + suffix_);
	produces <std::vector<double> > ( prefix_ + "systematicWeights" + suffix_ );
	produces <std::vector<int> > ( prefix_ + "systematicWeightIDs" + suffix_ );

//	produces < std::vector<double> > (prefix_ + "PDFWeights" + suffix_);
	produces < std::vector<int> > (prefix_ + "PileUpInteractions" + suffix_);
	produces < std::vector<int> > (prefix_ + "NumberOfTrueInteractions" + suffix_);
	produces < std::vector<int> > (prefix_ + "PileUpOriginBX" + suffix_);
	produces<unsigned int>(prefix_ + "TtbarDecay" + suffix_);


	produces<int>(prefix_ + "leptonicBGenJetIndex" + suffix_ );
	produces<int>(prefix_ + "hadronicBGenJetIndex" + suffix_ );
	produces<int>(prefix_ + "hadronicDecayQuarkBarGenJetIndex" + suffix_ );
	produces<int>(prefix_ + "hadronicDecayQuarkGenJetIndex" + suffix_ );


	produces<double>(prefix_ + "leptonicTopPt" + suffix_ );
	produces<double>(prefix_ + "leptonicTopPx" + suffix_ );
	produces<double>(prefix_ + "leptonicTopPy" + suffix_ );
	produces<double>(prefix_ + "leptonicTopPz" + suffix_ );
	produces<double>(prefix_ + "leptonicTopEnergy" + suffix_ );
	produces<double>(prefix_ + "hadronicTopPt" + suffix_ );
	produces<double>(prefix_ + "hadronicTopPx" + suffix_ );
	produces<double>(prefix_ + "hadronicTopPy" + suffix_ );
	produces<double>(prefix_ + "hadronicTopPz" + suffix_ );
	produces<double>(prefix_ + "hadronicTopEnergy" + suffix_ );

	produces<double>(prefix_ + "leptonicBPt" + suffix_ );
	produces<double>(prefix_ + "leptonicBPx" + suffix_ );
	produces<double>(prefix_ + "leptonicBPy" + suffix_ );
	produces<double>(prefix_ + "leptonicBPz" + suffix_ );
	produces<double>(prefix_ + "leptonicBEnergy" + suffix_ );
	produces<double>(prefix_ + "hadronicBPt" + suffix_ );
	produces<double>(prefix_ + "hadronicBPx" + suffix_ );
	produces<double>(prefix_ + "hadronicBPy" + suffix_ );
	produces<double>(prefix_ + "hadronicBPz" + suffix_ );
	produces<double>(prefix_ + "hadronicBEnergy" + suffix_ );

	produces<double>(prefix_ + "leptonicWPt" + suffix_ );
	produces<double>(prefix_ + "leptonicWPx" + suffix_ );
	produces<double>(prefix_ + "leptonicWPy" + suffix_ );
	produces<double>(prefix_ + "leptonicWPz" + suffix_ );
	produces<double>(prefix_ + "leptonicWEnergy" + suffix_ );
	produces<double>(prefix_ + "hadronicWPt" + suffix_ );
	produces<double>(prefix_ + "hadronicWPx" + suffix_ );
	produces<double>(prefix_ + "hadronicWPy" + suffix_ );
	produces<double>(prefix_ + "hadronicWPz" + suffix_ );
	produces<double>(prefix_ + "hadronicWEnergy" + suffix_ );

	produces<double>(prefix_ + "hadronicdecayquarkPt" + suffix_ );
	produces<double>(prefix_ + "hadronicdecayquarkPx" + suffix_ );
	produces<double>(prefix_ + "hadronicdecayquarkPy" + suffix_ );
	produces<double>(prefix_ + "hadronicdecayquarkPz" + suffix_ );
	produces<double>(prefix_ + "hadronicdecayquarkEnergy" + suffix_ );	
	produces<double>(prefix_ + "hadronicdecayquarkbarPt" + suffix_ );
	produces<double>(prefix_ + "hadronicdecayquarkbarPx" + suffix_ );
	produces<double>(prefix_ + "hadronicdecayquarkbarPy" + suffix_ );
	produces<double>(prefix_ + "hadronicdecayquarkbarPz" + suffix_ );
	produces<double>(prefix_ + "hadronicdecayquarkbarEnergy" + suffix_ );

	produces<double>(prefix_ + "SingleLeptonPt" + suffix_ );
	produces<double>(prefix_ + "SingleLeptonPx" + suffix_ );
	produces<double>(prefix_ + "SingleLeptonPy" + suffix_ );
	produces<double>(prefix_ + "SingleLeptonPz" + suffix_ );
	produces<double>(prefix_ + "SingleLeptonEnergy" + suffix_ );
	produces<double>(prefix_ + "SingleNeutrinoPt" + suffix_ );
	produces<double>(prefix_ + "SingleNeutrinoPx" + suffix_ );
	produces<double>(prefix_ + "SingleNeutrinoPy" + suffix_ );
	produces<double>(prefix_ + "SingleNeutrinoPz" + suffix_ );
	produces<double>(prefix_ + "SingleNeutrinoEnergy" + suffix_ );

  produces<double>(prefix_ + "ZPt" + suffix_);
  produces<double>(prefix_ + "ZEta" + suffix_);
  produces<double>(prefix_ + "ZPhi" + suffix_);
  produces<double>(prefix_ + "ZPx" + suffix_);
  produces<double>(prefix_ + "ZPy" + suffix_);
  produces<double>(prefix_ + "ZPz" + suffix_);
  produces<double>(prefix_ + "ZEnergy" + suffix_);
  produces<unsigned int>(prefix_ + "ZDecay" + suffix_);
  produces<unsigned int>(prefix_ + "ZStatus" + suffix_);

  produces < std::vector<double> > (prefix_ + "ZDecayParticlesPt" + suffix_);
  produces < std::vector<double> > (prefix_ + "ZDecayParticlesEta" + suffix_);
  produces < std::vector<double> > (prefix_ + "ZDecayParticlesPhi" + suffix_);
  produces < std::vector<double> > (prefix_ + "ZDecayParticlesPx" + suffix_);
  produces < std::vector<double> > (prefix_ + "ZDecayParticlesPy" + suffix_);
  produces < std::vector<double> > (prefix_ + "ZDecayParticlesPz" + suffix_);
  produces < std::vector<double> > (prefix_ + "ZDecayParticlesEnergy" + suffix_);
  produces < std::vector<int> > (prefix_ + "ZDecayParticlesPdgId" + suffix_);
  produces < std::vector<double> > (prefix_ + "ZDecayParticlesCharge" + suffix_);
}

void BristolNTuple_GenEventInfo::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup) {
	// uncomment to produce list shown in data/lheweights.txt
//	edm::Handle < LHERunInfoProduct > run;
//	typedef std::vector<LHERunInfoProduct::Header>::const_iterator headers_const_iterator;
//
//	iRun.getByLabel("externalLHEProducer", run);
//	LHERunInfoProduct myLHERunInfoProduct = *(run.product());
//
//	for (headers_const_iterator iter = myLHERunInfoProduct.headers_begin(); iter != myLHERunInfoProduct.headers_end();
//			iter++) {
//		std::cout << iter->tag() << std::endl;
//		std::vector < std::string > lines = iter->lines();
//		for (unsigned int iLine = 0; iLine < lines.size(); iLine++) {
//			std::cout << lines.at(iLine);
//		}
//	}
}

void BristolNTuple_GenEventInfo::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {


	std::auto_ptr<unsigned int> processID(new unsigned int(0));
	std::auto_ptr<double> ptHat(new double(0));
	std::auto_ptr<double> PUWeight(new double());
	std::auto_ptr<double> generatorWeight(new double(0));
	std::auto_ptr<double> centralLHEWeight(new double(0));
	std::auto_ptr<std::vector<double> > systematicWeights(new std::vector<double>());
	std::auto_ptr<std::vector<int> > systematicWeightIDs(new std::vector<int>());

//	std::auto_ptr < std::vector<double> > pdfWeights(new std::vector<double>());
	std::auto_ptr < std::vector<int> > Number_interactions(new std::vector<int>());

	std::auto_ptr < std::vector<int> > NumberOfTrueInteractions(new std::vector<int>());
	std::auto_ptr < std::vector<int> > OriginBX(new std::vector<int>());
	std::auto_ptr<unsigned int> ttbarDecay(new unsigned int(0));

	std::auto_ptr<int> leptonicBGenJetIndex(new int(-1));
	std::auto_ptr<int> hadronicBGenJetIndex(new int(-1));
	std::auto_ptr<int> hadronicDecayQuarkBarGenJetIndex(new int(-1));
	std::auto_ptr<int> hadronicDecayQuarkGenJetIndex(new int(-1));


	std::auto_ptr<double> leptonicTopPt(new double(LARGE_NEGATIVE_INIT_VALUE));
	std::auto_ptr<double> leptonicTopPx(new double(0));
	std::auto_ptr<double> leptonicTopPy(new double(0));
	std::auto_ptr<double> leptonicTopPz(new double(0));
	std::auto_ptr<double> leptonicTopEnergy(new double(0));
	std::auto_ptr<double> hadronicTopPt(new double(LARGE_NEGATIVE_INIT_VALUE));
	std::auto_ptr<double> hadronicTopPx(new double(0));
	std::auto_ptr<double> hadronicTopPy(new double(0));
	std::auto_ptr<double> hadronicTopPz(new double(0));
	std::auto_ptr<double> hadronicTopEnergy(new double(0));

	std::auto_ptr<double> leptonicBPt(new double(LARGE_NEGATIVE_INIT_VALUE));
	std::auto_ptr<double> leptonicBPx(new double(0));
	std::auto_ptr<double> leptonicBPy(new double(0));
	std::auto_ptr<double> leptonicBPz(new double(0));
	std::auto_ptr<double> leptonicBEnergy(new double(0));
	std::auto_ptr<double> hadronicBPt(new double(LARGE_NEGATIVE_INIT_VALUE));
	std::auto_ptr<double> hadronicBPx(new double(0));
	std::auto_ptr<double> hadronicBPy(new double(0));
	std::auto_ptr<double> hadronicBPz(new double(0));
	std::auto_ptr<double> hadronicBEnergy(new double(0));

	std::auto_ptr<double> leptonicWPt(new double(LARGE_NEGATIVE_INIT_VALUE));
	std::auto_ptr<double> leptonicWPx(new double(0));
	std::auto_ptr<double> leptonicWPy(new double(0));
	std::auto_ptr<double> leptonicWPz(new double(0));
	std::auto_ptr<double> leptonicWEnergy(new double(0));
	std::auto_ptr<double> hadronicWPt(new double(LARGE_NEGATIVE_INIT_VALUE));
	std::auto_ptr<double> hadronicWPx(new double(0));
	std::auto_ptr<double> hadronicWPy(new double(0));
	std::auto_ptr<double> hadronicWPz(new double(0));
	std::auto_ptr<double> hadronicWEnergy(new double(0));

	std::auto_ptr<double> hadronicdecayquarkPt(new double(LARGE_NEGATIVE_INIT_VALUE));
	std::auto_ptr<double> hadronicdecayquarkPx(new double(0));
	std::auto_ptr<double> hadronicdecayquarkPy(new double(0));
	std::auto_ptr<double> hadronicdecayquarkPz(new double(0));
	std::auto_ptr<double> hadronicdecayquarkEnergy(new double(0));
	std::auto_ptr<double> hadronicdecayquarkbarPt(new double(LARGE_NEGATIVE_INIT_VALUE));
	std::auto_ptr<double> hadronicdecayquarkbarPx(new double(0));
	std::auto_ptr<double> hadronicdecayquarkbarPy(new double(0));
	std::auto_ptr<double> hadronicdecayquarkbarPz(new double(0));
	std::auto_ptr<double> hadronicdecayquarkbarEnergy(new double(0));

	std::auto_ptr<double> SingleLeptonPt(new double(LARGE_NEGATIVE_INIT_VALUE));
	std::auto_ptr<double> SingleLeptonPx(new double(0));
	std::auto_ptr<double> SingleLeptonPy(new double(0));
	std::auto_ptr<double> SingleLeptonPz(new double(0));
	std::auto_ptr<double> SingleLeptonEnergy(new double(0));
	std::auto_ptr<double> SingleNeutrinoPt(new double(LARGE_NEGATIVE_INIT_VALUE));
	std::auto_ptr<double> SingleNeutrinoPx(new double(0));
	std::auto_ptr<double> SingleNeutrinoPy(new double(0));
	std::auto_ptr<double> SingleNeutrinoPz(new double(0));
	std::auto_ptr<double> SingleNeutrinoEnergy(new double(0));

	//-----------------------------------------------------------------
	if (!iEvent.isRealData()) {
		// GenEventInfo Part
		edm::Handle < GenEventInfoProduct > genEvtInfoProduct;
		iEvent.getByToken(genEvtInfoInputTag, genEvtInfoProduct);



		if (genEvtInfoProduct.isValid()) {

			*processID.get() = genEvtInfoProduct->signalProcessID();
			*ptHat.get() = (genEvtInfoProduct->hasBinningValues() ? genEvtInfoProduct->binningValues()[0] : 0.);

			*generatorWeight.get() = genEvtInfoProduct->weight();

		} 

		// PileupSummary Part
		edm::Handle < std::vector<PileupSummaryInfo> > puInfo;
		iEvent.getByToken(pileupInfoSrc_, puInfo);

		if (puInfo.isValid()) {

			for (std::vector<PileupSummaryInfo>::const_iterator it = puInfo->begin(); it != puInfo->end(); ++it) {
				Number_interactions->push_back(it->getPU_NumInteractions());
				OriginBX->push_back(it->getBunchCrossing());
				NumberOfTrueInteractions->push_back(it->getTrueNumInteractions());
			}
		} 

		//identify ttbar decay mode
		if (isTTbarMC_) {

			if (ttbarDecayFlags_.size() != TTbarDecay::NumberOfDecayModes - 1) {
				edm::LogError("BristolNTuple_GenEventError")
						<< "Error! Not enough flags given to describe all decay modes." << "Expecting "
						<< TTbarDecay::NumberOfDecayModes - 1 << " got " << ttbarDecayFlags_.size();
			}
			unsigned short numberOfIdentifiedModes(0);
			for (unsigned short mode = 0; mode < ttbarDecayFlags_.size(); ++mode) {
				bool result = passesFilter(iEvent, ttbarDecayFlags_.at(mode));
				if (result) {
					++numberOfIdentifiedModes;
					*ttbarDecay.get() = mode + 1; //0 == not ttbar, first decay = 1, first filter = 0
				}
			}
			if (numberOfIdentifiedModes > 1) {
				std::cout << "PANIC" << std::endl;
				edm::LogError("BristolNTuple_GenEventError") << "Error! Found more than one compatible decay mode:"
						<< numberOfIdentifiedModes;
			}

			// Store weights from LHE
			// For pdf and generator systematics
			edm::Handle<LHEEventProduct> EvtHandle ;
			iEvent.getByToken( lheEventProductToken_ , EvtHandle ) ;

			*centralLHEWeight.get() = EvtHandle->originalXWGTUP();

			// int whichWeight = 1;
			// cout << "Number of weights : " << EvtHandle->weights().size() << endl;
			for ( unsigned int weightIndex = 0; weightIndex < EvtHandle->weights().size(); ++weightIndex ) {
				systematicWeights->push_back( EvtHandle->weights()[weightIndex].wgt );
				systematicWeightIDs->push_back( atoi(EvtHandle->weights()[weightIndex].id.c_str()) );
//				std::cout << weightIndex << " " << EvtHandle->weights()[weightIndex].id << " " << EvtHandle->weights()[weightIndex].wgt << std::endl;
			}

			// Only get top parton info if ttbar decay chain has been identified
			// t->Ws (~1% of top decays) are not recognised, and are ignored.
			if (numberOfIdentifiedModes==1 ) {

				// Get parton info
				edm::Handle < TtGenEvent > ttGenEvt;
				iEvent.getByToken(tt_gen_event_input_, ttGenEvt);

				if ( ttGenEvt->isSemiLeptonic() ) {

					const reco::GenParticle * leptonicTop = ttGenEvt->leptonicDecayTop();
					*leptonicTopPt.get() = leptonicTop->pt();
					*leptonicTopPx.get() = leptonicTop->px();
					*leptonicTopPy.get() = leptonicTop->py();
					*leptonicTopPz.get() = leptonicTop->pz();
					*leptonicTopEnergy.get() = leptonicTop->energy();
					const reco::GenParticle * hadronicTop = ttGenEvt->hadronicDecayTop();
					*hadronicTopPt.get() = hadronicTop->pt();
					*hadronicTopPx.get() = hadronicTop->px();
					*hadronicTopPy.get() = hadronicTop->py();
					*hadronicTopPz.get() = hadronicTop->pz();
					*hadronicTopEnergy.get() = hadronicTop->energy();

					const reco::GenParticle * leptonicDecayW = ttGenEvt->leptonicDecayW();
					*leptonicWPt.get() = leptonicDecayW->pt();
					*leptonicWPx.get() = leptonicDecayW->px();
					*leptonicWPy.get() = leptonicDecayW->py();
					*leptonicWPz.get() = leptonicDecayW->pz();
					*leptonicWEnergy.get() = leptonicDecayW->energy();
					const reco::GenParticle * hadronicDecayW = ttGenEvt->hadronicDecayW();
					*hadronicWPt.get() = hadronicDecayW->pt();
					*hadronicWPx.get() = hadronicDecayW->px();
					*hadronicWPy.get() = hadronicDecayW->py();
					*hadronicWPz.get() = hadronicDecayW->pz();
					*hadronicWEnergy.get() = hadronicDecayW->energy();

					const reco::GenParticle * SingleLepton = ttGenEvt->singleLepton();
					*SingleLeptonPt.get() = SingleLepton->pt();
					*SingleLeptonPx.get() = SingleLepton->px();
					*SingleLeptonPy.get() = SingleLepton->py();
					*SingleLeptonPx.get() = SingleLepton->pz();
					*SingleLeptonEnergy.get() = SingleLepton->energy();
					const reco::GenParticle * SingleNeutrino = ttGenEvt->singleNeutrino();
					*SingleNeutrinoPt.get() = SingleNeutrino->pt();
					*SingleNeutrinoPx.get() = SingleNeutrino->px();
					*SingleNeutrinoPy.get() = SingleNeutrino->py();
					*SingleNeutrinoPx.get() = SingleNeutrino->pz();
					*SingleNeutrinoEnergy.get() = SingleNeutrino->energy();

					// Get partons that should result in a gen jet
					const reco::GenParticle * leptonicDecayB = ttGenEvt->leptonicDecayB();
					*leptonicBPt.get() = leptonicDecayB->pt();
					*leptonicBPx.get() = leptonicDecayB->px();
					*leptonicBPy.get() = leptonicDecayB->py();
					*leptonicBPz.get() = leptonicDecayB->pz();
					*leptonicBEnergy.get() = leptonicDecayB->energy();
					const reco::GenParticle * hadronicDecayB = ttGenEvt->hadronicDecayB();
					*hadronicBPt.get() = hadronicDecayB->pt();
					*hadronicBPx.get() = hadronicDecayB->px();
					*hadronicBPy.get() = hadronicDecayB->py();
					*hadronicBPz.get() = hadronicDecayB->pz();
					*hadronicBEnergy.get() = ttGenEvt->hadronicDecayB()->energy();
	
					const reco::GenParticle * hadronicDecayQuark = ttGenEvt->hadronicDecayQuark();
					*hadronicdecayquarkPt.get() = hadronicDecayQuark->pt();
					*hadronicdecayquarkPx.get() = hadronicDecayQuark->px();
					*hadronicdecayquarkPy.get() = hadronicDecayQuark->py();
					*hadronicdecayquarkPz.get() = hadronicDecayQuark->pz();
					*hadronicdecayquarkEnergy.get() = hadronicDecayQuark->energy();
					const reco::GenParticle * hadronicDecayQuarkBar = ttGenEvt->hadronicDecayQuarkBar();
					*hadronicdecayquarkbarPt.get() = hadronicDecayQuarkBar->pt();
					*hadronicdecayquarkbarPx.get() = hadronicDecayQuarkBar->px();
					*hadronicdecayquarkbarPy.get() = hadronicDecayQuarkBar->py();
					*hadronicdecayquarkbarPz.get() = hadronicDecayQuarkBar->pz();
					*hadronicdecayquarkbarEnergy.get() = hadronicDecayQuarkBar->energy();

					// Put these in a vector to pass in to JetPartonMatching
					const vector< const reco::Candidate* > partonsToMatch = { hadronicDecayQuark, hadronicDecayQuarkBar, leptonicDecayB, hadronicDecayB };

					// Get gen jets
					edm::Handle < reco::GenJetCollection > genJets;
					iEvent.getByToken(genJetsInputTag_, genJets);

					// Get subset of gen jets that are stored in ntuple
					vector<reco::GenJet> genJetsInNtuple;
					for (reco::GenJetCollection::const_iterator it = genJets->begin(); it != genJets->end(); ++it) 
					{
						if (it->pt() < minGenJetPt_ || fabs(it->eta()) > maxGenJetAbsoluteEta_ )
							continue;

						genJetsInNtuple.push_back( *it );
					}

					// Jet -> parton matching from:
					// https://github.com/cms-sw/cmssw/blob/CMSSW_7_3_X/TopQuarkAnalysis/TopTools/interface/JetPartonMatching.h
					JetPartonMatching matching( partonsToMatch, genJetsInNtuple, 0, true, true, 0.3 );

					// Store indices of matched gen jets
					*hadronicDecayQuarkGenJetIndex = matching.getMatchForParton(0);
					*hadronicDecayQuarkBarGenJetIndex = matching.getMatchForParton(1);
					*leptonicBGenJetIndex = matching.getMatchForParton(2);
					*hadronicBGenJetIndex = matching.getMatchForParton(3);

				}

				addTTZContent(iEvent, iSetup);
			}
		}
	}

	//-----------------------------------------------------------------
	iEvent.put(processID, prefix_ + "ProcessID" + suffix_);
	iEvent.put(ptHat, prefix_ + "PtHat" + suffix_);
	iEvent.put(PUWeight, prefix_ + "PUWeight" + suffix_);
	iEvent.put(generatorWeight, prefix_ + "generatorWeight" + suffix_);
	iEvent.put(centralLHEWeight, prefix_ + "centralLHEWeight" + suffix_);
	iEvent.put(systematicWeights, prefix_ + "systematicWeights" + suffix_);
	iEvent.put(systematicWeightIDs, prefix_ + "systematicWeightIDs" + suffix_);
//	iEvent.put(pdfWeights, prefix_ + "PDFWeights" + suffix_);
	iEvent.put(Number_interactions, prefix_ + "PileUpInteractions" + suffix_);
	iEvent.put(NumberOfTrueInteractions, prefix_ + "NumberOfTrueInteractions" + suffix_);
	iEvent.put(OriginBX, prefix_ + "PileUpOriginBX" + suffix_);
	iEvent.put(ttbarDecay, prefix_ + "TtbarDecay" + suffix_);

	iEvent.put(leptonicTopPt, prefix_ + "leptonicTopPt" + suffix_);
	iEvent.put(leptonicTopPx, prefix_ + "leptonicTopPx" + suffix_);
	iEvent.put(leptonicTopPy, prefix_ + "leptonicTopPy" + suffix_);
	iEvent.put(leptonicTopPz, prefix_ + "leptonicTopPz" + suffix_);
	iEvent.put(leptonicTopEnergy, prefix_ + "leptonicTopEnergy" + suffix_);
	iEvent.put(hadronicTopPt, prefix_ + "hadronicTopPt" + suffix_);
	iEvent.put(hadronicTopPx, prefix_ + "hadronicTopPx" + suffix_);
	iEvent.put(hadronicTopPy, prefix_ + "hadronicTopPy" + suffix_);
	iEvent.put(hadronicTopPz, prefix_ + "hadronicTopPz" + suffix_);
	iEvent.put(hadronicTopEnergy, prefix_ + "hadronicTopEnergy" + suffix_);

	iEvent.put(leptonicBPt, prefix_ + "leptonicBPt" + suffix_);
	iEvent.put(leptonicBPx, prefix_ + "leptonicBPx" + suffix_);
	iEvent.put(leptonicBPy, prefix_ + "leptonicBPy" + suffix_);
	iEvent.put(leptonicBPz, prefix_ + "leptonicBPz" + suffix_);
	iEvent.put(leptonicBEnergy, prefix_ + "leptonicBEnergy" + suffix_);
	iEvent.put(hadronicBPt, prefix_ + "hadronicBPt" + suffix_);
	iEvent.put(hadronicBPx, prefix_ + "hadronicBPx" + suffix_);
	iEvent.put(hadronicBPy, prefix_ + "hadronicBPy" + suffix_);
	iEvent.put(hadronicBPz, prefix_ + "hadronicBPz" + suffix_);
	iEvent.put(hadronicBEnergy, prefix_ + "hadronicBEnergy" + suffix_);

	iEvent.put(leptonicWPt, prefix_ + "leptonicWPt" + suffix_);
	iEvent.put(leptonicWPx, prefix_ + "leptonicWPx" + suffix_);
	iEvent.put(leptonicWPy, prefix_ + "leptonicWPy" + suffix_);
	iEvent.put(leptonicWPz, prefix_ + "leptonicWPz" + suffix_);
	iEvent.put(leptonicWEnergy, prefix_ + "leptonicWEnergy" + suffix_);
	iEvent.put(hadronicWPt, prefix_ + "hadronicWPt" + suffix_);
	iEvent.put(hadronicWPx, prefix_ + "hadronicWPx" + suffix_);
	iEvent.put(hadronicWPy, prefix_ + "hadronicWPy" + suffix_);
	iEvent.put(hadronicWPz, prefix_ + "hadronicWPz" + suffix_);
	iEvent.put(hadronicWEnergy, prefix_ + "hadronicWEnergy" + suffix_);

	iEvent.put(hadronicdecayquarkPt, prefix_ + "hadronicdecayquarkPt" + suffix_);
	iEvent.put(hadronicdecayquarkPx, prefix_ + "hadronicdecayquarkPx" + suffix_);
	iEvent.put(hadronicdecayquarkPy, prefix_ + "hadronicdecayquarkPy" + suffix_);
	iEvent.put(hadronicdecayquarkPz, prefix_ + "hadronicdecayquarkPz" + suffix_);
	iEvent.put(hadronicdecayquarkEnergy, prefix_ + "hadronicdecayquarkEnergy" + suffix_);
	iEvent.put(hadronicdecayquarkbarPt, prefix_ + "hadronicdecayquarkbarPt" + suffix_);
	iEvent.put(hadronicdecayquarkbarPx, prefix_ + "hadronicdecayquarkbarPx" + suffix_);
	iEvent.put(hadronicdecayquarkbarPy, prefix_ + "hadronicdecayquarkbarPy" + suffix_);
	iEvent.put(hadronicdecayquarkbarPz, prefix_ + "hadronicdecayquarkbarPz" + suffix_);
	iEvent.put(hadronicdecayquarkbarEnergy, prefix_ + "hadronicdecayquarkbarEnergy" + suffix_);

	iEvent.put(SingleLeptonPt, prefix_ + "SingleLeptonPt" + suffix_);
	iEvent.put(SingleLeptonPx, prefix_ + "SingleLeptonPx" + suffix_);
	iEvent.put(SingleLeptonPy, prefix_ + "SingleLeptonPy" + suffix_);
	iEvent.put(SingleLeptonPz, prefix_ + "SingleLeptonPz" + suffix_);
	iEvent.put(SingleLeptonEnergy, prefix_ + "SingleLeptonEnergy" + suffix_);
	iEvent.put(SingleNeutrinoPt, prefix_ + "SingleNeutrinoPt" + suffix_);
	iEvent.put(SingleNeutrinoPx, prefix_ + "SingleNeutrinoPx" + suffix_);
	iEvent.put(SingleNeutrinoPy, prefix_ + "SingleNeutrinoPy" + suffix_);
	iEvent.put(SingleNeutrinoPz, prefix_ + "SingleNeutrinoPz" + suffix_);
	iEvent.put(SingleNeutrinoEnergy, prefix_ + "SingleNeutrinoEnergy" + suffix_);

	iEvent.put(leptonicBGenJetIndex, prefix_ + "leptonicBGenJetIndex" + suffix_);
	iEvent.put(hadronicBGenJetIndex, prefix_ + "hadronicBGenJetIndex" + suffix_);
	iEvent.put(hadronicDecayQuarkBarGenJetIndex, prefix_ + "hadronicDecayQuarkBarGenJetIndex" + suffix_);
	iEvent.put(hadronicDecayQuarkGenJetIndex, prefix_ + "hadronicDecayQuarkGenJetIndex" + suffix_);


}

bool BristolNTuple_GenEventInfo::isAncestor(const reco::Candidate* ancestor, const reco::Candidate * particle) const
{
  //particle is already the ancestor
  if (ancestor == particle)
    return true;

  //otherwise loop on mothers, if any and return true if the ancestor is found
  for (size_t i = 0; i < particle->numberOfMothers(); i++) {
    if (isAncestor(ancestor, particle->mother(i)))
      return true;
  }
  //if we did not return yet, then particle and ancestor are not relatives
  return false;
}

void BristolNTuple_GenEventInfo::addTTZContent(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  using namespace reco;
  using namespace pat;

  std::auto_ptr<unsigned int> zDecay(new unsigned int(0));
  std::auto_ptr<unsigned int> zStatus(new unsigned int(0));

  std::auto_ptr<double> zPt(new double(LARGE_NEGATIVE_INIT_VALUE));
  std::auto_ptr<double> zEta(new double(LARGE_NEGATIVE_INIT_VALUE));
  std::auto_ptr<double> zPhi(new double(LARGE_NEGATIVE_INIT_VALUE));
  std::auto_ptr<double> zPx(new double());
  std::auto_ptr<double> zPy(new double());
  std::auto_ptr<double> zPz(new double());
  std::auto_ptr<double> zEnergy(new double());
  // particles the Z boson decays into
  std::auto_ptr < std::vector<double> > decayPt(new std::vector<double>());
  std::auto_ptr < std::vector<double> > decayEta(new std::vector<double>());
  std::auto_ptr < std::vector<double> > decayPhi(new std::vector<double>());
  std::auto_ptr < std::vector<double> > decayPx(new std::vector<double>());
  std::auto_ptr < std::vector<double> > decayPy(new std::vector<double>());
  std::auto_ptr < std::vector<double> > decayPz(new std::vector<double>());
  std::auto_ptr < std::vector<double> > decayEnergy(new std::vector<double>());
  std::auto_ptr < std::vector<int> > decayPdgId(new std::vector<int>());
  std::auto_ptr < std::vector<double> > decayCharge(new std::vector<double>());

  // Pruned particles are the one containing "important" stuff
  Handle < edm::View<reco::GenParticle> > pruned;
  iEvent.getByToken(prunedGenToken_, pruned);

  // Packed particles are all the status 1, so usable to remake jets
  // The navigation from status 1 to pruned is possible (the other direction should be made by hand)
  Handle < edm::View<pat::PackedGenParticle> > packed;
  iEvent.getByToken(packedGenToken_, packed);

  for (auto particle = pruned->begin(); particle != pruned->end(); ++particle) {
    if (std::abs(particle->pdgId()) == 23) {
      auto decayParticles = getZDecayParticles(&(*particle), packed);
      *zDecay = getZDecay(decayParticles);
      *zStatus = particle->status();

      if (*zDecay == ZDecay::NotInterestingZDecay)
        continue;

      *zPt.get() = particle->pt();
      *zEta.get() = particle->eta();
      *zPhi.get() = particle->phi();
      *zPx.get() = particle->px();
      *zPy.get() = particle->py();
      *zPz.get() = particle->pz();
      *zEnergy.get() = particle->energy();

      for (auto decayParticle : decayParticles) {
        decayPt->push_back(decayParticle->pt());
        decayEta->push_back(decayParticle->eta());
        decayPhi->push_back(decayParticle->phi());
        decayPx->push_back(decayParticle->px());
        decayPy->push_back(decayParticle->py());
        decayPz->push_back(decayParticle->pz());
        decayEnergy->push_back(decayParticle->energy());
        decayPdgId->push_back(decayParticle->pdgId());
        decayCharge->push_back(decayParticle->charge());
      }

      break;
    }
  }

  iEvent.put(zPt, prefix_ + "ZPt" + suffix_);
  iEvent.put(zEta, prefix_ + "ZEta" + suffix_);
  iEvent.put(zPhi, prefix_ + "ZPhi" + suffix_);
  iEvent.put(zPx, prefix_ + "ZPx" + suffix_);
  iEvent.put(zPy, prefix_ + "ZPy" + suffix_);
  iEvent.put(zPz, prefix_ + "ZPz" + suffix_);
  iEvent.put(zEnergy, prefix_ + "ZEnergy" + suffix_);
  iEvent.put(zDecay, prefix_ + "ZDecay" + suffix_);
  iEvent.put(zStatus, prefix_ + "ZStatus" + suffix_);

  iEvent.put(decayPt, prefix_ + "ZDecayParticlesPt" + suffix_);
  iEvent.put(decayEta, prefix_ + "ZDecayParticlesEta" + suffix_);
  iEvent.put(decayPhi, prefix_ + "ZDecayParticlesPhi" + suffix_);
  iEvent.put(decayPx, prefix_ + "ZDecayParticlesPx" + suffix_);
  iEvent.put(decayPy, prefix_ + "ZDecayParticlesPy" + suffix_);
  iEvent.put(decayPz, prefix_ + "ZDecayParticlesPz" + suffix_);
  iEvent.put(decayEnergy, prefix_ + "ZDecayParticlesEnergy" + suffix_);
  iEvent.put(decayPdgId, prefix_ + "ZDecayParticlesPdgId" + suffix_);
  iEvent.put(decayCharge, prefix_ + "ZDecayParticlesCharge" + suffix_);

}

std::vector<const pat::PackedGenParticle*> BristolNTuple_GenEventInfo::getZDecayParticles(
    const reco::Candidate* zBoson, const edm::Handle<edm::View<pat::PackedGenParticle> >& packed) const
{
  std::vector<const pat::PackedGenParticle*> decayParticles;
  /* look for 2 leptons
   * pdgIds:
   *    11 -> electron
   *    12 -> nu_e
   *    13 -> mu
   *    14 -> nu_mu
   *    15 -> tau
   *    16 -> tau_nu
   */
  std::vector<unsigned int> pidsOfInterest = { 11, 12, 13, 14, 15, 16 };
  for (auto particle = packed->begin(); particle != packed->end(); ++particle) {
    auto motherInPrunedCollection = particle->mother(0);

    if (motherInPrunedCollection != nullptr && isAncestor(zBoson, motherInPrunedCollection)) {
      auto isInteresting = std::find(pidsOfInterest.begin(), pidsOfInterest.end(), std::abs(particle->pdgId()))
          != pidsOfInterest.end();
      if (isInteresting) {
        decayParticles.push_back(&(*particle));
      }
    }
  }
  return decayParticles;
}

ZDecay::value BristolNTuple_GenEventInfo::getZDecay(
    const std::vector<const pat::PackedGenParticle*>& decayParticles) const
{
  ZDecay::value zDecay(ZDecay::NotInterestingZDecay);
  for (auto particle : decayParticles) {
    unsigned int pdgId = std::abs(particle->pdgId());
    switch (pdgId) {
    case 11:
      zDecay = ZDecay::ZToEE;
      break;
    case 12:
      zDecay = ZDecay::ZTo2NuE;
      break;
    case 13:
      zDecay = ZDecay::ZToMuMu;
      break;
    case 14:
      zDecay = ZDecay::ZTo2NuMu;
      break;
    case 15:
      zDecay = ZDecay::ZToTauTau;
      break;
    case 16:
      zDecay = ZDecay::ZTo2NuTau;
      break;
    default:
      zDecay = ZDecay::NotInterestingZDecay;
      break;
    }
  }
  return zDecay;
}

#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenEventInfo.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "boost/filesystem.hpp"

#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"

#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"


#include <iostream>

using namespace std;

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
		suffix_(iConfig.getParameter < std::string > ("Suffix")) {

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


	std::auto_ptr<unsigned int> processID(new unsigned int());
	std::auto_ptr<double> ptHat(new double());
	std::auto_ptr<double> PUWeight(new double());
	std::auto_ptr<double> generatorWeight(new double());
	std::auto_ptr<double> centralLHEWeight(new double());
	std::auto_ptr<std::vector<double> > systematicWeights(new std::vector<double>());
	std::auto_ptr<std::vector<int> > systematicWeightIDs(new std::vector<int>());

//	std::auto_ptr < std::vector<double> > pdfWeights(new std::vector<double>());
	std::auto_ptr < std::vector<int> > Number_interactions(new std::vector<int>());

	std::auto_ptr < std::vector<int> > NumberOfTrueInteractions(new std::vector<int>());
	std::auto_ptr < std::vector<int> > OriginBX(new std::vector<int>());
	std::auto_ptr<unsigned int> ttbarDecay(new unsigned int());

	std::auto_ptr<int> leptonicBGenJetIndex(new int());
	std::auto_ptr<int> hadronicBGenJetIndex(new int());
	std::auto_ptr<int> hadronicDecayQuarkBarGenJetIndex(new int());
	std::auto_ptr<int> hadronicDecayQuarkGenJetIndex(new int());


	std::auto_ptr<double> leptonicTopPt(new double());
	std::auto_ptr<double> leptonicTopPx(new double());
	std::auto_ptr<double> leptonicTopPy(new double());
	std::auto_ptr<double> leptonicTopPz(new double());
	std::auto_ptr<double> leptonicTopEnergy(new double());
	std::auto_ptr<double> hadronicTopPt(new double());
	std::auto_ptr<double> hadronicTopPx(new double());
	std::auto_ptr<double> hadronicTopPy(new double());
	std::auto_ptr<double> hadronicTopPz(new double());
	std::auto_ptr<double> hadronicTopEnergy(new double());

	std::auto_ptr<double> leptonicBPt(new double());
	std::auto_ptr<double> leptonicBPx(new double());
	std::auto_ptr<double> leptonicBPy(new double());
	std::auto_ptr<double> leptonicBPz(new double());
	std::auto_ptr<double> leptonicBEnergy(new double());
	std::auto_ptr<double> hadronicBPt(new double());
	std::auto_ptr<double> hadronicBPx(new double());
	std::auto_ptr<double> hadronicBPy(new double());
	std::auto_ptr<double> hadronicBPz(new double());
	std::auto_ptr<double> hadronicBEnergy(new double());

	std::auto_ptr<double> leptonicWPt(new double());
	std::auto_ptr<double> leptonicWPx(new double());
	std::auto_ptr<double> leptonicWPy(new double());
	std::auto_ptr<double> leptonicWPz(new double());
	std::auto_ptr<double> leptonicWEnergy(new double());
	std::auto_ptr<double> hadronicWPt(new double());
	std::auto_ptr<double> hadronicWPx(new double());
	std::auto_ptr<double> hadronicWPy(new double());
	std::auto_ptr<double> hadronicWPz(new double());
	std::auto_ptr<double> hadronicWEnergy(new double());

	std::auto_ptr<double> hadronicdecayquarkPt(new double());
	std::auto_ptr<double> hadronicdecayquarkPx(new double());
	std::auto_ptr<double> hadronicdecayquarkPy(new double());
	std::auto_ptr<double> hadronicdecayquarkPz(new double());
	std::auto_ptr<double> hadronicdecayquarkEnergy(new double());
	std::auto_ptr<double> hadronicdecayquarkbarPt(new double());
	std::auto_ptr<double> hadronicdecayquarkbarPx(new double());
	std::auto_ptr<double> hadronicdecayquarkbarPy(new double());
	std::auto_ptr<double> hadronicdecayquarkbarPz(new double());
	std::auto_ptr<double> hadronicdecayquarkbarEnergy(new double());

	std::auto_ptr<double> SingleLeptonPt(new double());
	std::auto_ptr<double> SingleLeptonPx(new double());
	std::auto_ptr<double> SingleLeptonPy(new double());
	std::auto_ptr<double> SingleLeptonPz(new double());
	std::auto_ptr<double> SingleLeptonEnergy(new double());
	std::auto_ptr<double> SingleNeutrinoPt(new double());
	std::auto_ptr<double> SingleNeutrinoPx(new double());
	std::auto_ptr<double> SingleNeutrinoPy(new double());
	std::auto_ptr<double> SingleNeutrinoPz(new double());
	std::auto_ptr<double> SingleNeutrinoEnergy(new double());


	*processID.get() = 0;
	*ptHat.get() = 0.;
	*PUWeight.get() = 0.;
	*generatorWeight.get() = 0.;
	*centralLHEWeight.get() = 0;
	*ttbarDecay.get() = 0;

	*leptonicTopPt.get() = 0;
	*leptonicTopPx.get() = 0;
	*leptonicTopPy.get() = 0;
	*leptonicTopPz.get() = 0;
	*leptonicTopEnergy.get() = 0;
	*hadronicTopPt.get() = 0;
	*hadronicTopPx.get() = 0;
	*hadronicTopPy.get() = 0;
	*hadronicTopPz.get() = 0;
	*hadronicTopEnergy.get() = 0;

	*leptonicBPt.get() = 0;
	*leptonicBPx.get() = 0;
	*leptonicBPy.get() = 0;
	*leptonicBPz.get() = 0;
	*leptonicBEnergy.get() = 0;
	*hadronicBPt.get() = 0;
	*hadronicBPx.get() = 0;
	*hadronicBPy.get() = 0;
	*hadronicBPz.get() = 0;
	*hadronicBEnergy.get() = 0;

	*leptonicWPt.get() = 0;
	*leptonicWPx.get() = 0;
	*leptonicWPy.get() = 0;
	*leptonicWPz.get() = 0;
	*leptonicWEnergy.get() = 0;
	*hadronicWPt.get() = 0;
	*hadronicWPx.get() = 0;
	*hadronicWPy.get() = 0;
	*hadronicWPz.get() = 0;
	*hadronicWEnergy.get() = 0;

	*hadronicdecayquarkPt.get() = 0;
	*hadronicdecayquarkPx.get() = 0;
	*hadronicdecayquarkPy.get() = 0;
	*hadronicdecayquarkPz.get() = 0;
	*hadronicdecayquarkEnergy.get() = 0;
	*hadronicdecayquarkbarPt.get() = 0;
	*hadronicdecayquarkbarPx.get() = 0;
	*hadronicdecayquarkbarPy.get() = 0;
	*hadronicdecayquarkbarPz.get() = 0;
	*hadronicdecayquarkbarEnergy.get() = 0;

	*SingleLeptonPt.get() = 0;
	*SingleLeptonPx.get() = 0;
	*SingleLeptonPy.get() = 0;
	*SingleLeptonPz.get() = 0;
	*SingleLeptonEnergy.get() = 0;
	*SingleNeutrinoPt.get() = 0;
	*SingleNeutrinoPx.get() = 0;
	*SingleNeutrinoPy.get() = 0;
	*SingleNeutrinoPz.get() = 0;
	*SingleNeutrinoEnergy.get() = 0;

	*leptonicBGenJetIndex.get() = -1;
	*hadronicBGenJetIndex.get() = -1;
	*hadronicDecayQuarkGenJetIndex.get() = -1;
	*hadronicDecayQuarkBarGenJetIndex.get() = -1;


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

		// // PU Weights Part
		// edm::Handle<double> puWeightsHandle;
		// iEvent.getByLabel(puWeightsInputTag_, puWeightsHandle);

		// if (puWeightsHandle.isValid()) {
		// 	edm::LogInfo("BristolNTuple_GenEventInfoInfo") << "Successfully obtained " << puWeightsInputTag_;

		// 	*PUWeight.get() = *puWeightsHandle;

		// }

		// // PDF Weights Part
		// if (storePDFWeights_) {
		// 	edm::Handle < std::vector<double> > pdfWeightsHandle;
		// 	iEvent.getByLabel(pdfWeightsInputTag_, pdfWeightsHandle);

		// 	if (pdfWeightsHandle.isValid()) {
		// 		edm::LogInfo("BristolNTuple_GenEventInfoInfo") << "Successfully obtained " << pdfWeightsInputTag_;

		// 		*pdfWeights.get() = *pdfWeightsHandle;

		// 	}
		// }
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

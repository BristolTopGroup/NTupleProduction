#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenEventInfo.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "boost/filesystem.hpp"

BristolNTuple_GenEventInfo::BristolNTuple_GenEventInfo(const edm::ParameterSet& iConfig) : //
		genEvtInfoInputTag(iConfig.getParameter < edm::InputTag > ("GenEventInfoInputTag")), //
		puWeightsInputTag_(iConfig.getParameter < edm::InputTag > ("PUWeightsInputTag")), //
		storePDFWeights_(iConfig.getParameter<bool>("StorePDFWeights")), //
		pdfWeightsInputTag_(iConfig.getParameter < edm::InputTag > ("PDFWeightsInputTag")), //
		pileupInfoSrc_(iConfig.getParameter < edm::InputTag > ("pileupInfo")), //
		prefix_(iConfig.getParameter < std::string > ("Prefix")), //
		suffix_(iConfig.getParameter < std::string > ("Suffix")) {
	produces<unsigned int>(prefix_ + "ProcessID" + suffix_);
	produces<double>(prefix_ + "PtHat" + suffix_);
	produces<double>(prefix_ + "PUWeight" + suffix_);
	produces < std::vector<double> > (prefix_ + "PDFWeights" + suffix_);
	produces < std::vector<int> > (prefix_ + "PileUpInteractions" + suffix_);
	produces < std::vector<int> > (prefix_ + "NumberOfTrueInteractions" + suffix_);
	produces < std::vector<int> > (prefix_ + "PileUpOriginBX" + suffix_);
	produces<unsigned int>(prefix_ + "FlavourHistory" + suffix_);
}

void BristolNTuple_GenEventInfo::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	std::auto_ptr<unsigned int> processID(new unsigned int());
	std::auto_ptr<double> ptHat(new double());
	std::auto_ptr<double> PUWeight(new double());
	std::auto_ptr < std::vector<double> > pdfWeights(new std::vector<double>());
	std::auto_ptr < std::vector<int> > Number_interactions(new std::vector<int>());

	std::auto_ptr < std::vector<int> > NumberOfTrueInteractions(new std::vector<int>());
	std::auto_ptr < std::vector<int> > OriginBX(new std::vector<int>());
	std::auto_ptr<unsigned int> flavourHistory(new unsigned int());

	*processID.get() = 0;
	*ptHat.get() = 0.;
	*PUWeight.get() = 0.;
	*flavourHistory.get() = 0;

	//-----------------------------------------------------------------
	if (!iEvent.isRealData()) {
		// GenEventInfo Part
		edm::Handle < GenEventInfoProduct > genEvtInfoProduct;
		iEvent.getByLabel(genEvtInfoInputTag, genEvtInfoProduct);

		edm::Handle<unsigned int> historyProduct;
		iEvent.getByLabel("flavorHistoryFilter", historyProduct);

		*flavourHistory.get() = *historyProduct;

		if (genEvtInfoProduct.isValid()) {
			edm::LogInfo("BristolNTuple_GenEventInfoInfo") << "Successfully obtained " << genEvtInfoInputTag;

			*processID.get() = genEvtInfoProduct->signalProcessID();
			*ptHat.get() = (genEvtInfoProduct->hasBinningValues() ? genEvtInfoProduct->binningValues()[0] : 0.);

		} else {
			edm::LogError("BristolNTuple_GenEventInfoError") << "Error! Can't get the product " << genEvtInfoInputTag;
		}

		// PU Weights Part
		edm::Handle<double> puWeightsHandle;
		iEvent.getByLabel(puWeightsInputTag_, puWeightsHandle);

		if (puWeightsHandle.isValid()) {
			edm::LogInfo("BristolNTuple_GenEventInfoInfo") << "Successfully obtained " << puWeightsInputTag_;

			*PUWeight.get() = *puWeightsHandle;

		} else {
			edm::LogError("BristolNTuple_GenEventInfoError") << "Error! Can't get the product " << puWeightsInputTag_;
		}

		// PDF Weights Part
		if (storePDFWeights_) {
			edm::Handle < std::vector<double> > pdfWeightsHandle;
			iEvent.getByLabel(pdfWeightsInputTag_, pdfWeightsHandle);

			if (pdfWeightsHandle.isValid()) {
				edm::LogInfo("BristolNTuple_GenEventInfoInfo") << "Successfully obtained " << pdfWeightsInputTag_;

				*pdfWeights.get() = *pdfWeightsHandle;

			} else {
				edm::LogError("BristolNTuple_GenEventInfoError") << "Error! Can't get the product "
						<< pdfWeightsInputTag_;
			}
		}
		// PileupSummary Part
		edm::Handle < std::vector<PileupSummaryInfo> > puInfo;
		iEvent.getByLabel(pileupInfoSrc_, puInfo);

		if (puInfo.isValid()) {

			for (std::vector<PileupSummaryInfo>::const_iterator it = puInfo->begin(); it != puInfo->end(); ++it) {
				Number_interactions->push_back(it->getPU_NumInteractions());
				OriginBX->push_back(it->getBunchCrossing());
				NumberOfTrueInteractions->push_back(it->getTrueNumInteractions());
			}
		} else {
			edm::LogError("BristolNTuple_PileUpError") << "Error! Can't get the product " << pileupInfoSrc_;
		}
	}

	//-----------------------------------------------------------------
	iEvent.put(processID, prefix_ + "ProcessID" + suffix_);
	iEvent.put(ptHat, prefix_ + "PtHat" + suffix_);
	iEvent.put(PUWeight, prefix_ + "PUWeight" + suffix_);
	iEvent.put(pdfWeights, prefix_ + "PDFWeights" + suffix_);
	iEvent.put(Number_interactions, prefix_ + "PileUpInteractions" + suffix_);
	iEvent.put(NumberOfTrueInteractions, prefix_ + "NumberOfTrueInteractions" + suffix_);
	iEvent.put(OriginBX, prefix_ + "PileUpOriginBX" + suffix_);
	iEvent.put(flavourHistory, prefix_ + "FlavourHistory" + suffix_);

}

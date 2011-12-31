#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenEventInfo.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "boost/filesystem.hpp"

BristolNTuple_GenEventInfo::BristolNTuple_GenEventInfo(const edm::ParameterSet& iConfig) ://
	genEvtInfoInputTag(iConfig.getParameter<edm::InputTag> ("GenEventInfoInputTag")), //
			storePDFWeights_(iConfig.getParameter<bool> ("StorePDFWeights")), //
			isFall11MC_(iConfig.getParameter<bool> ("isFall11MC")),//
			pdfWeightsInputTag_(iConfig.getParameter<edm::InputTag> ("PDFWeightsInputTag")), //
			pileupInfoSrc_(iConfig.getParameter<edm::InputTag> ("pileupInfo")), //
			prefix_(iConfig.getParameter<std::string> ("Prefix")), //
			suffix_(iConfig.getParameter<std::string> ("Suffix")), //
			dataPileUpFile_(iConfig.getParameter<std::string> ("dataPileUpFile")), //
			lumiWeightOneX_(), //
			lumiWeight3X_(), //
			lumiWeight3D_(),//
			PShiftUp_(iConfig.getParameter<double> ("PossionShiftUp")), //
			PShiftDown_(iConfig.getParameter<double> ("PossionShiftDown"))//
{
	produces<unsigned int> (prefix_ + "ProcessID" + suffix_);
	produces<double> (prefix_ + "PtHat" + suffix_);
	produces<double> (prefix_ + "PUWeightInTimeOnly" + suffix_);
	produces<double> (prefix_ + "PUWeight3BX" + suffix_);
	produces<double> (prefix_ + "PUWeight3D" + suffix_);
	produces<double> (prefix_ + "PUWeightShiftUp" + suffix_);
	produces<double> (prefix_ + "PUWeightShiftDown" + suffix_);
	produces<std::vector<double> > (prefix_ + "PDFWeights" + suffix_);
	produces<std::vector<int> > (prefix_ + "PileUpInteractions" + suffix_);
	if (isFall11MC_)
		produces<std::vector<int> > (prefix_ + "NumberOfTrueInteractions" + suffix_);
	produces<std::vector<int> > (prefix_ + "PileUpOriginBX" + suffix_);
	produces<unsigned int> (prefix_ + "FlavourHistory" + suffix_);

	initLumiWeights();
}

void BristolNTuple_GenEventInfo::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	std::auto_ptr<unsigned int> processID(new unsigned int());
	std::auto_ptr<double> ptHat(new double());
	std::auto_ptr<double> PUWeightInTimeOnly(new double());
	std::auto_ptr<double> PUWeight3BX(new double());
	std::auto_ptr<double> PUWeight3D(new double());
	std::auto_ptr<double> PUWeightShiftUp(new double());
	std::auto_ptr<double> PUWeightShiftDown(new double());
	std::auto_ptr<std::vector<double> > pdfWeights(new std::vector<double>());
	std::auto_ptr<std::vector<int> > Number_interactions(new std::vector<int>());

	std::auto_ptr<std::vector<int> > NumberOfTrueInteractions(new std::vector<int>());
	std::auto_ptr<std::vector<int> > OriginBX(new std::vector<int>());
	std::auto_ptr<unsigned int> flavourHistory(new unsigned int());

	*processID.get() = 0;
	*ptHat.get() = 0.;
	*PUWeightInTimeOnly.get() = 0.;
	*PUWeight3BX.get() = 0.;
	*PUWeight3D.get() = 0.;
	*PUWeightShiftUp.get() = 0.;
	*PUWeightShiftDown.get() = 0.;

	*flavourHistory.get() = 0;

	//-----------------------------------------------------------------
	if (!iEvent.isRealData()) {
		// GenEventInfo Part
		edm::Handle<GenEventInfoProduct> genEvtInfoProduct;
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
		// PDF Weights Part
		if (storePDFWeights_) {
			edm::Handle<std::vector<double> > pdfWeightsHandle;
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
		edm::Handle<std::vector<PileupSummaryInfo> > puInfo;
		iEvent.getByLabel(pileupInfoSrc_, puInfo);
		int npv0 = 0;
		float sum_nvtx = 0;

		if (puInfo.isValid()) {

			for (std::vector<PileupSummaryInfo>::const_iterator it = puInfo->begin(); it != puInfo->end(); ++it) {
				Number_interactions->push_back(it->getPU_NumInteractions());
				OriginBX->push_back(it->getBunchCrossing());
				sum_nvtx += float(it->getPU_NumInteractions());
				if (isFall11MC_) {
					NumberOfTrueInteractions->push_back(it->getTrueNumInteractions());
				}
				if (it->getBunchCrossing() == 0) {
					npv0 = it->getPU_NumInteractions();
					if (isFall11MC_)
						npv0 = it->getTrueNumInteractions();
				}

			}
		} else {
			edm::LogError("BristolNTuple_PileUpError") << "Error! Can't get the product " << pileupInfoSrc_;
		}
		float ave_nvtx = sum_nvtx / 3.;
		edm::EventBase* iEventB = dynamic_cast<edm::EventBase*> (&iEvent);
		*PUWeightInTimeOnly.get() = lumiWeightOneX_.weight(*iEventB);
		*PUWeight3BX.get() = lumiWeight3X_.weight3BX(ave_nvtx);
		*PUWeight3D.get() = lumiWeight3D_.weight3D((*iEventB));
		*PUWeightShiftUp.get() = PShiftUp_.ShiftWeight(npv0);
		*PUWeightShiftDown.get() = PShiftDown_.ShiftWeight(npv0);
	}

	//-----------------------------------------------------------------
	iEvent.put(processID, prefix_ + "ProcessID" + suffix_);
	iEvent.put(ptHat, prefix_ + "PtHat" + suffix_);
	iEvent.put(PUWeightInTimeOnly, prefix_ + "PUWeightInTimeOnly" + suffix_);
	iEvent.put(PUWeight3BX, prefix_ + "PUWeight3BX" + suffix_);
	iEvent.put(PUWeight3D, prefix_ + "PUWeight3D" + suffix_);
	iEvent.put(PUWeightShiftUp, prefix_ + "PUWeightShiftUp" + suffix_);
	iEvent.put(PUWeightShiftDown, prefix_ + "PUWeightShiftDown" + suffix_);
	iEvent.put(pdfWeights, prefix_ + "PDFWeights" + suffix_);
	iEvent.put(Number_interactions, prefix_ + "PileUpInteractions" + suffix_);
	if (isFall11MC_)
		iEvent.put(NumberOfTrueInteractions, prefix_ + "NumberOfTrueInteractions" + suffix_);
	iEvent.put(OriginBX, prefix_ + "PileUpOriginBX" + suffix_);
	iEvent.put(flavourHistory, prefix_ + "FlavourHistory" + suffix_);

}

void BristolNTuple_GenEventInfo::initLumiWeights() {
	//check if data pile up input file exists
	if (!boost::filesystem::exists(dataPileUpFile_)) {
		edm::LogError("BristolNTuple_PileUpError") << "Error! Could not find PU data file " << dataPileUpFile_;
	}

	//assign MC PU distribution vectors
	std::vector<float> dataDistr, dataDistr1BX, mcDistr, mcDistr1BX;
	if (isFall11MC_) {
		for (unsigned int i = 0; i < Fall2011.size(); ++i)
			mcDistr.push_back(Fall2011.at(i));

		for (unsigned int i = 0; i < Fall2011_InTime.size(); ++i)
			mcDistr1BX.push_back(Fall2011_InTime.at(i));

	} else {
		for (unsigned int i = 0; i < PoissonIntDist.size(); ++i)
			mcDistr.push_back(PoissonIntDist.at(i));

		for (unsigned int i = 0; i < PoissonOneXDist.size(); ++i)
			mcDistr1BX.push_back(PoissonOneXDist.at(i));
	}

	//get data histogram
	boost::scoped_ptr<TFile> file(new TFile(dataPileUpFile_.c_str()));
	boost::scoped_ptr<TH1D> dataInput((TH1D*) file->Get("pileup")->Clone());

	for (unsigned int i = 0; i < mcDistr.size(); ++i)
		//find bin-center corresponding to i number of vertices
		dataDistr.push_back(dataInput->GetBinContent(dataInput->GetXaxis()->FindBin(i)));

	for (unsigned int i = 0; i < mcDistr1BX.size(); ++i)
		//find bin-center corresponding to i number of vertices
		dataDistr1BX.push_back(dataInput->GetBinContent(dataInput->GetXaxis()->FindBin(i)));

	lumiWeightOneX_ = edm::LumiReWeighting(mcDistr1BX, dataDistr1BX);
	lumiWeight3X_ = edm::LumiReWeighting(mcDistr, dataDistr);
	lumiWeight3D_ = edm::Lumi3DReWeighting(mcDistr, dataDistr);

	lumiWeight3D_.weight3D_init(1);

}


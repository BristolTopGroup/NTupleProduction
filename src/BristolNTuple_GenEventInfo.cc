#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenEventInfo.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

BristolNTuple_GenEventInfo::BristolNTuple_GenEventInfo(const edm::ParameterSet& iConfig) :
    genEvtInfoInputTag(iConfig.getParameter<edm::InputTag>("GenEventInfoInputTag")),
    storePDFWeights(iConfig.getParameter<bool>("StorePDFWeights")),
    pdfWeightsInputTag(iConfig.getParameter<edm::InputTag>("PDFWeightsInputTag")),
    pileupInfoSrc(iConfig.getParameter<edm::InputTag>("pileupInfo")),
    prefix(iConfig.getParameter<std::string> ("Prefix")),
    suffix(iConfig.getParameter<std::string> ("Suffix"))
{
    produces<unsigned int> (prefix + "ProcessID" + suffix);
    produces<double> (prefix + "PtHat" + suffix);
    produces<std::vector<double> > (prefix + "PDFWeights" + suffix);
    produces<std::vector<int> > (prefix + "PileUpInteractions" + suffix);
    produces<std::vector<int> > (prefix + "PileUpOriginBX" + suffix);
}

void BristolNTuple_GenEventInfo::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

    std::auto_ptr<unsigned int> processID(new unsigned int());
    std::auto_ptr<double> ptHat(new double());
    std::auto_ptr < std::vector<double> > pdfWeights(new std::vector<double>());
    std::auto_ptr < std::vector<int> > Number_interactions(new std::vector<int>());
    std::auto_ptr < std::vector<int> > OriginBX(new std::vector<int>());

    *processID.get() = 0;
    *ptHat.get() = 0.;

    //-----------------------------------------------------------------
    if (!iEvent.isRealData()) {
        // GenEventInfo Part
        edm::Handle < GenEventInfoProduct > genEvtInfoProduct;
        iEvent.getByLabel(genEvtInfoInputTag, genEvtInfoProduct);

        if (genEvtInfoProduct.isValid()) {
            edm::LogInfo("BristolNTuple_GenEventInfoInfo") << "Successfully obtained " << genEvtInfoInputTag;

            *processID.get() = genEvtInfoProduct->signalProcessID();
            *ptHat.get() = (genEvtInfoProduct->hasBinningValues() ? genEvtInfoProduct->binningValues()[0] : 0.);

        } else {
            edm::LogError("BristolNTuple_GenEventInfoError") << "Error! Can't get the product " << genEvtInfoInputTag;
        }
        // PDF Weights Part
        if (storePDFWeights) {
            edm::Handle < std::vector<double> > pdfWeightsHandle;
            iEvent.getByLabel(pdfWeightsInputTag, pdfWeightsHandle);

            if (pdfWeightsHandle.isValid()) {
                edm::LogInfo("BristolNTuple_GenEventInfoInfo") << "Successfully obtained " << pdfWeightsInputTag;

                *pdfWeights.get() = *pdfWeightsHandle;

            } else {
                edm::LogError("BristolNTuple_GenEventInfoError") << "Error! Can't get the product "
                        << pdfWeightsInputTag;
            }
        }
        // PileupSummary Part
        edm::Handle < std::vector<PileupSummaryInfo> > puInfo;
        iEvent.getByLabel(pileupInfoSrc, puInfo);

        if (puInfo.isValid()) {
            for (std::vector<PileupSummaryInfo>::const_iterator it = puInfo->begin(); it != puInfo->end(); ++it) {
                Number_interactions->push_back(it->getPU_NumInteractions());
                OriginBX -> push_back(it -> getBunchCrossing());
            }
        } else {
            edm::LogError("BristolNTuple_PileUpError") << "Error! Can't get the product " << pileupInfoSrc;
        }
    }

    //-----------------------------------------------------------------
    iEvent.put(processID, prefix + "ProcessID" + suffix);
    iEvent.put(ptHat, prefix + "PtHat" + suffix);
    iEvent.put(pdfWeights, prefix + "PDFWeights" + suffix);
    iEvent.put(Number_interactions, prefix + "PileUpInteractions" + suffix);
    iEvent.put(OriginBX, prefix + "PileUpOriginBX" + suffix);
}

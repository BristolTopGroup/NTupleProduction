#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_METcorrections.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"


BristolNTuple_METcorrections::BristolNTuple_METcorrections(const edm::ParameterSet& iConfig) :
        inputTag(consumes<CorrMETData> (iConfig.getParameter < edm::InputTag > ("InputTag"))), //
        prefix(iConfig.getParameter < std::string > ("Prefix")), //
        suffix(iConfig.getParameter < std::string > ("Suffix"))
{
        produces<double>(prefix + "x" + suffix);
        produces<double>(prefix + "y" + suffix);
        //      produces<double>(prefix + "sumet" + suffix);
}

void BristolNTuple_METcorrections::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<CorrMETData> metCorr;
    iEvent.getByToken(inputTag, metCorr);

    //    std::cout << "Systematic shift corrections, corrx = " << metCorr->mex << ", corry = " << metCorr->mey << std::endl;

    std::auto_ptr<double> corrx(new double(metCorr->mex));
    std::auto_ptr<double> corry(new double(metCorr->mey));
    //    std::auto_ptr<double> sumet(new double(metCorr->sumet));

    iEvent.put(corrx, prefix + "x" + suffix);
    iEvent.put(corry, prefix + "y" + suffix);
    //    iEvent.put(sumet, prefix + "sumet" + suffix);
}

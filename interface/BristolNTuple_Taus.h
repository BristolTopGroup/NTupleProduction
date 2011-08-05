#ifndef BristolNTupleTaus
#define BristolNTupleTaus

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

class BristolNTuple_Taus: public edm::EDProducer {
public:
    explicit BristolNTuple_Taus(const edm::ParameterSet&);

private:
    void produce(edm::Event &, const edm::EventSetup &);
    const edm::InputTag inputTag;
    const std::string prefix, suffix;
    const unsigned int maxSize;
};

#endif

#ifndef BristolNTupleGenMETExtra
#define BristolNTupleGenMETExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETFwd.h"

class BristolNTuple_GenMET : public edm::EDProducer {
 public:
  explicit BristolNTuple_GenMET(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::EDGetTokenT< std::vector<pat::MET> > inputTag;
  const std::string     prefix,suffix;
};

#endif

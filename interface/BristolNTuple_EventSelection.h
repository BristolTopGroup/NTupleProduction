#ifndef BristolNTupleEventSelection
#define BristolNTupleEventSelection

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

class BristolNTuple_EventSelection : public edm::EDProducer {
 public:
  explicit BristolNTuple_EventSelection(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   l1InputTag,vtxInputTag;
  const unsigned int    vtxMinNDOF;
  const double          vtxMaxAbsZ, vtxMaxd0;
  const edm::InputTag   trkInputTag;
  const unsigned int    numTracks;
  const double          hpTrackThreshold;
  const edm::InputTag   hcalNoiseInputTag;
  const std::string     prefix,suffix;
};

#endif

#ifndef BristolNTuplePFJetsExtra
#define BristolNTuplePFJetsExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondFormats/BTauObjects/interface/BTagCalibrationReader.h"

class BristolNTuple_PFJets : public edm::EDProducer {

 public:
  explicit BristolNTuple_PFJets(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::EDGetTokenT<std::vector<pat::Jet>> inputTag;
  const std::string     prefix,suffix;
  const unsigned int    maxSize;
  const double      minJetPtToStore;
  const std::string jecUncPath;
  const bool readJEC;
  const std::string jetCorrectionService;
  const bool readJECuncertainty, doVertexAssociation;
  const edm::EDGetTokenT<std::vector<reco::Vertex>> vtxInputTag;
  const bool isRealData;

  BTagCalibration calib;
  BTagCalibrationReader reader_bc;
  BTagCalibrationReader reader_bc_up;
  BTagCalibrationReader reader_bc_down;
  BTagCalibrationReader reader_l;
  BTagCalibrationReader reader_l_up;
  BTagCalibrationReader reader_l_down;
};

#endif

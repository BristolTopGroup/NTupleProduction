#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_BeamSpot.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

RootTupleMakerV2_BeamSpot::RootTupleMakerV2_BeamSpot(const edm::ParameterSet& iConfig) :
    prefix  (iConfig.getParameter<std::string>  ("Prefix")),
    suffix  (iConfig.getParameter<std::string>  ("Suffix"))
{
    produces<std::vector<double> > (prefix + "X0" + suffix);
    produces<std::vector<double> > (prefix + "Y0" + suffix);
    produces<std::vector<double> > (prefix + "Z0" + suffix);
    produces<std::vector<double> > (prefix + "X0Error" + suffix);
    produces<std::vector<double> > (prefix + "Y0Error" + suffix);
    produces<std::vector<double> > (prefix + "Z0Error" + suffix);

    produces<std::vector<double> > (prefix + "sigmaZ" + suffix);
    produces<std::vector<double> > (prefix + "sigmaZError" + suffix);
    produces<std::vector<double> > (prefix + "dxdz" + suffix);
    produces<std::vector<double> > (prefix + "dxdzError" + suffix);
    produces<std::vector<double> > (prefix + "dydz" + suffix);
    produces<std::vector<double> > (prefix + "dydzError" + suffix);

    produces<std::vector<double> > (prefix + "BeamWidthX" + suffix);
    produces<std::vector<double> > (prefix + "BeamWidthY" + suffix);
    produces<std::vector<double> > (prefix + "BeamWidthXError" + suffix);
    produces<std::vector<double> > (prefix + "BeamWidthYError" + suffix);
}

void RootTupleMakerV2_BeamSpot::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

    std::auto_ptr < std::vector<double> > x(new std::vector<double>());
    std::auto_ptr < std::vector<double> > y(new std::vector<double>());
    std::auto_ptr < std::vector<double> > z(new std::vector<double>());
    std::auto_ptr < std::vector<double> > xError(new std::vector<double>());
    std::auto_ptr < std::vector<double> > yError(new std::vector<double>());
    std::auto_ptr < std::vector<double> > zError(new std::vector<double>());

    std::auto_ptr < std::vector<double> > sigmaZ(new std::vector<double>());
    std::auto_ptr < std::vector<double> > sigmaZError(new std::vector<double>());
    std::auto_ptr < std::vector<double> > dxdz(new std::vector<double>());
    std::auto_ptr < std::vector<double> > dxdzError(new std::vector<double>());
    std::auto_ptr < std::vector<double> > dydz(new std::vector<double>());
    std::auto_ptr < std::vector<double> > dydzError(new std::vector<double>());

    std::auto_ptr < std::vector<double> > beamWidthX(new std::vector<double>());
    std::auto_ptr < std::vector<double> > beamWidthY(new std::vector<double>());
    std::auto_ptr < std::vector<double> > beamWidthXError(new std::vector<double>());
    std::auto_ptr < std::vector<double> > beamWidthYError(new std::vector<double>());
  
  //-----------------------------------------------------------------
    edm::Handle < reco::BeamSpot > beamSpot;
    iEvent.getByLabel("offlineBeamSpot", beamSpot);

  if(beamSpot.isValid()) {
    x->push_back(beamSpot->x0());
    y->push_back(beamSpot->y0());
    z->push_back(beamSpot->z0());
    xError->push_back(beamSpot->x0Error());
    yError->push_back(beamSpot->y0Error());
    zError->push_back(beamSpot->z0Error());

    sigmaZ->push_back(beamSpot->sigmaZ());
    sigmaZError->push_back(beamSpot->sigmaZ0Error());
    dxdz->push_back(beamSpot->dxdz());
    dxdzError->push_back(beamSpot->dxdzError());
    dydz->push_back(beamSpot->dydz());
    dydzError->push_back(beamSpot->dydzError());

    beamWidthX->push_back(beamSpot->BeamWidthX());
    beamWidthY->push_back(beamSpot->BeamWidthY());
    beamWidthXError->push_back(beamSpot->BeamWidthXError());
    beamWidthYError->push_back(beamSpot->BeamWidthYError());
  } else {
    edm::LogError("RootTupleMakerV2_BeamSpotError") << "Error! Can't get the product " << "offlineBeamSpot";
  }

  //-----------------------------------------------------------------
  // put vectors in the event
  iEvent.put(x, prefix + "X0" + suffix);
  iEvent.put(y, prefix + "Y0" + suffix);
  iEvent.put(z, prefix + "Z0" + suffix);
  iEvent.put(xError, prefix + "X0Error" + suffix);
  iEvent.put(yError, prefix + "Y0Error" + suffix);
  iEvent.put(zError, prefix + "Z0Error" + suffix);

  iEvent.put(sigmaZ, prefix + "sigmaZ" + suffix);
  iEvent.put(sigmaZError, prefix + "sigmaZError" + suffix);
  iEvent.put(dxdz, prefix + "dxdz" + suffix);
  iEvent.put(dxdzError, prefix + "dxdzError" + suffix);
  iEvent.put(dydz, prefix + "dydz" + suffix);
  iEvent.put(dydzError, prefix + "dydzError" + suffix);

  iEvent.put(beamWidthX, prefix + "BeamWidthX" + suffix);
  iEvent.put(beamWidthY, prefix + "BeamWidthY" + suffix);
  iEvent.put(beamWidthXError, prefix + "BeamWidthXError" + suffix);
  iEvent.put(beamWidthYError, prefix + "BeamWidthYError" + suffix);
}

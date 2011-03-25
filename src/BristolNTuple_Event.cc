#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Event.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"

BristolNTuple_Event::BristolNTuple_Event(const edm::ParameterSet& iConfig):
dcsInputTag(iConfig.getParameter<edm::InputTag>("DCSInputTag"))
{
  produces <double>       ( "magneticField" );
}

void BristolNTuple_Event::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  edm::Handle<DcsStatusCollection> dcsHandle;
    iEvent.getByLabel(dcsInputTag, dcsHandle);
    double evt_bField = 3.8;
      // need the magnetic field
      //
      // if isRealData then derive bfield using the
      // magnet current from DcsStatus
      // otherwise take it from the IdealMagneticFieldRecord
      if(iEvent.isRealData()) {
        if(dcsHandle.isValid()) {
          edm::LogInfo("BristolNTuple_ElectronsInfo") << "Successfully obtained " << dcsInputTag;
          // scale factor = 3.801/18166.0 which are
          // average values taken over a stable two-week period
          double currentToBFieldScaleFactor = 2.09237036221512717e-04;
          double current = (*dcsHandle)[0].magnetCurrent();
          evt_bField = current*currentToBFieldScaleFactor;
        } else {
          edm::LogError("BristolNTuple_Event") << "Error! Can't get the product " << dcsInputTag;
        }
      } else {
        edm::ESHandle<MagneticField> magneticField;
        iSetup.get<IdealMagneticFieldRecord>().get(magneticField);

        if(magneticField.isValid()) {
          edm::LogInfo("BristolNTuple_EventInfo") << "Successfully obtained IdealMagneticFieldRecord";

          evt_bField = magneticField->inTesla(GlobalPoint(0.,0.,0.)).z();
        } else {
          edm::LogError("BristolNTuple_EventError") << "Error! Can't get IdealMagneticFieldRecord";
        }
      }
  std::auto_ptr<double >  magField  ( new double(evt_bField)  );

  //-----------------------------------------------------------------
  iEvent.put( magField,   "magneticField"   );
}

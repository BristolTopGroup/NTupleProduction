#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Electrons.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "RecoEgamma/EgammaTools/interface/ConversionFinder.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

BristolNTuple_Electrons::BristolNTuple_Electrons(const edm::ParameterSet& iConfig) :
    trkInputTag(iConfig.getParameter<edm::InputTag> ("TracksInputTag")),
    dcsInputTag(iConfig.getParameter<edm::InputTag> ("DCSInputTag")),
    inputTag(iConfig.getParameter<edm::InputTag> ("InputTag")),
    prefix(iConfig.getParameter<std::string> ("Prefix")),
    suffix(iConfig.getParameter<std::string> ("Suffix")),
    maxSize(iConfig.getParameter<unsigned int> ("MaxSize")),
    storePFIsolation(iConfig.getParameter<bool> ("storePFIsolation")),
    vtxInputTag(iConfig.getParameter<edm::InputTag> ("VertexInputTag")) {

    produces<std::vector<double> > (prefix + "Eta" + suffix);
    produces<std::vector<double> > (prefix + "Phi" + suffix);
    produces<std::vector<double> > (prefix + "Pt" + suffix);
    produces<std::vector<double> > (prefix + "Px" + suffix);
    produces<std::vector<double> > (prefix + "Py" + suffix);
    produces<std::vector<double> > (prefix + "Pz" + suffix);
    produces<std::vector<double> > (prefix + "Energy" + suffix);
    produces<std::vector<double> > (prefix + "CaloEnergy" + suffix);
    produces<std::vector<int> > (prefix + "Charge" + suffix);

    produces<std::vector<double> > (prefix + "HoE" + suffix);
    produces<std::vector<double> > (prefix + "SigmaEtaEta" + suffix);
    produces<std::vector<double> > (prefix + "SigmaIEtaIEta" + suffix);
    produces<std::vector<double> > (prefix + "DeltaPhiTrkSC" + suffix);
    produces<std::vector<double> > (prefix + "DeltaEtaTrkSC" + suffix);

    produces<std::vector<double> > (prefix + "TrkIso03" + suffix);
    produces<std::vector<double> > (prefix + "EcalIso03" + suffix);
    produces<std::vector<double> > (prefix + "HcalIso03" + suffix);
    produces<std::vector<double> > (prefix + "TrkIso" + suffix);
    produces<std::vector<double> > (prefix + "EcalIso" + suffix);
    produces<std::vector<double> > (prefix + "HcalIso" + suffix);

    produces<std::vector<double> > (prefix + "dB" + suffix);

    produces<std::vector<int> > (prefix + "closestCtfTrackRef" + suffix);
    produces<std::vector<double> > (prefix + "shFracInnerHits" + suffix);

    produces<std::vector<double> > (prefix + "GSFTrack.d0" + suffix);
    produces<std::vector<double> > (prefix + "GSFTrack.Eta" + suffix);
    produces<std::vector<double> > (prefix + "GSFTrack.Phi" + suffix);
    produces<std::vector<double> > (prefix + "GSFTrack.Theta" + suffix);
    produces<std::vector<int> > (prefix + "GSFTrack.Charge" + suffix);
    produces<std::vector<double> > (prefix + "GSFTrack.Pt" + suffix);

    produces<std::vector<double> > (prefix + "EcalIsoHeep" + suffix);
    produces<std::vector<double> > (prefix + "HcalIsoD1Heep" + suffix);
    produces<std::vector<double> > (prefix + "HcalIsoD2Heep" + suffix);
    produces<std::vector<double> > (prefix + "TrkIsoHeep" + suffix);

    produces<std::vector<int> > (prefix + "MissingHits" + suffix);
    produces<std::vector<double> > (prefix + "Dist" + suffix);
    produces<std::vector<double> > (prefix + "DCotTheta" + suffix);

    produces<std::vector<double> > (prefix + "SCEta" + suffix);
    produces<std::vector<double> > (prefix + "SCPhi" + suffix);
    produces<std::vector<double> > (prefix + "SCPt" + suffix);
    produces<std::vector<double> > (prefix + "SCRawEnergy" + suffix);

    produces<std::vector<int> > (prefix + "VtxIndex" + suffix);
    produces<std::vector<double> > (prefix + "VtxDistXY" + suffix);
    produces<std::vector<double> > (prefix + "VtxDistZ" + suffix);

    produces<std::vector<double> > (prefix + "Vertex.X" + suffix);
    produces<std::vector<double> > (prefix + "Vertex.Y" + suffix);
    produces<std::vector<double> > (prefix + "Vertex.Z" + suffix);

    if (storePFIsolation) {
        produces<std::vector<double> > (prefix + "PfChargedHadronIso" + suffix);
        produces<std::vector<double> > (prefix + "PfNeutralHadronIso" + suffix);
        produces<std::vector<double> > (prefix + "PFGammaIso" + suffix);
    }
}

void BristolNTuple_Electrons::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    std::auto_ptr < std::vector<double> > eta(new std::vector<double>());
    std::auto_ptr < std::vector<double> > phi(new std::vector<double>());
    std::auto_ptr < std::vector<double> > pt(new std::vector<double>());
    std::auto_ptr < std::vector<double> > px(new std::vector<double>());
    std::auto_ptr < std::vector<double> > py(new std::vector<double>());
    std::auto_ptr < std::vector<double> > pz(new std::vector<double>());
    std::auto_ptr < std::vector<double> > energy(new std::vector<double>());
    std::auto_ptr < std::vector<double> > caloEnergy(new std::vector<double>());
    std::auto_ptr < std::vector<int> > charge(new std::vector<int>());

    std::auto_ptr < std::vector<double> > hoe(new std::vector<double>());
    std::auto_ptr < std::vector<double> > sigmaEtaEta(new std::vector<double>());
    std::auto_ptr < std::vector<double> > sigmaIEtaIEta(new std::vector<double>());
    std::auto_ptr < std::vector<double> > deltaPhiTrkSC(new std::vector<double>());
    std::auto_ptr < std::vector<double> > deltaEtaTrkSC(new std::vector<double>());

    std::auto_ptr < std::vector<double> > trkIso(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ecalIso(new std::vector<double>());
    std::auto_ptr < std::vector<double> > hcalIso(new std::vector<double>());
    std::auto_ptr < std::vector<double> > trkIso03(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ecalIso03(new std::vector<double>());
    std::auto_ptr < std::vector<double> > hcalIso03(new std::vector<double>());

    std::auto_ptr < std::vector<double> > dB(new std::vector<double>());

    std::auto_ptr < std::vector<double> > PfChargedHadronIso(new std::vector<double>());
    std::auto_ptr < std::vector<double> > PfNeutralHadronIso(new std::vector<double>());
    std::auto_ptr < std::vector<double> > PFGammaIso(new std::vector<double>());

    std::auto_ptr < std::vector<int> > closestCtfTrackRef(new std::vector<int>());
    std::auto_ptr < std::vector<double> > shFracInnerHits(new std::vector<double>());
    std::auto_ptr < std::vector<double> > gsfTrackD0(new std::vector<double>());
    std::auto_ptr < std::vector<double> > gsfTrackEta(new std::vector<double>());
    std::auto_ptr < std::vector<double> > gsfTrackPhi(new std::vector<double>());
    std::auto_ptr < std::vector<double> > gsfTrackTheta(new std::vector<double>());
    std::auto_ptr < std::vector<int> > gsfTrackCharge(new std::vector<int>());
    std::auto_ptr < std::vector<double> > gsfTrackPt(new std::vector<double>());

    std::auto_ptr < std::vector<double> > ecalIsoHeep(new std::vector<double>());
    std::auto_ptr < std::vector<double> > hcalIsoD1Heep(new std::vector<double>());
    std::auto_ptr < std::vector<double> > hcalIsoD2Heep(new std::vector<double>());
    std::auto_ptr < std::vector<double> > trkIsoHeep(new std::vector<double>());

    std::auto_ptr < std::vector<int> > missingHits(new std::vector<int>());
    std::auto_ptr < std::vector<double> > dist_vec(new std::vector<double>());
    std::auto_ptr < std::vector<double> > dCotTheta(new std::vector<double>());

    std::auto_ptr < std::vector<double> > scEta(new std::vector<double>());
    std::auto_ptr < std::vector<double> > scPhi(new std::vector<double>());
    std::auto_ptr < std::vector<double> > scPt(new std::vector<double>());
    std::auto_ptr < std::vector<double> > scRawEnergy(new std::vector<double>());

    std::auto_ptr < std::vector<int> > vtxIndex(new std::vector<int>());
    std::auto_ptr < std::vector<double> > vtxDistXY(new std::vector<double>());
    std::auto_ptr < std::vector<double> > vtxDistZ(new std::vector<double>());

    std::auto_ptr < std::vector<double> > VertexX(new std::vector<double>());
    std::auto_ptr < std::vector<double> > VertexY(new std::vector<double>());
    std::auto_ptr < std::vector<double> > VertexZ(new std::vector<double>());

    //-----------------------------------------------------------------
    edm::Handle < std::vector<pat::Electron> > electrons;
    iEvent.getByLabel(inputTag, electrons);

    edm::Handle < reco::TrackCollection > tracks;
    iEvent.getByLabel(trkInputTag, tracks);

    edm::Handle < DcsStatusCollection > dcsHandle;
    iEvent.getByLabel(dcsInputTag, dcsHandle);

    edm::Handle < reco::VertexCollection > primaryVertices;
    iEvent.getByLabel(vtxInputTag, primaryVertices);

    double evt_bField = 3.8;
    // need the magnetic field
    //
    // if isRealData then derive bfield using the
    // magnet current from DcsStatus
    // otherwise take it from the IdealMagneticFieldRecord
    if (iEvent.isRealData()) {
        if (dcsHandle.isValid()) {
            edm::LogInfo("RootTupleMakerV2_ElectronsInfo") << "Successfully obtained " << dcsInputTag;
            // scale factor = 3.801/18166.0 which are
            // average values taken over a stable two-week period
            double currentToBFieldScaleFactor = 2.09237036221512717e-04;
            if ((*dcsHandle).size() > 0) {
                double current = (*dcsHandle)[0].magnetCurrent();
                evt_bField = current * currentToBFieldScaleFactor;
            }
        } else {
            edm::LogError("RootTupleMakerV2_ElectronsError") << "Error! Can't get the product " << dcsInputTag;
        }
    } else {
        edm::ESHandle < MagneticField > magneticField;
        iSetup.get<IdealMagneticFieldRecord> ().get(magneticField);

        if (magneticField.isValid()) {
            edm::LogInfo("RootTupleMakerV2_ElectronsInfo") << "Successfully obtained IdealMagneticFieldRecord";

            evt_bField = magneticField->inTesla(GlobalPoint(0., 0., 0.)).z();
        } else {
            edm::LogError("RootTupleMakerV2_ElectronsError") << "Error! Can't get IdealMagneticFieldRecord";
        }
    }

    if (electrons.isValid()) {
        edm::LogInfo("BristolNTuple_ElectronsExtraInfo") << "Total # Electrons: " << electrons->size();
        for (std::vector<pat::Electron>::const_iterator it = electrons->begin(); it != electrons->end(); ++it) {
            // exit from loop when you reach the required number of electrons
            if (px->size() >= maxSize)
                break;

            // Conversion
            ConversionFinder convFinder;
            double dist = -9999.;
            double dcot = -9999.;
            if (tracks.isValid()) {
                edm::LogInfo("RootTupleMakerV2_ElectronsInfo") << "Successfully obtained " << trkInputTag;

                ConversionInfo convInfo = convFinder.getConversionInfo(*it, tracks, evt_bField);
                dist = convInfo.dist();
                dcot = convInfo.dcot();
            } else {
                edm::LogError("RootTupleMakerV2_ElectronsError") << "Error! Can't get the product " << trkInputTag;
            }

            // Vertex association
            double minVtxDist3D = 9999.;
            int vtxIndex_ = -1;
            double vtxDistXY_ = -9999.;
            double vtxDistZ_ = -9999.;

            if (primaryVertices.isValid()) {
                edm::LogInfo("RootTupleMakerV2_ElectronsInfo") << "Total # Primary Vertices: "
                        << primaryVertices->size();

                for (reco::VertexCollection::const_iterator v_it = primaryVertices->begin(); v_it
                        != primaryVertices->end(); ++v_it) {

                    double distXY = it->gsfTrack()->dxy(v_it->position());
                    double distZ = it->gsfTrack()->dz(v_it->position());
                    double dist3D = sqrt(pow(distXY, 2) + pow(distZ, 2));

                    if (dist3D < minVtxDist3D) {
                        minVtxDist3D = dist3D;
                        vtxIndex_ = int(std::distance(primaryVertices->begin(), v_it));
                        vtxDistXY_ = distXY;
                        vtxDistZ_ = distZ;
                    }
                }
            } else {
                edm::LogError("RootTupleMakerV2_ElectronsError") << "Error! Can't get the product " << vtxInputTag;
            }

            eta->push_back(it->eta());
            phi->push_back(it->phi());
            pt->push_back(it->pt());
            px->push_back(it->px());
            py->push_back(it->py());
            pz->push_back(it->pz());
            gsfTrackPt->push_back(it->gsfTrack()->pt());
            energy->push_back(it->energy());
            caloEnergy->push_back(it->caloEnergy());
            charge->push_back(it->charge());

            // ID variables
            hoe->push_back(it->hadronicOverEm());
            sigmaEtaEta->push_back(it->sigmaEtaEta());
            sigmaIEtaIEta->push_back(it->sigmaIetaIeta());
            deltaPhiTrkSC->push_back(it->deltaPhiSuperClusterTrackAtVtx());
            deltaEtaTrkSC->push_back(it->deltaEtaSuperClusterTrackAtVtx());

            //Iso variables
            trkIso->push_back(it->trackIso());
            ecalIso->push_back(it->ecalIso());
            hcalIso->push_back(it->hcalIso());
            trkIso03->push_back(it->dr03TkSumPt());
            ecalIso03->push_back(it->dr03EcalRecHitSumEt());
            hcalIso03->push_back(it->dr03HcalTowerSumEt());

            // Iso variables (Heep)
            ecalIsoHeep->push_back(it->dr03EcalRecHitSumEt());
            hcalIsoD1Heep->push_back(it->dr03HcalDepth1TowerSumEt());
            hcalIsoD2Heep->push_back(it->dr03HcalDepth2TowerSumEt());
            trkIsoHeep->push_back(it->dr03TkSumPt());

            // Conversion variables
            missingHits->push_back(it->gsfTrack()->trackerExpectedHitsInner().numberOfHits());
            dist_vec->push_back(dist);
            dCotTheta->push_back(dcot);

            // SC associated with electron
            scEta->push_back(it->superCluster()->eta());
            scPhi->push_back(it->superCluster()->phi());
            scPt->push_back(it->superCluster()->energy() / cosh(it->superCluster()->eta()));
            scRawEnergy->push_back(it->superCluster()->rawEnergy());

            closestCtfTrackRef->push_back(static_cast<int> (it->closestCtfTrackRef().key()));
            shFracInnerHits->push_back(it->shFracInnerHits());

            gsfTrackD0->push_back(it->gsfTrack()->d0());
            gsfTrackEta->push_back(it->gsfTrack()->eta());
            gsfTrackPhi->push_back(it->gsfTrack()->phi());
            gsfTrackTheta->push_back(it->gsfTrack()->theta());
            gsfTrackCharge->push_back(it->gsfTrack()->charge());
            dB->push_back(it->dB());

            // Vertex association variables
            vtxIndex->push_back(vtxIndex_);
            vtxDistXY->push_back(vtxDistXY_);
            vtxDistZ->push_back(vtxDistZ_);

            VertexX->push_back(it->vertex().x());
            VertexY->push_back(it->vertex().y());
            VertexZ->push_back(it->vertex().z());

            if (storePFIsolation) {
                pat::IsolationKeys isokeyPfChargedHadronIso = pat::IsolationKeys(4);
                pat::IsolationKeys isokeyPfNeutralHadronIso = pat::IsolationKeys(5);
                pat::IsolationKeys isokeyPFGammaIso = pat::IsolationKeys(6);

                const reco::IsoDeposit * PfChargedHadronIsolation = it->isoDeposit(isokeyPfChargedHadronIso);
                const reco::IsoDeposit * PfNeutralHadronIsolation = it->isoDeposit(isokeyPfNeutralHadronIso);
                const reco::IsoDeposit * PFGammaIsolation = it->isoDeposit(isokeyPFGammaIso);
                if (PfChargedHadronIsolation)
                    PfChargedHadronIso->push_back(PfChargedHadronIsolation->depositWithin(0.3));
                else
                    edm::LogError("BristolNTuple_ElectronsExtraError") << "Error! Can't get the isolation deposit "
                            << "PfChargedHadronIsolation";
                if (PfNeutralHadronIsolation)
                    PfNeutralHadronIso->push_back(PfNeutralHadronIsolation->depositWithin(0.3));
                else
                    edm::LogError("BristolNTuple_ElectronsExtraError") << "Error! Can't get the isolation deposit "
                            << "PfNeutralHadronIsolation";
                if (PFGammaIsolation)
                    PFGammaIso->push_back(PFGammaIsolation->depositWithin(0.3));
                else
                    edm::LogError("BristolNTuple_ElectronsExtraError") << "Error! Can't get the isolation deposit "
                            << "PFGammaIsolation";
            }

        }
    } else {
        edm::LogError("BristolNTuple_ElectronsExtraError") << "Error! Can't get the product " << inputTag;
    }


    //-----------------------------------------------------------------
    // put vectors in the event
    iEvent.put(eta, prefix + "Eta" + suffix);
    iEvent.put(phi, prefix + "Phi" + suffix);
    iEvent.put(pt, prefix + "Pt" + suffix);
    iEvent.put(px, prefix + "Px" + suffix);
    iEvent.put(py, prefix + "Py" + suffix);
    iEvent.put(pz, prefix + "Pz" + suffix);
    iEvent.put(energy, prefix + "Energy" + suffix);
    iEvent.put(caloEnergy, prefix + "CaloEnergy" + suffix);
    iEvent.put(charge, prefix + "Charge" + suffix);

    iEvent.put(hoe, prefix + "HoE" + suffix);
    iEvent.put(sigmaEtaEta, prefix + "SigmaEtaEta" + suffix);
    iEvent.put(sigmaIEtaIEta, prefix + "SigmaIEtaIEta" + suffix);
    iEvent.put(deltaPhiTrkSC, prefix + "DeltaPhiTrkSC" + suffix);
    iEvent.put(deltaEtaTrkSC, prefix + "DeltaEtaTrkSC" + suffix);

    iEvent.put(trkIso, prefix + "TrkIso" + suffix);
    iEvent.put(ecalIso, prefix + "EcalIso" + suffix);
    iEvent.put(hcalIso, prefix + "HcalIso" + suffix);
    iEvent.put(trkIso03, prefix + "TrkIso03" + suffix);
    iEvent.put(ecalIso03, prefix + "EcalIso03" + suffix);
    iEvent.put(hcalIso03, prefix + "HcalIso03" + suffix);
    iEvent.put(ecalIsoHeep, prefix + "EcalIsoHeep" + suffix);
    iEvent.put(hcalIsoD1Heep, prefix + "HcalIsoD1Heep" + suffix);
    iEvent.put(hcalIsoD2Heep, prefix + "HcalIsoD2Heep" + suffix);
    iEvent.put(trkIsoHeep, prefix + "TrkIsoHeep" + suffix);

    iEvent.put(missingHits, prefix + "MissingHits" + suffix);
    iEvent.put(dist_vec, prefix + "Dist" + suffix);
    iEvent.put(dCotTheta, prefix + "DCotTheta" + suffix);

    iEvent.put(scEta, prefix + "SCEta" + suffix);
    iEvent.put(scPhi, prefix + "SCPhi" + suffix);
    iEvent.put(scPt, prefix + "SCPt" + suffix);
    iEvent.put(scRawEnergy, prefix + "SCRawEnergy" + suffix);
    iEvent.put(vtxIndex, prefix + "VtxIndex" + suffix);
    iEvent.put(vtxDistXY, prefix + "VtxDistXY" + suffix);
    iEvent.put(vtxDistZ, prefix + "VtxDistZ" + suffix);

    iEvent.put(dB, prefix + "dB" + suffix);

    iEvent.put(closestCtfTrackRef, prefix + "closestCtfTrackRef" + suffix);
    iEvent.put(shFracInnerHits, prefix + "shFracInnerHits" + suffix);

    iEvent.put(gsfTrackPt, prefix + "GSFTrack.Pt" + suffix);
    iEvent.put(gsfTrackD0, prefix + "GSFTrack.d0" + suffix);
    iEvent.put(gsfTrackEta, prefix + "GSFTrack.Eta" + suffix);
    iEvent.put(gsfTrackPhi, prefix + "GSFTrack.Phi" + suffix);
    iEvent.put(gsfTrackTheta, prefix + "GSFTrack.Theta" + suffix);
    iEvent.put(gsfTrackCharge, prefix + "GSFTrack.Charge" + suffix);

    iEvent.put(VertexX, prefix + "Vertex.X" + suffix);
    iEvent.put(VertexY, prefix + "Vertex.Y" + suffix);
    iEvent.put(VertexZ, prefix + "Vertex.Z" + suffix);

    if (storePFIsolation) {
        iEvent.put(PfChargedHadronIso, prefix + "PfChargedHadronIso" + suffix);
        iEvent.put(PfNeutralHadronIso, prefix + "PfNeutralHadronIso" + suffix);
        iEvent.put(PFGammaIso, prefix + "PFGammaIso" + suffix);
    }
}

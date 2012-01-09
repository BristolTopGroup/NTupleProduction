#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Electrons.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "FWCore/Framework/interface/ESHandle.h"
//#include "MagneticField/Engine/interface/MagneticField.h"
//#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
//#include "RecoEgamma/EgammaTools/interface/ConversionFinder.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"

BristolNTuple_Electrons::BristolNTuple_Electrons(const edm::ParameterSet& iConfig) :
    trkInputTag(iConfig.getParameter<edm::InputTag> ("TracksInputTag")),
    dcsInputTag(iConfig.getParameter<edm::InputTag> ("DCSInputTag")),
    inputTag(iConfig.getParameter<edm::InputTag> ("InputTag")),
    prefix(iConfig.getParameter<std::string> ("Prefix")),
    suffix(iConfig.getParameter<std::string> ("Suffix")),
    maxSize(iConfig.getParameter<unsigned int> ("MaxSize")),
    storePFIsolation(iConfig.getParameter<bool> ("storePFIsolation")),
    vtxInputTag(iConfig.getParameter<edm::InputTag> ("VertexInputTag")),
    beamSpotInputTag(iConfig.getParameter<edm::InputTag>   ("BeamSpotInputTag")),
    conversionsInputTag(iConfig.getParameter<edm::InputTag>("ConversionsInputTag")),
    likelihoodInputTag(iConfig.getParameter<edm::InputTag> ("LikelihoodInputTag")){

	//kinematic variables
    produces<std::vector<double> > (prefix + "Px" + suffix);
    produces<std::vector<double> > (prefix + "Py" + suffix);
    produces<std::vector<double> > (prefix + "Pz" + suffix);
    produces<std::vector<double> > (prefix + "Energy" + suffix);
    //extra properties
    produces<std::vector<int> > (prefix + "Charge" + suffix);

    //electron ID variables
    produces < std::vector<double> > (prefix + "HadronicOverEM" + suffix);
	produces < std::vector<double> > (prefix + "eSeedClusterOverPout" + suffix);
	produces < std::vector<double> > (prefix + "ESuperClusterOverP" + suffix);
	produces < std::vector<double> > (prefix + "Fbrem" + suffix);
	produces < std::vector<double> > (prefix + "SigmaEtaEta" + suffix);
	produces < std::vector<double> > (prefix + "SigmaIEtaIEta" + suffix);
	produces < std::vector<double> > (prefix + "DeltaPhiTrkSC" + suffix);
	produces < std::vector<double> > (prefix + "DeltaEtaTrkSC" + suffix);
	produces <std::vector<int> >    ( prefix + "PassID" + suffix );
	produces <std::vector<int> >    ( prefix + "PassIDMC" + suffix );
	produces <std::vector<bool> >    ( prefix + "eidVeryLooseMC" + suffix );
	produces <std::vector<bool> >    ( prefix + "eidLooseMC" + suffix );
	produces <std::vector<bool> >    ( prefix + "eidMediumMC" + suffix );
	produces <std::vector<bool> >    ( prefix + "eidTightMC" + suffix );
	produces <std::vector<bool> >    ( prefix + "eidSuperTightMC" + suffix );
	produces <std::vector<bool> >    ( prefix + "eidHyperTight1MC" + suffix );
	produces <std::vector<bool> >    ( prefix + "eidHyperTight2MC" + suffix );
	produces <std::vector<bool> >    ( prefix + "eidHyperTight3MC" + suffix );
	produces <std::vector<bool> >    ( prefix + "eidHyperTight4MC" + suffix );
	produces < std::vector<double> > (prefix + "Likelihood" + suffix);
	produces < std::vector<int> > (prefix + "NumberOfBrems" + suffix);

	//electron isolation variables
	produces < std::vector<double> > (prefix + "TrkIso03" + suffix);
	produces < std::vector<double> > (prefix + "EcalIso03" + suffix);
	produces < std::vector<double> > (prefix + "HcalIso03" + suffix);
	produces < std::vector<double> > (prefix + "RelIso03" + suffix);
	produces < std::vector<double> > (prefix + "TrkIso04" + suffix);
	produces < std::vector<double> > (prefix + "EcalIso04" + suffix);
	produces < std::vector<double> > (prefix + "HcalIso04" + suffix);
	produces < std::vector<double> > (prefix + "RelIso04" + suffix);

	//electron PF isolation variables
	if (storePFIsolation) {
		produces < std::vector<double> > (prefix + "PfChargedHadronIso03" + suffix);
		produces < std::vector<double> > (prefix + "PfNeutralHadronIso03" + suffix);
		produces < std::vector<double> > (prefix + "PFGammaIso03" + suffix);
		produces < std::vector<double> > (prefix + "PFRelIso03" + suffix);
		produces < std::vector<double> > (prefix + "PfChargedHadronIso04" + suffix);
		produces < std::vector<double> > (prefix + "PfNeutralHadronIso04" + suffix);
		produces < std::vector<double> > (prefix + "PFGammaIso04" + suffix);
		produces < std::vector<double> > (prefix + "PFRelIso04" + suffix);
		produces < std::vector<double> > (prefix + "PfChargedHadronIso05" + suffix);
		produces < std::vector<double> > (prefix + "PfNeutralHadronIso05" + suffix);
		produces < std::vector<double> > (prefix + "PFGammaIso05" + suffix);
		produces < std::vector<double> > (prefix + "PFRelIso05" + suffix);
	}

	//high energy electron isolation variables
	produces < std::vector<double> > (prefix + "EcalIsoHeep03" + suffix);
	produces < std::vector<double> > (prefix + "HcalIsoD1Heep03" + suffix);
	produces < std::vector<double> > (prefix + "HcalIsoD2Heep03" + suffix);
	produces < std::vector<double> > (prefix + "TrkIsoHeep03" + suffix);
	produces < std::vector<double> > (prefix + "EcalIsoHeep04" + suffix);
	produces < std::vector<double> > (prefix + "HcalIsoD1Heep04" + suffix);
	produces < std::vector<double> > (prefix + "HcalIsoD2Heep04" + suffix);
	produces < std::vector<double> > (prefix + "TrkIsoHeep04" + suffix);

	//electron conversion identification variables
	produces < std::vector<double> > (prefix + "Dist" + suffix);
	produces < std::vector<double> > (prefix + "DCotTheta" + suffix);
	produces < std::vector<double> > (prefix + "ConvRadius" + suffix);
	produces < std::vector<int> > (prefix + "MissingHits" + suffix);
	produces <std::vector<bool> >   ( prefix + "HasMatchedConvPhot" + suffix );
	produces<std::vector<double> > (prefix + "shFracInnerHits" + suffix);


	//associated track
//	produces < std::vector<int> > (prefix + "closestCtfTrackRef" + suffix);
//	produces < std::vector<double> > (prefix + "GSFTrack.d0" + suffix);
//	produces < std::vector<double> > (prefix + "GSFTrack.Eta" + suffix);
//	produces < std::vector<double> > (prefix + "GSFTrack.Phi" + suffix);
//	produces < std::vector<double> > (prefix + "GSFTrack.Theta" + suffix);
//	produces < std::vector<int> > (prefix + "GSFTrack.Charge" + suffix);
//	produces < std::vector<double> > (prefix + "GSFTrack.Pt" + suffix);

	//calorimeter variables
//	produces<std::vector<double> > (prefix + "CaloEnergy" + suffix);
    produces<std::vector<double> > (prefix + "SCEta" + suffix);
    produces<std::vector<double> > (prefix + "SCPhi" + suffix);
    produces<std::vector<double> > (prefix + "SCPt" + suffix);
    produces<std::vector<double> > (prefix + "SCRawEnergy" + suffix);

    //electron vertex variables
    produces<std::vector<int> > (prefix + "VtxIndex" + suffix);
    produces<std::vector<double> > (prefix + "VtxDistZ" + suffix);
    produces <std::vector<double> > ( prefix + "PrimaryVertexDXY" + suffix );//2D impact parameter, XY distance to vertex
    produces <std::vector<double> > ( prefix + "PrimaryVertexDXYError" + suffix );
    produces <std::vector<double> > ( prefix + "BeamSpotDXY" + suffix );
    produces <std::vector<double> > ( prefix + "BeamSpotDXYError" + suffix );
//    produces<std::vector<double> > (prefix + "VtxDistXY" + suffix);//identical to dB



}

void BristolNTuple_Electrons::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	//kinematic variables
    std::auto_ptr < std::vector<double> > px(new std::vector<double>());
    std::auto_ptr < std::vector<double> > py(new std::vector<double>());
    std::auto_ptr < std::vector<double> > pz(new std::vector<double>());
    std::auto_ptr < std::vector<double> > energy(new std::vector<double>());
    //extra properties
    std::auto_ptr < std::vector<int> > charge(new std::vector<int>());

    //electron ID variables
    std::auto_ptr < std::vector<double> > hadronicOverEM(new std::vector<double>());
	std::auto_ptr < std::vector<double> > EseedOverPout(new std::vector<double>());
	std::auto_ptr < std::vector<double> > eSuperClusterOverP(new std::vector<double>());
	std::auto_ptr < std::vector<double> > fbrem(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sigmaEtaEta(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sigmaIEtaIEta(new std::vector<double>());
	std::auto_ptr < std::vector<double> > deltaPhiTrkSC(new std::vector<double>());
	std::auto_ptr < std::vector<double> > deltaEtaTrkSC(new std::vector<double>());
	std::auto_ptr < std::vector<int> > passID(new std::vector<int>());
	std::auto_ptr < std::vector<int> > passIDMC(new std::vector<int>());
	std::auto_ptr < std::vector<bool> > eidVeryLooseMC(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > eidLooseMC(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > eidMediumMC(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > eidTightMC(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > eidSuperTightMC(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > eidHyperTight1MC(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > eidHyperTight2MC(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > eidHyperTight3MC(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > eidHyperTight4MC(new std::vector<bool>());
	std::auto_ptr < std::vector<double> > likelihood(new std::vector<double>());
	std::auto_ptr < std::vector<int> > numberOfBrems(new std::vector<int>());


    //electron isolation variables
    std::auto_ptr < std::vector<double> > trkIso04(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ecalIso04(new std::vector<double>());
    std::auto_ptr < std::vector<double> > hcalIso04(new std::vector<double>());
    std::auto_ptr < std::vector<double> > relIso04(new std::vector<double>());
    //smaller cone
    std::auto_ptr < std::vector<double> > trkIso03(new std::vector<double>());
    std::auto_ptr < std::vector<double> > ecalIso03(new std::vector<double>());
    std::auto_ptr < std::vector<double> > hcalIso03(new std::vector<double>());
    std::auto_ptr < std::vector<double> > relIso03(new std::vector<double>());

    //electron PF isolation variables
	std::auto_ptr < std::vector<double> > PfChargedHadronIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfNeutralHadronIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFGammaIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFRelIso03(new std::vector<double>());

	std::auto_ptr < std::vector<double> > PfChargedHadronIso04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfNeutralHadronIso04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFGammaIso04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFRelIso04(new std::vector<double>());

	std::auto_ptr < std::vector<double> > PfChargedHadronIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PfNeutralHadronIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFGammaIso05(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFRelIso05(new std::vector<double>());


//    std::auto_ptr < std::vector<double> > dB(new std::vector<double>());

    //high energy electron isolation variables
    std::auto_ptr < std::vector<double> > ecalIsoHeep03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > hcalIsoD1Heep03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > hcalIsoD2Heep03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > trkIsoHeep03(new std::vector<double>());

	std::auto_ptr < std::vector<double> > ecalIsoHeep04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > hcalIsoD1Heep04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > hcalIsoD2Heep04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > trkIsoHeep04(new std::vector<double>());

	//electron conversion identification variables
	std::auto_ptr < std::vector<int> > missingHits(new std::vector<int>());
	std::auto_ptr < std::vector<double> > dist_vec(new std::vector<double>());
	std::auto_ptr < std::vector<double> > dCotTheta(new std::vector<double>());
	std::auto_ptr < std::vector<double> > conversionRadius(new std::vector<double>());
	std::auto_ptr < std::vector<bool> > hasMatchedConvPhot(new std::vector<bool>());
	std::auto_ptr < std::vector<double> > shFracInnerHits(new std::vector<double>());

	//associated track
//    std::auto_ptr < std::vector<int> > closestCtfTrackRef(new std::vector<int>());
//    std::auto_ptr < std::vector<double> > gsfTrackD0(new std::vector<double>());
//    std::auto_ptr < std::vector<double> > gsfTrackEta(new std::vector<double>());
//    std::auto_ptr < std::vector<double> > gsfTrackPhi(new std::vector<double>());
//    std::auto_ptr < std::vector<double> > gsfTrackTheta(new std::vector<double>());
//    std::auto_ptr < std::vector<int> > gsfTrackCharge(new std::vector<int>());
//    std::auto_ptr < std::vector<double> > gsfTrackPt(new std::vector<double>());

	//calorimeter variables
    std::auto_ptr < std::vector<double> > scEta(new std::vector<double>());
    std::auto_ptr < std::vector<double> > scPhi(new std::vector<double>());
    std::auto_ptr < std::vector<double> > scPt(new std::vector<double>());
    std::auto_ptr < std::vector<double> > scRawEnergy(new std::vector<double>());

    //electron vertex variables
    std::auto_ptr < std::vector<int> > vtxIndex(new std::vector<int>());
    std::auto_ptr < std::vector<double> > vtxDistZ(new std::vector<double>());
    std::auto_ptr < std::vector<double> > primaryVertexDXY(new std::vector<double>());
    std::auto_ptr < std::vector<double> > primaryVertexDXYError(new std::vector<double>());
    std::auto_ptr < std::vector<double> > beamSpotDXY(new std::vector<double>());
    std::auto_ptr < std::vector<double> > beamSpotDXYError(new std::vector<double>());

    //-----------------------------------------------------------------
    edm::Handle < std::vector<pat::Electron> > electrons;
	iEvent.getByLabel(inputTag, electrons);

	edm::Handle < reco::BeamSpot > bsHandle;
	iEvent.getByLabel(beamSpotInputTag, bsHandle);

	edm::Handle < reco::ConversionCollection > hConversions;
	iEvent.getByLabel(conversionsInputTag, hConversions);

	edm::Handle < reco::TrackCollection > tracks;
	iEvent.getByLabel(trkInputTag, tracks);

	edm::Handle < DcsStatusCollection > dcsHandle;
	iEvent.getByLabel(dcsInputTag, dcsHandle);

	edm::Handle < reco::VertexCollection > primaryVertices;
	iEvent.getByLabel(vtxInputTag, primaryVertices);

	std::vector < edm::Handle<edm::ValueMap<float> > > eIDValueMap(1);
	iEvent.getByLabel(likelihoodInputTag, eIDValueMap[0]);
	const edm::ValueMap<float> & eIDmapLikelihood = *eIDValueMap[0];

    if (electrons.isValid()) {
        edm::LogInfo("BristolNTuple_ElectronsExtraInfo") << "Total # Electrons: " << electrons->size();
        for (std::vector<pat::Electron>::const_iterator it = electrons->begin(); it != electrons->end(); ++it) {
            // exit from loop when you reach the required number of electrons
            if (px->size() >= maxSize)
                break;

            int passId = 0;

            /* passID for different electron IDs is assigned bitwise
             * https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCategoryBasedElectronID
             * bit 0: eidVeryLoose
             * bit 1: eidLoose
             * bit 2: eidMedium
             * bit 3: eidTight
             * bit 4: eidSuperTight
             * bit 5: eidHyperTight1
             * bit 6: eidHyperTight2
             * bit 7: eidHyperTight3
             * bit 8: eidHyperTight4
             */
            if (it->electronID("eidVeryLoose") > 0)   passId = passId | 1 << 0;
            if (it->electronID("eidLoose") > 0)       passId = passId | 1 << 1;
            if (it->electronID("eidMedium") > 0)      passId = passId | 1 << 2;
            if (it->electronID("eidTight") > 0)       passId = passId | 1 << 3;
            if (it->electronID("eidSuperTight") > 0)  passId = passId | 1 << 4;
            if (it->electronID("eidHyperTight1") > 0) passId = passId | 1 << 5;
            if (it->electronID("eidHyperTight2") > 0) passId = passId | 1 << 6;
            if (it->electronID("eidHyperTight3") > 0) passId = passId | 1 << 7;
            if (it->electronID("eidHyperTight4") > 0) passId = passId | 1 << 8;

            int passIdMC = 0;
            /* passID for different electron IDs is assigned bitwise
			 * https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideCategoryBasedElectronID
			 * bit 0: eidVeryLooseMC
			 * bit 1: eidLooseMC
			 * bit 2: eidMediumMC
			 * bit 3: eidTightMC
			 * bit 4: eidSuperTightMC
			 * bit 5: eidHyperTight1MC
			 * bit 6: eidHyperTight2MC
			 * bit 7: eidHyperTight3MC
			 * bit 8: eidHyperTight4MC
			 */
            if (it->electronID("eidVeryLooseMC") > 0) {
				passIdMC = passIdMC | 1 << 0;
				eidVeryLooseMC->push_back(true);
			} else
				eidVeryLooseMC->push_back(false);
			if (it->electronID("eidLooseMC") > 0) {
				passIdMC = passIdMC | 1 << 1;
				eidLooseMC->push_back(true);
			} else
				eidLooseMC->push_back(false);
			if (it->electronID("eidMediumMC") > 0) {
				passIdMC = passIdMC | 1 << 2;
				eidMediumMC->push_back(true);
			} else
				eidMediumMC->push_back(false);
			if (it->electronID("eidTightMC") > 0) {
				passIdMC = passIdMC | 1 << 3;
				eidTightMC->push_back(true);
			} else
				eidTightMC->push_back(false);
			if (it->electronID("eidSuperTightMC") > 0) {
				passIdMC = passIdMC | 1 << 4;
				eidSuperTightMC->push_back(true);
			} else
				eidSuperTightMC->push_back(false);
			if (it->electronID("eidHyperTight1MC") > 0) {
				passIdMC = passIdMC | 1 << 5;
				eidHyperTight1MC->push_back(true);
			} else
				eidHyperTight1MC->push_back(false);
			if (it->electronID("eidHyperTight2MC") > 0) {
				passIdMC = passIdMC | 1 << 6;
				eidHyperTight2MC->push_back(true);
			} else
				eidHyperTight2MC->push_back(false);
			if (it->electronID("eidHyperTight3MC") > 0) {
				passIdMC = passIdMC | 1 << 7;
				eidHyperTight3MC->push_back(true);
			} else
				eidHyperTight3MC->push_back(false);
			if (it->electronID("eidHyperTight4MC") > 0) {
				passIdMC = passIdMC | 1 << 8;
				eidHyperTight4MC->push_back(true);
			} else
				eidHyperTight4MC->push_back(false);



            /* Conversion (fit)
             * See https://indico.cern.ch/getFile.py/access?contribId=12&sessionId=0&resId=0&materialId=slides&confId=133587
             * and
             * https://hypernews.cern.ch/HyperNews/CMS/get/egamma/999.html ( N.1 )
             */
			bool matchesConv = false;
			if (hConversions.isValid() && bsHandle.isValid()) {
				matchesConv = ConversionTools::hasMatchedConversion(*it, hConversions, bsHandle->position());
			} else {
				if (!bsHandle.isValid())
					edm::LogError("RootTupleMakerV2_ElectronsError") << "Error! Can't get the product "
							<< beamSpotInputTag;
				if (!hConversions.isValid())
					edm::LogError("RootTupleMakerV2_ElectronsError") << "Error! Can't get the product "
							<< conversionsInputTag;
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

            // Likelihood Based Ele ID ( https://twiki.cern.ch/twiki/bin/view/CMS/LikelihoodBasedEleID2011 )
			double likelihood_ = -999.;
			if (eIDValueMap[0].isValid()) {
				likelihood_ = eIDmapLikelihood[it->originalObjectRef()];
			}

            //kinematic variables
            px->push_back(it->px());
            py->push_back(it->py());
            pz->push_back(it->pz());
            energy->push_back(it->energy());
            //extra properties
            charge->push_back(it->charge());



            // ID variables
            hadronicOverEM->push_back(it->hadronicOverEm());
            EseedOverPout->push_back(it->eSeedClusterOverPout());
            eSuperClusterOverP->push_back(it->eSuperClusterOverP());
            fbrem->push_back(it->fbrem());
            sigmaEtaEta->push_back(it->sigmaEtaEta());
            sigmaIEtaIEta->push_back(it->sigmaIetaIeta());
            deltaPhiTrkSC->push_back(it->deltaPhiSuperClusterTrackAtVtx());
            deltaEtaTrkSC->push_back(it->deltaEtaSuperClusterTrackAtVtx());
            passID->push_back( passId );
            passIDMC->push_back( passIdMC );
            likelihood->push_back(likelihood_);
            numberOfBrems->push_back( it->numberOfBrems() );

            //electron isolation variables
            trkIso03->push_back(it->dr03TkSumPt());
			ecalIso03->push_back(it->dr03EcalRecHitSumEt());
			hcalIso03->push_back(it->dr03HcalTowerSumEt());
			relIso03->push_back((it->dr03HcalTowerSumEt() + it->dr03EcalRecHitSumEt() + it->dr03TkSumPt()) / it->et());
			trkIso04->push_back(it->dr04TkSumPt());
			ecalIso04->push_back(it->dr04EcalRecHitSumEt());
			hcalIso04->push_back(it->dr04HcalTowerSumEt());
			relIso04->push_back((it->dr04HcalTowerSumEt() + it->dr04EcalRecHitSumEt() + it->dr04TkSumPt()) / it->et());

			//electron PF isolation variables
			if (storePFIsolation) {
				pat::IsolationKeys isokeyPfChargedHadronIso = pat::IsolationKeys(4);
				pat::IsolationKeys isokeyPfNeutralHadronIso = pat::IsolationKeys(5);
				pat::IsolationKeys isokeyPFGammaIso = pat::IsolationKeys(6);

				double pfRelIso03(0), pfRelIso04(0), pfRelIso05(0);

				const reco::IsoDeposit * PfChargedHadronIsolation = it->isoDeposit(isokeyPfChargedHadronIso);
				const reco::IsoDeposit * PfNeutralHadronIsolation = it->isoDeposit(isokeyPfNeutralHadronIso);
				const reco::IsoDeposit * PFGammaIsolation = it->isoDeposit(isokeyPFGammaIso);
				if (PfChargedHadronIsolation){
					PfChargedHadronIso03->push_back(PfChargedHadronIsolation->depositWithin(0.3));
					PfChargedHadronIso04->push_back(PfChargedHadronIsolation->depositWithin(0.4));
					PfChargedHadronIso05->push_back(PfChargedHadronIsolation->depositWithin(0.5));
					pfRelIso03 += PfChargedHadronIsolation->depositWithin(0.3);
					pfRelIso04 += PfChargedHadronIsolation->depositWithin(0.4);
					pfRelIso05 += PfChargedHadronIsolation->depositWithin(0.5);
				}
				else
					edm::LogError("BristolNTuple_ElectronsExtraError") << "Error! Can't get the isolation deposit "
							<< "PfChargedHadronIsolation";
				if (PfNeutralHadronIsolation){
					PfNeutralHadronIso03->push_back(PfNeutralHadronIsolation->depositWithin(0.3));
					PfNeutralHadronIso04->push_back(PfNeutralHadronIsolation->depositWithin(0.4));
					PfNeutralHadronIso05->push_back(PfNeutralHadronIsolation->depositWithin(0.5));
					pfRelIso03 += PfNeutralHadronIsolation->depositWithin(0.3);
					pfRelIso04 += PfNeutralHadronIsolation->depositWithin(0.4);
					pfRelIso05 += PfNeutralHadronIsolation->depositWithin(0.5);
				}

				else
					edm::LogError("BristolNTuple_ElectronsExtraError") << "Error! Can't get the isolation deposit "
							<< "PfNeutralHadronIsolation";
				if (PFGammaIsolation){
					PFGammaIso03->push_back(PFGammaIsolation->depositWithin(0.3));
					PFGammaIso04->push_back(PFGammaIsolation->depositWithin(0.4));
					PFGammaIso05->push_back(PFGammaIsolation->depositWithin(0.5));
					pfRelIso03 += PFGammaIsolation->depositWithin(0.3);
					pfRelIso04 += PFGammaIsolation->depositWithin(0.4);
					pfRelIso05 += PFGammaIsolation->depositWithin(0.5);
				}
				else
					edm::LogError("BristolNTuple_ElectronsExtraError") << "Error! Can't get the isolation deposit "
							<< "PFGammaIsolation";
				PFRelIso03->push_back(pfRelIso03/it->et());
				PFRelIso04->push_back(pfRelIso04/it->et());
				PFRelIso05->push_back(pfRelIso05/it->et());
			}

            // Iso variables (Heep)
            ecalIsoHeep03->push_back(it->dr03EcalRecHitSumEt());
            hcalIsoD1Heep03->push_back(it->dr03HcalDepth1TowerSumEt());
            hcalIsoD2Heep03->push_back(it->dr03HcalDepth2TowerSumEt());
            trkIsoHeep03->push_back(it->dr03TkSumPt());

            ecalIsoHeep04->push_back(it->dr04EcalRecHitSumEt());
			hcalIsoD1Heep04->push_back(it->dr04HcalDepth1TowerSumEt());
			hcalIsoD2Heep04->push_back(it->dr04HcalDepth2TowerSumEt());
			trkIsoHeep04->push_back(it->dr04TkSumPt());

            // Conversion variables
            missingHits->push_back(it->gsfTrack()->trackerExpectedHitsInner().numberOfHits());
            dist_vec->push_back(it->convDist());
            dCotTheta->push_back(it->convDcot());
            conversionRadius->push_back(it->convRadius());
            hasMatchedConvPhot->push_back( matchesConv );
            shFracInnerHits->push_back(it->shFracInnerHits());

            //associated track
            //            closestCtfTrackRef->push_back(static_cast<int> (it->closestCtfTrackRef().key()));
                        //            gsfTrackPt->push_back(it->gsfTrack()->pt());
            //            gsfTrackD0->push_back(it->gsfTrack()->d0());
            //            gsfTrackEta->push_back(it->gsfTrack()->eta());
            //            gsfTrackPhi->push_back(it->gsfTrack()->phi());
            //            gsfTrackTheta->push_back(it->gsfTrack()->theta());
            //            gsfTrackCharge->push_back(it->gsfTrack()->charge());

            // SC associated with electron
            scEta->push_back(it->superCluster()->eta());
            scPhi->push_back(it->superCluster()->phi());
            scPt->push_back(it->superCluster()->energy() / cosh(it->superCluster()->eta()));
            scRawEnergy->push_back(it->superCluster()->rawEnergy());

            // Vertex association variables
            vtxIndex->push_back(vtxIndex_);
     //       vtxDistXY->push_back(vtxDistXY_);
            vtxDistZ->push_back(vtxDistZ_);
            primaryVertexDXY->push_back(it->dB());
			primaryVertexDXYError->push_back(it->edB());
			beamSpotDXY->push_back(it->dB(pat::Electron::BS2D));
			beamSpotDXYError->push_back(it->edB(pat::Electron::BS2D));
//            VertexX->push_back(it->vertex().x());
//            VertexY->push_back(it->vertex().y());
//            VertexZ->push_back(it->vertex().z());



        }
    } else {
        edm::LogError("BristolNTuple_ElectronsExtraError") << "Error! Can't get the product " << inputTag;
    }


    //-----------------------------------------------------------------
    // put vectors in the event
    //kinematic variables
    iEvent.put(px, prefix + "Px" + suffix);
    iEvent.put(py, prefix + "Py" + suffix);
    iEvent.put(pz, prefix + "Pz" + suffix);
    iEvent.put(energy, prefix + "Energy" + suffix);
    //extra properties
    iEvent.put(charge, prefix + "Charge" + suffix);

    //electron ID variables
    iEvent.put(hadronicOverEM, prefix + "HadronicOverEM" + suffix);
    iEvent.put(EseedOverPout, prefix + "eSeedClusterOverPout" + suffix );
    iEvent.put(eSuperClusterOverP, prefix + "ESuperClusterOverP" + suffix);
    iEvent.put(fbrem, prefix + "Fbrem" + suffix);
    iEvent.put(sigmaEtaEta, prefix + "SigmaEtaEta" + suffix);
    iEvent.put(sigmaIEtaIEta, prefix + "SigmaIEtaIEta" + suffix);
    iEvent.put(deltaPhiTrkSC, prefix + "DeltaPhiTrkSC" + suffix);
    iEvent.put(deltaEtaTrkSC, prefix + "DeltaEtaTrkSC" + suffix);
    iEvent.put( passID, prefix + "PassID" + suffix );
    iEvent.put( passIDMC, prefix + "PassIDMC" + suffix );
    iEvent.put( eidVeryLooseMC, prefix + "eidVeryLooseMC" + suffix );
    iEvent.put( eidLooseMC, prefix + "eidLooseMC" + suffix );
    iEvent.put( eidMediumMC, prefix + "eidMediumMC" + suffix );
    iEvent.put( eidTightMC, prefix + "eidTightMC" + suffix );
    iEvent.put( eidSuperTightMC, prefix + "eidSuperTightMC" + suffix );
    iEvent.put( eidHyperTight1MC, prefix + "eidHyperTight1MC" + suffix );
    iEvent.put( eidHyperTight2MC, prefix + "eidHyperTight2MC" + suffix );
    iEvent.put( eidHyperTight3MC, prefix + "eidHyperTight3MC" + suffix );
    iEvent.put( eidHyperTight4MC, prefix + "eidHyperTight4MC" + suffix );
    iEvent.put( likelihood, prefix + "Likelihood" + suffix );
    iEvent.put( numberOfBrems, prefix + "NumberOfBrems" + suffix );

    //electron isolation variables
    iEvent.put(trkIso04, prefix + "TrkIso04" + suffix);
    iEvent.put(ecalIso04, prefix + "EcalIso04" + suffix);
    iEvent.put(hcalIso04, prefix + "HcalIso04" + suffix);
    iEvent.put(relIso04, prefix + "RelIso04" + suffix);

    iEvent.put(trkIso03, prefix + "TrkIso03" + suffix);
    iEvent.put(ecalIso03, prefix + "EcalIso03" + suffix);
    iEvent.put(hcalIso03, prefix + "HcalIso03" + suffix);
    iEvent.put(relIso03, prefix + "RelIso03" + suffix);

    //electron PF isolation variables
    if (storePFIsolation) {
		iEvent.put(PfChargedHadronIso03, prefix + "PfChargedHadronIso03" + suffix);
		iEvent.put(PfNeutralHadronIso03, prefix + "PfNeutralHadronIso03" + suffix);
		iEvent.put(PFGammaIso03, prefix + "PFGammaIso03" + suffix);
		iEvent.put(PFRelIso03, prefix + "PFRelIso03" + suffix);

		iEvent.put(PfChargedHadronIso04, prefix + "PfChargedHadronIso04" + suffix);
		iEvent.put(PfNeutralHadronIso04, prefix + "PfNeutralHadronIso04" + suffix);
		iEvent.put(PFGammaIso04, prefix + "PFGammaIso04" + suffix);
		iEvent.put(PFRelIso04, prefix + "PFRelIso04" + suffix);

		iEvent.put(PfChargedHadronIso05, prefix + "PfChargedHadronIso05" + suffix);
		iEvent.put(PfNeutralHadronIso05, prefix + "PfNeutralHadronIso05" + suffix);
		iEvent.put(PFGammaIso05, prefix + "PFGammaIso05" + suffix);
		iEvent.put(PFRelIso05, prefix + "PFRelIso05" + suffix);
	}

    //high energy electron isolation variables
    iEvent.put(ecalIsoHeep03, prefix + "EcalIsoHeep03" + suffix);
    iEvent.put(hcalIsoD1Heep03, prefix + "HcalIsoD1Heep03" + suffix);
    iEvent.put(hcalIsoD2Heep03, prefix + "HcalIsoD2Heep03" + suffix);
    iEvent.put(trkIsoHeep03, prefix + "TrkIsoHeep03" + suffix);

    iEvent.put(ecalIsoHeep04, prefix + "EcalIsoHeep04" + suffix);
	iEvent.put(hcalIsoD1Heep04, prefix + "HcalIsoD1Heep04" + suffix);
	iEvent.put(hcalIsoD2Heep04, prefix + "HcalIsoD2Heep04" + suffix);
	iEvent.put(trkIsoHeep04, prefix + "TrkIsoHeep04" + suffix);

	//electron conversion identification variables
    iEvent.put(missingHits, prefix + "MissingHits" + suffix);
    iEvent.put(dist_vec, prefix + "Dist" + suffix);
    iEvent.put(dCotTheta, prefix + "DCotTheta" + suffix);
    iEvent.put(conversionRadius, prefix + "ConvRadius" + suffix);
    iEvent.put(hasMatchedConvPhot, prefix + "HasMatchedConvPhot" + suffix);
    iEvent.put(shFracInnerHits, prefix + "shFracInnerHits" + suffix);

    //associated track
//	iEvent.put(gsfTrackPt, prefix + "GSFTrack.Pt" + suffix);
//	iEvent.put(gsfTrackD0, prefix + "GSFTrack.d0" + suffix);
//	iEvent.put(gsfTrackEta, prefix + "GSFTrack.Eta" + suffix);
//	iEvent.put(gsfTrackPhi, prefix + "GSFTrack.Phi" + suffix);
//	iEvent.put(gsfTrackTheta, prefix + "GSFTrack.Theta" + suffix);
//	iEvent.put(gsfTrackCharge, prefix + "GSFTrack.Charge" + suffix);
//    iEvent.put(closestCtfTrackRef, prefix + "closestCtfTrackRef" + suffix);

    //calorimeter variables
    iEvent.put(scEta, prefix + "SCEta" + suffix);
    iEvent.put(scPhi, prefix + "SCPhi" + suffix);
    iEvent.put(scPt, prefix + "SCPt" + suffix);
    iEvent.put(scRawEnergy, prefix + "SCRawEnergy" + suffix);

    //calorimeter variables
    iEvent.put(vtxIndex, prefix + "VtxIndex" + suffix);
	iEvent.put(vtxDistZ, prefix + "VtxDistZ" + suffix);
	iEvent.put(primaryVertexDXY, prefix + "PrimaryVertexDXY" + suffix);
	iEvent.put(primaryVertexDXYError, prefix + "PrimaryVertexDXYError" + suffix);
	iEvent.put(beamSpotDXY, prefix + "BeamSpotDXY" + suffix);
	iEvent.put(beamSpotDXYError, prefix + "BeamSpotDXYError" + suffix);

//    iEvent.put(VertexX, prefix + "Vertex.X" + suffix);
	//    iEvent.put(VertexY, prefix + "Vertex.Y" + suffix);
	//    iEvent.put(VertexZ, prefix + "Vertex.Z" + suffix);

}

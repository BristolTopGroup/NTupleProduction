#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Electrons.h"
#include "BristolAnalysis/NTupleTools/interface/DirectionalIsolation.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"
#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"

BristolNTuple_Electrons::BristolNTuple_Electrons(const edm::ParameterSet& iConfig) :
  		inputTag(consumes<edm::View<pat::Electron>>(iConfig.getParameter<edm::InputTag>("InputTag"))),			
		prefix(iConfig.getParameter < std::string > ("Prefix")), //
		suffix(iConfig.getParameter < std::string > ("Suffix")), //
		maxSize(iConfig.getParameter<unsigned int>("MaxSize")), //
		storePFIsolation_(iConfig.getParameter<bool>("storePFIsolation")), //
		debugRelease_(iConfig.getParameter<bool>("debugRelease")), //
		vtxInputTag(consumes<std::vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("VertexInputTag"))), //		
		beamSpotInputTag(consumes<reco::BeamSpot>(iConfig.getParameter<edm::InputTag>("BeamSpotInputTag"))), //
		conversionsInputTag(consumes<std::vector<reco::Conversion>>(iConfig.getParameter<edm::InputTag>("ConversionsInputTag"))), // 		
  		tightElectronIDMapToken_(consumes<edm::ValueMap<bool> >(iConfig.getParameter<edm::InputTag>("tightElectronIDMap"))), //
  		tightElectronIDMapToken_bitmap_(consumes<edm::ValueMap<unsigned int> >(iConfig.getParameter<edm::InputTag>("tightElectronIDMap_bitmap"))) //
{

	//kinematic variables
	produces < std::vector<double> > (prefix + "Px" + suffix);
	produces < std::vector<double> > (prefix + "Py" + suffix);
	produces < std::vector<double> > (prefix + "Pz" + suffix);
	produces < std::vector<double> > (prefix + "Energy" + suffix);
	//extra properties
	produces < std::vector<int> > (prefix + "Charge" + suffix);
	produces < std::vector<double> > (prefix + "ecalDrivenMomentum.Px" + suffix);
	produces < std::vector<double> > (prefix + "ecalDrivenMomentum.Py" + suffix);
	produces < std::vector<double> > (prefix + "ecalDrivenMomentum.Pz" + suffix);

	//electron ID variables
	produces < std::vector<double> > (prefix + "HadronicOverEM" + suffix);
	produces < std::vector<double> > (prefix + "eSeedClusterOverPout" + suffix);
	produces < std::vector<double> > (prefix + "ESuperClusterOverP" + suffix);
	produces < std::vector<double> > (prefix + "Fbrem" + suffix);
	produces < std::vector<double> > (prefix + "SigmaEtaEta" + suffix);
	produces < std::vector<double> > (prefix + "SigmaIEtaIEta" + suffix);
	produces < std::vector<double> > (prefix + "DeltaPhiTrkSC" + suffix);
	produces < std::vector<double> > (prefix + "DeltaEtaTrkSC" + suffix);
	produces < std::vector<int> > (prefix + "NumberOfBrems" + suffix);
	produces < std::vector<double> > (prefix + "mvaTrigV0" + suffix);
	produces < std::vector<double> > (prefix + "mvaNonTrigV0" + suffix);

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
	if (storePFIsolation_) {
		produces < std::vector<double> > (prefix + "PFRelIso03" + suffix);

		produces < std::vector<double> > (prefix + "PFRelIso04" + suffix);
		
		//new variable for pf delta beta corrected reliso
		produces < std::vector<double> > (prefix + "sumChargedHadronPt03" + suffix);
		produces < std::vector<double> > (prefix + "sumChargedHadronPt04" + suffix);
		produces < std::vector<double> > (prefix + "sumNeutralHadronPt03" + suffix);
		produces < std::vector<double> > (prefix + "sumNeutralHadronPt04" + suffix);
		produces < std::vector<double> > (prefix + "sumPhotonPt03" + suffix);
		produces < std::vector<double> > (prefix + "sumPhotonPt04" + suffix);
		produces < std::vector<double> > (prefix + "sumPUPt03" + suffix);
		produces < std::vector<double> > (prefix + "sumPUPt04" + suffix);
		
		produces < std::vector<double> > (prefix + "PFRelIso03DeltaBeta" + suffix);
		produces < std::vector<double> > (prefix + "PFRelIso04DeltaBeta" + suffix);
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

	produces < std::vector<bool> > (prefix + "isTightElectron" + suffix);
	produces < std::vector<bool> > (prefix + "isTightNonIsoElectron" + suffix);
	produces < std::vector<bool> > (prefix + "isTightConversionElectron" + suffix);

	//electron conversion identification variables
	produces < std::vector<double> > (prefix + "Dist" + suffix);
	produces < std::vector<double> > (prefix + "DCotTheta" + suffix);
	produces < std::vector<double> > (prefix + "ConvRadius" + suffix);
	produces < std::vector<int> > (prefix + "MissingHits" + suffix);
	//this might be identical to passConversionVeto
	produces < std::vector<bool> > (prefix + "HasMatchedConvPhot" + suffix);
	produces < std::vector<double> > (prefix + "shFracInnerHits" + suffix);
	produces < std::vector<bool> > (prefix + "passConversionVeto" + suffix);

	//calorimeter variables
	produces < std::vector<double> > (prefix + "SCEta" + suffix);
	produces < std::vector<double> > (prefix + "SCPhi" + suffix);
	produces < std::vector<double> > (prefix + "SCPt" + suffix);
	produces < std::vector<double> > (prefix + "SCP" + suffix);
	produces < std::vector<double> > (prefix + "SCEnergy" + suffix);
	produces < std::vector<double> > (prefix + "SCRawEnergy" + suffix);

	//electron vertex variables
	produces < std::vector<int> > (prefix + "VtxIndex" + suffix);
	produces < std::vector<double> > (prefix + "VtxDistZ" + suffix);
	produces < std::vector<double> > (prefix + "PrimaryVertexDXY" + suffix); //2D impact parameter, XY distance to vertex
	produces < std::vector<double> > (prefix + "PrimaryVertexDXYError" + suffix);
	produces < std::vector<double> > (prefix + "BeamSpotDXY" + suffix);
	produces < std::vector<double> > (prefix + "BeamSpotDXYError" + suffix);
	//quantities corrected for position of primary vertex
	produces < std::vector<double> > (prefix + "PrimaryVertexDXYCorr" + suffix);
	produces < std::vector<double> > (prefix + "VtxDistZCorr" + suffix);
}

void BristolNTuple_Electrons::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	//kinematic variables
	std::auto_ptr < std::vector<double> > px(new std::vector<double>());
	std::auto_ptr < std::vector<double> > py(new std::vector<double>());
	std::auto_ptr < std::vector<double> > pz(new std::vector<double>());
	std::auto_ptr < std::vector<double> > energy(new std::vector<double>());
	//extra properties
	std::auto_ptr < std::vector<int> > charge(new std::vector<int>());
	std::auto_ptr < std::vector<double> > ecalDrivenMomentumPx(new std::vector<double>());
	std::auto_ptr < std::vector<double> > ecalDrivenMomentumPy(new std::vector<double>());
	std::auto_ptr < std::vector<double> > ecalDrivenMomentumPz(new std::vector<double>());
	//electron ID variables
	std::auto_ptr < std::vector<double> > hadronicOverEM(new std::vector<double>());
	std::auto_ptr < std::vector<double> > EseedOverPout(new std::vector<double>());
	std::auto_ptr < std::vector<double> > eSuperClusterOverP(new std::vector<double>());
	std::auto_ptr < std::vector<double> > fbrem(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sigmaEtaEta(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sigmaIEtaIEta(new std::vector<double>());
	std::auto_ptr < std::vector<double> > deltaPhiTrkSC(new std::vector<double>());
	std::auto_ptr < std::vector<double> > deltaEtaTrkSC(new std::vector<double>());
	std::auto_ptr < std::vector<int> > numberOfBrems(new std::vector<int>());
	std::auto_ptr < std::vector<double> > mvaTrigV0(new std::vector<double>());
	std::auto_ptr < std::vector<double> > mvaNonTrigV0(new std::vector<double>());

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

	
	//muonn PF isolation variables
	std::auto_ptr < std::vector<double> > PFRelIso03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFRelIso04(new std::vector<double>());
	
	//new iso vars
	std::auto_ptr < std::vector<double> > sumChargedHadronPt03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumChargedHadronPt04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumNeutralHadronPt03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumNeutralHadronPt04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumPhotonPt03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumPhotonPt04(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumPUPt03(new std::vector<double>());
	std::auto_ptr < std::vector<double> > sumPUPt04(new std::vector<double>());
	
	std::auto_ptr < std::vector<double> > PFRelIso03DeltaBeta(new std::vector<double>());
	std::auto_ptr < std::vector<double> > PFRelIso04DeltaBeta(new std::vector<double>());

//    std::auto_ptr < std::vector<double> > dB(new std::vector<double>());

	// Electron ID variables
	std::auto_ptr < std::vector<bool> > isTightElectron(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > isTightConversionElectron(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > isTightNonIsoElectron(new std::vector<bool>());

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
	std::auto_ptr < std::vector<bool> > passConversionVeto(new std::vector<bool>());

	//calorimeter variables
	std::auto_ptr < std::vector<double> > scEta(new std::vector<double>());
	std::auto_ptr < std::vector<double> > scPhi(new std::vector<double>());
	std::auto_ptr < std::vector<double> > scPt(new std::vector<double>());
	std::auto_ptr < std::vector<double> > scP(new std::vector<double>());
	std::auto_ptr < std::vector<double> > scEnergy(new std::vector<double>());
	std::auto_ptr < std::vector<double> > scRawEnergy(new std::vector<double>());

	//electron vertex variables
	std::auto_ptr < std::vector<int> > vtxIndex(new std::vector<int>());
	std::auto_ptr < std::vector<double> > vtxDistZ(new std::vector<double>());
	std::auto_ptr < std::vector<double> > primaryVertexDXY(new std::vector<double>());
	std::auto_ptr < std::vector<double> > primaryVertexDXYError(new std::vector<double>());
	std::auto_ptr < std::vector<double> > beamSpotDXY(new std::vector<double>());
	std::auto_ptr < std::vector<double> > beamSpotDXYError(new std::vector<double>());
	std::auto_ptr < std::vector<double> > vtxDistZCorr(new std::vector<double>());
	std::auto_ptr < std::vector<double> > primaryVertexDXYCorr(new std::vector<double>());

	//-----------------------------------------------------------------

    edm::Handle<edm::View<pat::Electron> > electrons;
    iEvent.getByToken(inputTag,electrons);

	edm::Handle< reco::BeamSpot > bsHandle;
	iEvent.getByToken(beamSpotInputTag, bsHandle);

	edm::Handle< std::vector< reco::Conversion > > hConversions;
	iEvent.getByToken(conversionsInputTag, hConversions);

	edm::Handle< std::vector< reco::Vertex > > primaryVertices;
	iEvent.getByToken(vtxInputTag, primaryVertices);

	edm::Handle<edm::ValueMap<bool> > tight_id_decisions;
	iEvent.getByToken(tightElectronIDMapToken_,tight_id_decisions);
	tightElectronIDDecisions_ = *tight_id_decisions;

	edm::Handle<edm::ValueMap<unsigned int> > tight_id_decisions_bitmap;
	iEvent.getByToken(tightElectronIDMapToken_bitmap_,tight_id_decisions_bitmap);
	tightElectronIDDecisions_bitmap_ = *tight_id_decisions_bitmap;

	if (electrons.isValid()) {

		edm::LogInfo("BristolNTuple_ElectronsExtraInfo") << "Total # Electrons: " << electrons->size();

		for (size_t index = 0; index < electrons->size(); ++index){
			const auto it = electrons->ptrAt(index);

			// exit from loop when you reach the required number of electrons (99)
			if (px->size() >= maxSize) break;

			// Check ID
			isTightElectron->push_back( tightElectronIDDecisions_[it] );

			if ( tightElectronIDDecisions_bitmap_[it] == 3327 || tightElectronIDDecisions_bitmap_[it] == 3583 || tightElectronIDDecisions_bitmap_[it] == 3839) {
				isTightNonIsoElectron->push_back( true );
			}
			else {
				isTightNonIsoElectron->push_back( false );
			}

			if ( tightElectronIDDecisions_bitmap_[it] == 1023 || tightElectronIDDecisions_bitmap_[it] == 2047 || tightElectronIDDecisions_bitmap_[it] == 3071) {
				isTightConversionElectron->push_back( true );
			}
			else {
				isTightConversionElectron->push_back( false );
			}

			/* Conversion (fit)
			 * See https://indico.cern.ch/getFile.py/access?contribId=12&sessionId=0&resId=0&materialId=slides&confId=133587
			 * and
			 * https://hypernews.cern.ch/HyperNews/CMS/get/egamma/999.html ( N.1 )
			 */
			bool matchesConv = false;
			if (hConversions.isValid() && bsHandle.isValid()) {
				matchesConv = ConversionTools::hasMatchedConversion(*it, hConversions, bsHandle->position());
			} 
			// else {
			// 	if (!bsHandle.isValid())
			// 		edm::LogError("RootTupleMakerV2_ElectronsError") << "Error! Can't get the product "
			// 				<< beamSpotInputTag;
			// 	if (!hConversions.isValid())
			// 		edm::LogError("RootTupleMakerV2_ElectronsError") << "Error! Can't get the product "
			// 				<< conversionsInputTag;
			// }
			// Vertex association
			double minVtxDist3D = 9999.;
			int vtxIndex_ = -1;
//			double vtxDistXY_ = -9999.;
			double vtxDistZ_ = -9999.;
			double vtxDistXY_Corr = -9999.;
			double vtxDistZ_Corr = -9999.;

			if (primaryVertices.isValid()) {
				edm::LogInfo("RootTupleMakerV2_ElectronsInfo") << "Total # Primary Vertices: "
						<< primaryVertices->size();
				reco::Vertex pv = primaryVertices->front();
				vtxDistXY_Corr = it->gsfTrack()->d0() - pv.x() * sin(it->gsfTrack()->phi())
						+ pv.y() * cos(it->gsfTrack()->phi());
				vtxDistZ_Corr = (it->vz() - pv.z())
						- ((it->vx() - pv.x()) * it->px() + (it->vy() - pv.y()) * it->py()) / it->pt() / it->pt()
								* it->pz();

				for (reco::VertexCollection::const_iterator v_it = primaryVertices->begin();
						v_it != primaryVertices->end(); ++v_it) {

					double distXY = it->gsfTrack()->dxy(v_it->position());
					double distZ = it->gsfTrack()->dz(v_it->position());
					double dist3D = sqrt(pow(distXY, 2) + pow(distZ, 2));

					if (dist3D < minVtxDist3D) {
						minVtxDist3D = dist3D;
						vtxIndex_ = int(std::distance(primaryVertices->begin(), v_it));
//						vtxDistXY_ = distXY;
						vtxDistZ_ = distZ;
					}
				}
			}
// 			} else {
// 				edm::LogError("RootTupleMakerV2_ElectronsError") << "Error! Can't get the product " << vtxInputTag;
// 			}

			//kinematic variables
			px->push_back(it->px());
			py->push_back(it->py());
			pz->push_back(it->pz());
			energy->push_back(it->energy());
			//extra properties
			charge->push_back(it->charge());
			ecalDrivenMomentumPx->push_back(it->ecalDrivenMomentum().Px());
			ecalDrivenMomentumPy->push_back(it->ecalDrivenMomentum().Py());
			ecalDrivenMomentumPz->push_back(it->ecalDrivenMomentum().Pz());
			// ID variables
			hadronicOverEM->push_back(it->hadronicOverEm());
			EseedOverPout->push_back(it->eSeedClusterOverPout());
			eSuperClusterOverP->push_back(it->eSuperClusterOverP());
			fbrem->push_back(it->fbrem());
			sigmaEtaEta->push_back(it->sigmaEtaEta());
			sigmaIEtaIEta->push_back(it->sigmaIetaIeta());
			deltaPhiTrkSC->push_back(it->deltaPhiSuperClusterTrackAtVtx());
			deltaEtaTrkSC->push_back(it->deltaEtaSuperClusterTrackAtVtx());
			numberOfBrems->push_back(it->numberOfBrems());

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
			if (storePFIsolation_) {

				reco::GsfElectron::PflowIsolationVariables pfIso = it->pfIsolationVariables();

				sumChargedHadronPt03->push_back(pfIso.sumChargedHadronPt);
				sumChargedHadronPt04->push_back(0);
			
				sumNeutralHadronPt03->push_back(pfIso.sumNeutralHadronEt);
				sumNeutralHadronPt04->push_back(0);

				sumPhotonPt03->push_back(pfIso.sumPhotonEt);
				sumPhotonPt04->push_back(0);

				sumPUPt03->push_back(pfIso.sumPUPt);
				sumPUPt04->push_back(0);
				
				// 3rd and 4th arguments for rho isolation
				PFRelIso03->push_back(( pfIso.sumChargedHadronPt + pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt ) / it->pt());
				PFRelIso04->push_back(0);

				PFRelIso03DeltaBeta->push_back(( pfIso.sumChargedHadronPt 
				  + std::max(0.0 , pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - 0.5 * pfIso.sumPUPt ) ) / it->pt());
				PFRelIso04DeltaBeta->push_back(0);
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
			// missingHits->push_back(it->gsfTrack()->numberOfLostTrackerHits(HitPattern::MISSING_INNER_HITS));
			missingHits->push_back(0);
			dist_vec->push_back(it->convDist());
			dCotTheta->push_back(it->convDcot());
			conversionRadius->push_back(it->convRadius());
			hasMatchedConvPhot->push_back(matchesConv);
			shFracInnerHits->push_back(it->shFracInnerHits());
//			bool passesConversionVeto = !ConversionTools::hasMatchedConversion(it,hConversions,beamspot.position());
			passConversionVeto->push_back(it->passConversionVeto());

			// SC associated with electron
			scEta->push_back(it->superCluster()->eta());
			scPhi->push_back(it->superCluster()->phi());
			scPt->push_back(it->superCluster()->energy() / cosh(it->superCluster()->eta()));
			scP->push_back(it->eSuperClusterOverP() / it->superCluster()->energy());
			scEnergy->push_back(it->superCluster()->energy());
			scRawEnergy->push_back(it->superCluster()->rawEnergy());

			// Vertex association variables
			vtxIndex->push_back(vtxIndex_);
			vtxDistZ->push_back(vtxDistZ_);
			primaryVertexDXY->push_back(it->dB());
			primaryVertexDXYError->push_back(it->edB());
			beamSpotDXY->push_back(it->dB(pat::Electron::BS2D));
			beamSpotDXYError->push_back(it->edB(pat::Electron::BS2D));
			vtxDistZCorr->push_back(vtxDistZ_Corr);
			primaryVertexDXYCorr->push_back(vtxDistXY_Corr);

		}
	}
	// } else {
	// 	edm::LogError("BristolNTuple_ElectronsExtraError") << "Error! Can't get the product " << inputTag;
	// }

	//-----------------------------------------------------------------
	// put vectors in the event
	//kinematic variables
	iEvent.put(px, prefix + "Px" + suffix);
	iEvent.put(py, prefix + "Py" + suffix);
	iEvent.put(pz, prefix + "Pz" + suffix);
	iEvent.put(energy, prefix + "Energy" + suffix);
	//extra properties
	iEvent.put(charge, prefix + "Charge" + suffix);
	iEvent.put(ecalDrivenMomentumPx, prefix + "ecalDrivenMomentum.Px" + suffix);
	iEvent.put(ecalDrivenMomentumPy, prefix + "ecalDrivenMomentum.Py" + suffix);
	iEvent.put(ecalDrivenMomentumPz, prefix + "ecalDrivenMomentum.Pz" + suffix);
	//electron ID variables
	iEvent.put(hadronicOverEM, prefix + "HadronicOverEM" + suffix);
	iEvent.put(EseedOverPout, prefix + "eSeedClusterOverPout" + suffix);
	iEvent.put(eSuperClusterOverP, prefix + "ESuperClusterOverP" + suffix);
	iEvent.put(fbrem, prefix + "Fbrem" + suffix);
	iEvent.put(sigmaEtaEta, prefix + "SigmaEtaEta" + suffix);
	iEvent.put(sigmaIEtaIEta, prefix + "SigmaIEtaIEta" + suffix);
	iEvent.put(deltaPhiTrkSC, prefix + "DeltaPhiTrkSC" + suffix);
	iEvent.put(deltaEtaTrkSC, prefix + "DeltaEtaTrkSC" + suffix);
	iEvent.put(numberOfBrems, prefix + "NumberOfBrems" + suffix);
	iEvent.put(mvaTrigV0, prefix + "mvaTrigV0" + suffix);
	iEvent.put(mvaNonTrigV0, prefix + "mvaNonTrigV0" + suffix);

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
	if (storePFIsolation_) {
		iEvent.put(PFRelIso03, prefix + "PFRelIso03" + suffix);
		iEvent.put(PFRelIso04, prefix + "PFRelIso04" + suffix);
		
		iEvent.put(sumChargedHadronPt03, prefix + "sumChargedHadronPt03" + suffix);
		iEvent.put(sumChargedHadronPt04, prefix + "sumChargedHadronPt04" + suffix);
		iEvent.put(sumNeutralHadronPt03, prefix + "sumNeutralHadronPt03" + suffix);
		iEvent.put(sumNeutralHadronPt04, prefix + "sumNeutralHadronPt04" + suffix);
		iEvent.put(sumPhotonPt03, prefix + "sumPhotonPt03" + suffix);
		iEvent.put(sumPhotonPt04, prefix + "sumPhotonPt04" + suffix);
		iEvent.put(sumPUPt03, prefix + "sumPUPt03" + suffix);
		iEvent.put(sumPUPt04, prefix + "sumPUPt04" + suffix);
		
		iEvent.put(PFRelIso03DeltaBeta, prefix + "PFRelIso03DeltaBeta" + suffix);
		iEvent.put(PFRelIso04DeltaBeta, prefix + "PFRelIso04DeltaBeta" + suffix);
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

	iEvent.put(isTightElectron, prefix + "isTightElectron" + suffix);
	iEvent.put(isTightNonIsoElectron, prefix + "isTightNonIsoElectron" + suffix);
	iEvent.put(isTightConversionElectron, prefix + "isTightConversionElectron" + suffix);

	//electron conversion identification variables
	iEvent.put(missingHits, prefix + "MissingHits" + suffix);
	iEvent.put(dist_vec, prefix + "Dist" + suffix);
	iEvent.put(dCotTheta, prefix + "DCotTheta" + suffix);
	iEvent.put(conversionRadius, prefix + "ConvRadius" + suffix);
	iEvent.put(hasMatchedConvPhot, prefix + "HasMatchedConvPhot" + suffix);
	iEvent.put(shFracInnerHits, prefix + "shFracInnerHits" + suffix);
	iEvent.put(passConversionVeto, prefix + "passConversionVeto" + suffix);

	//calorimeter variables
	iEvent.put(scEta, prefix + "SCEta" + suffix);
	iEvent.put(scPhi, prefix + "SCPhi" + suffix);
	iEvent.put(scPt, prefix + "SCPt" + suffix);
	iEvent.put(scP, prefix + "SCP" + suffix);
	iEvent.put(scEnergy, prefix + "SCEnergy" + suffix);
	iEvent.put(scRawEnergy, prefix + "SCRawEnergy" + suffix);

	//calorimeter variables
	iEvent.put(vtxIndex, prefix + "VtxIndex" + suffix);
	iEvent.put(vtxDistZ, prefix + "VtxDistZ" + suffix);
	iEvent.put(primaryVertexDXY, prefix + "PrimaryVertexDXY" + suffix);
	iEvent.put(primaryVertexDXYError, prefix + "PrimaryVertexDXYError" + suffix);
	iEvent.put(beamSpotDXY, prefix + "BeamSpotDXY" + suffix);
	iEvent.put(beamSpotDXYError, prefix + "BeamSpotDXYError" + suffix);
	iEvent.put(vtxDistZCorr, prefix + "VtxDistZCorr" + suffix);
	iEvent.put(primaryVertexDXYCorr, prefix + "PrimaryVertexDXYCorr" + suffix);

}









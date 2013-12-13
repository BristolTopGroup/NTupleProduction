#crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/DYJetsToLL_TuneZ2_M-50_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg
#for i in `seq 1 10`;
#do
#crab -submit 500 -c DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
#done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/GJets_TuneZ2_HT-40To100_7TeV_madgraph_Fall11_LeptonPlus3JetsSkim.cfg
for i in `seq 1 10`;
do
crab -submit 500 -c GJets_TuneZ2_40_HT_100_7TeV-madgraph_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/GJets_TuneZ2_HT-100To200_7TeV_madgraph_Fall11_LeptonPlus3JetsSkim.cfg &> gjets_100to200.log
for i in `seq 1 10`;
do
crab -submit 500 -c GJets_TuneZ2_100_HT_200_7TeV-madgraph_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/GJets_TuneZ2_HT-200_7TeV_madgraph_Fall11_LeptonPlus3JetsSkim.cfg &> gjets_200.log
for i in `seq 1 10`;
do
crab -submit 500 -c GJets_TuneZ2_200_HT_inf_7TeV-madgraph_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/QCD_20to30_BCtoE_TuneZ2_7TeV_pythia6_Fall11_LeptonPlus3JetsSkim.cfg &> qcd_20to30_bcetoe.log
for i in `seq 1 10`;
do
crab -submit 500 -c QCD_Pt-20to30_BCtoE_TuneZ2_7TeV-pythia6_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/QCD_20to30_EMEnriched_TuneZ2_7TeV_pythia6_Fall11_LeptonPlus3JetsSkim.cfg &> qcd_20to30_EM.log
for i in `seq 1 10`;
do
crab -submit 500 -c QCD_Pt-20to30_EMEnriched_TuneZ2_7TeV-pythia6_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/QCD_30to80_BCtoE_TuneZ2_7TeV_pythia6_Fall11_LeptonPlus3JetsSkim.cfg &> qcd_30to70_bcetoe.log
for i in `seq 1 10`;
do
crab -submit 500 -c QCD_Pt-30to80_BCtoE_TuneZ2_7TeV-pythia6_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/QCD_30to80_EMEnriched_TuneZ2_7TeV_pythia6_Fall11_LeptonPlus3JetsSkim.cfg &> qcd_30to80_EM.log
for i in `seq 1 10`;
do
crab -submit 500 -c QCD_Pt-30to80_EMEnriched_TuneZ2_7TeV-pythia6_Fall11-PU_S6_START44_V5-v1_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/QCD_80to170_BCtoE_TuneZ2_7TeV_pythia6_Fall11_LeptonPlus3JetsSkim.cfg &> qcd_80to170_bcetoe.log
for i in `seq 1 10`;
do
crab -submit 500 -c QCD_Pt-80to170_BCtoE_TuneZ2_7TeV-pythia6_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/QCD_80to170_EMEnriched_TuneZ2_7TeV_pythia6_Fall11_LeptonPlus3JetsSkim.cfg &> qcd_80to170_EM.log
for i in `seq 1 10`;
do
crab -submit 500 -c QCD_Pt-80to170_EMEnriched_TuneZ2_7TeV-pythia6_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV_pythia6_Fall11_LeptonPlus3JetsSkim.cfg &> qcd_mu.log
for i in `seq 1 10`;
do
crab -submit 500 -c QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/T_TuneZ2_s-channel_7TeV_powheg-tauola_Fall11_LeptonPlus3JetsSkim.cfg &> singleT_s.log
for i in `seq 1 10`;
do
crab -submit 500 -c T_TuneZ2_s-channel_7TeV-powheg-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/T_TuneZ2_t-channel_7TeV_-powheg-tauola_Fall11_LeptonPlus3JetsSkim.cfg &> singleT_t.log
for i in `seq 1 10`;
do
crab -submit 500 -c T_TuneZ2_t-channel_7TeV-powheg-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola_Fall11_LeptonPlus3JetsSkim.cfg &> singleT_tW.log
for i in `seq 1 10`;
do
crab -submit 500 -c T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/Tbar_TuneZ2_s-channel_7TeV_powheg-tauola_Fall11_LeptonPlus3JetsSkim.cfg &> singleTbar_s.log
for i in `seq 1 10`;
do
crab -submit 500 -c Tbar_TuneZ2_s-channel_7TeV-powheg-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/Tbar_TuneZ2_t-channel_7TeV_-powheg-tauola_Fall11_LeptonPlus3JetsSkim.cfg &> singleTbar_t.log
for i in `seq 1 10`;
do
crab -submit 500 -c Tbar_TuneZ2_t-channel_7TeV-powheg-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola_Fall11_LeptonPlus3JetsSkim.cfg &> singleTbar_tW.log
for i in `seq 1 10`;
do
crab -submit 500 -c Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/TTbarInclWIncl_TuneZ2_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> ttbarW.log
for i in `seq 1 10`;
do
crab -submit 500 -c TTbarInclWIncl_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/TTbarZIncl_TuneZ2_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> ttbarZ.log
for i in `seq 1 10`;
do
crab -submit 500 -c TTbarZIncl_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/TTH_HToGG_M-125_7TeV-pythia6_Fall11_LeptonPlus3JetsSkim.cfg &> ttHHtogg.log
for i in `seq 1 10`;
do
crab -submit 500 -c TTH_HToGG_M-125_7TeV-pythia6_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

#crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/TTJets_TuneZ2_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg &> ttbar.log
#for i in `seq 1 10`;
#do
#crab -submit 500 -c TTJets_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_withPDFweights_Dec2013_3
#done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/W1Jet_TuneZ2_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg  &> w1jet.log
for i in `seq 1 10`;
do
crab -submit 500 -c W1Jet_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/W2Jets_TuneZ2_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg  &> w2jet.log
for i in `seq 1 10`;
do
crab -submit 500 -c W2Jets_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/W3Jets_TuneZ2_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg  &> w3jet.log
for i in `seq 1 10`;
do
crab -submit 500 -c W3Jets_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/W4Jets_TuneZ2_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg  &> w4jet.log
for i in `seq 1 10`;
do
crab -submit 500 -c W4Jets_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/WJetsToLNu_TuneZ2_7TeV_madgraph_tauola_Fall11_LeptonPlus3JetsSkim.cfg  &> wjetstolnu.log
for i in `seq 1 10`;
do
crab -submit 500 -c WJetsToLNu_TuneZ2_7TeV-madgraph-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/WW_TuneZ2_7TeV-pythia6-tauola_Fall11_LeptonPlus3JetsSkim.cfg &> ww.log
for i in `seq 1 10`;
do
crab -submit 500 -c WW_TuneZ2_7TeV-pythia6-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/WZ_TuneZ2_7TeV-pythia6-tauola_Fall11_LeptonPlus3JetsSkim.cfg &> wz.log
for i in `seq 1 10`;
do
crab -submit 500 -c WZ_TuneZ2_7TeV-pythia6-tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done

crab -create -cfg BristolAnalysis/NTupleTools/Configuration/defaultMC_Fall11/v10/ZZ_TuneZ2_7TeV-pythia6-tauola_Fall11_LeptonPlus3JetsSkim.cfg &> zz.log
for i in `seq 1 10`;
do
crab -submit 500 -c ZZ_TuneZ2_7TeV_pythia6_tauola_Fall11-PU_S6_START44_V9B-v1_nTuple_v10_LeptonPlus3Jets_Dec2013
done
NTupleProduction
================

## Brief Description
Software for nTuples production (v11) from AOD files for ttbar+X differential cross section analysis

## General Recipe

To setup the code:

```
#set GITHUBUSERNAME if not previously set
export GITHUBUSERNAME=yourGITHUBUsername
git config --global user.github $GITHUBUSERNAME
#on soolin:
export CMSSW_GIT_REFERENCE=/storage/.cmsgit-cache

#change CMSSW installation paths
export SCRAM_ARCH=slc5_amd64_gcc462
scram p -n CMSSW_5_3_20_nTuple_v11 CMSSW_5_3_20
cd CMSSW_5_3_20_nTuple_v11/src/
cmsenv
git cms-init

# Latest PAT recipe
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePATReleaseNotes52X#Add_new_jet_flavour_CMSSW_5_3_20

git cms-addpkg PhysicsTools/PatAlgos

git cms-addpkg EgammaAnalysis/ElectronTools

# ElectroWeakAnalysis needed for full LHAPDF libraries to work
git cms-addpkg ElectroWeakAnalysis/Utilities

# Clone our main ntuple producing software and checkout run1 branch
cd BristolAnalysis/NTupleTools
git remote rename origin upstream
git remote add origin git@github.com:<Your Git name with forked repo>/NTupleProduction.git
git fetch --all
git checkout -b run1 upstream/run1
cd ../../

# Clone our version of the TopSkimming software and checkout run1 branch
git clone git@github.com:BristolTopGroup/TopSkimming.git TopQuarkAnalysis/TopSkimming
cd TopQuarkAnalysis/TopSkimming
git remote rename origin upstream
git checkout -b run1 upstream/run1
cd ../../

#setup full version of LHAPDF (faster AND prevents crashes!)
#https://github.com/cms-sw/cmssw/tree/CMSSW_7_0_X/ElectroWeakAnalysis/Utilities
scram setup lhapdffull
touch $CMSSW_BASE/src/ElectroWeakAnalysis/Utilities/BuildFile.xml
scram b -j8

#get XML files for electron MVA
cd EgammaAnalysis/ElectronTools/data/
cat download.url | xargs wget 
cd -

#test release
#make nTuples
nohup cmsRun BristolAnalysis/NTupleTools/test/makeTuples_cfg.py CMSSW=53X centreOfMassEnergy=8 useData=1 maxEvents=100 dataType=Test skim=NoSkim >&test_data.log &
nohup cmsRun BristolAnalysis/NTupleTools/test/makeTuples_cfg.py CMSSW=53X centreOfMassEnergy=8 useData=0 maxEvents=100 dataType=Test skim=NoSkim >&test_mc.log &
#unfolding
nohup cmsRun BristolAnalysis/NTupleTools/test/unfoldingAndCutflow_cfg.py CMSSW=53X centreOfMassEnergy=8 useData=0 maxEvents=100 dataType=TestUnfold skim=NoSkim >&test_unfolding.log &
# BLT/LGBT
nohup cmsRun BristolAnalysis/NTupleTools/test/makeBLT_cfg.py CMSSW=53X centreOfMassEnergy=8 useData=0 maxEvents=100 dataType=TestBLT skim=NoSkim >& testBLT_mc.log &
nohup cmsRun BristolAnalysis/NTupleTools/test/makeBLT_cfg.py CMSSW=53X centreOfMassEnergy=8 useData=1 maxEvents=100 dataType=TestBLT skim=NoSkim >& testBLT_data.log &

#wait until tasks finish
```


## Notes
More information can be found at [Bristol Ntuple Recipes twiki page](https://twiki.cern.ch/twiki/bin/view/CMS/BristolNTuplerRecipes), although it's outdated.

## Bugs
Please report any problems on our [issues page](https://github.com/BristolTopGroup/NTupleProduction/issues).
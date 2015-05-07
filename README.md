NTupleProduction
================

## Brief Description
Software for nTuples production from miniAOD files for ttbar+X differential cross section analysis

## General Recipe

To setup the code:

```
#set GITHUBUSERNAME if not previously set
export GITHUBUSERNAME=yourGITHUBUsername
git config --global user.github $GITHUBUSERNAME
#on soolin:
export CMSSW_GIT_REFERENCE=/storage/.cmsgit-cache


# Set up the CMSSW release
export SCRAM_ARCH=slc6_amd64_gcc491
cmsrel CMSSW_7_4_0
cd CMSSW_7_4_0/src/
cmsenv
git cms-init
# Do merge-topics and addpkgs first
# Add TopEventProducers as we need to modify one file later on 
git cms-addpkg TopQuarkAnalysis/TopEventProducers/

# Clone our main ntuple producing software and checkout run2 branch
git clone git@github.com:BristolTopGroup/NTupleProduction.git BristolAnalysis/NTupleTools
cd BristolAnalysis/NTupleTools
git remote rename origin upstream
git remote add origin git@github.com:<Your Git name with forked repo>/NTupleProduction.git
git fetch --all
git checkout -b CMSSW_7_3_X upstream/CMSSW_7_3_X
cd ../../

# Clone our version of the TopSkimming software and checkout run2 branch
git clone git@github.com:BristolTopGroup/TopSkimming.git TopQuarkAnalysis/TopSkimming
cd TopQuarkAnalysis/TopSkimming
git remote rename origin upstream
git checkout -b CMSSW_7_3_X upstream/CMSSW_7_3_X
cd ../../

#### In TopQuarkAnalysis/TopEventProducers/python/producers/TopDecaySubset_cfi.py
#### Set runMode to Run2

# Compile
scramv1 b -j 8

#test release
### Not yet available
```

## Notes
More information can be found at [Bristol Ntuple Recipes twiki page](https://twiki.cern.ch/twiki/bin/view/CMS/BristolNTuplerRecipes), although it's outdated.

## Bugs
Please report any problems on our [issues page](https://github.com/BristolTopGroup/NTupleProduction/issues).

# Vagrant
Vagrant is used to "Create and configure lightweight, reproducible, and portable development environments" and can be downloaded from https://www.vagrantup.com/

## How to use the existing CMSSW box
In case you are happy with the existing CMSSW box (kreczko/cmssw), feel free to use it.

```shell
# First download it onto your machine
wget https://copy.com/bmAv9ng0wVSlKw4G
# then add it to your collection
vagrant box add cmssw.box --name kreczko/cmssw
```
Now you will be able to create as many instances of this box as you like by
```shell
# cd into your CMSSW project
vagrant init kreczko/cmssw
vagrant up
# log onto the machine
vagrant ssh
# and follow instructions under "Setting up CMSSW"
``` 

## How to make a vagrant box for NTupleProduction (or any CMSSW project)
A list of general boxes can be found on http://www.vagrantbox.es .
```shell
# go into your project area
vagrant box add SL6 http://lyte.id.au/vagrant/sl6-64-lyte.box
# cd into project directory
# get started with vagrant
vagrant init SL6
vagrant up
vagrant ssh
# you are now in the VM
# your code is now available under /vagrant
cd /vagrant
# install repositories
sudo cp vagrant/cvmfs.repo /etc/yum.repos.d/.
sudo wget -O /etc/pki/rpm-gpg/RPM-GPG-KEY-CernVM http://cvmrepo.web.cern.ch/cvmrepo/yum/RPM-GPG-KEY-CernVM
# install CVMFS and dependencies
sudo yum install cvmfs freetype freetype-devel -y
# configure CVMFS
sudo cp vagrant/default.local /etc/cvmfs/.
sudo cvmfs_config chksetup
# restart autofs service
sudo service autofs restart
```
Everything should be now ready to run CMSSW (easy, right?).

### Setting up CMSSW

```shell
cd
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
. $VO_CMS_SW_DIR/cmsset_default.sh
# follow the instructions except for the NTupleTools git clone
# do not forget to 
# scp -r soolin:/storage/.cmsgit-cache <your NTupleTools folder>
# and
export CMSSW_GIT_REFERENCE=/vagrant/.cmsgit-cache
# also, copy your private key over
# on your machine (for github)
cp ~/.ssh/id_rsa* <your nTuple folder>
# on vagrant VM
mv /vagrant/id_rsa* ~/.ssh/.
# next we need a CMSSW release
cd ~
cmsrel CMSSW_7_0_9_patch2
```
Because CMSSW does not like symlinks we have to exit the Vagrant box now and change the mount point.
Edit the Vagrant file to adjust your path to your CMSSW area, i.e.
```config.vm.synced_folder ".", "/home/vagrant/CMSSW_7_0_9_patch2/src/NTupleProduction"```
and restart the Vagrant box (```vagrant halt && vagrant up```).
Now ssh into the box again and go into the CMSSW src folder
```shell 
cd /home/vagrant/CMSSW_7_0_9_patch2/src
scram b -j2
```
Hooray! You are compiling a CMSSW package on your machine!
Once you are done with the machine you can exit (```exit```) and either destroy the machine or halt it
```
# to destroy 
vagrant destroy
# to halt
vagrant halt
```

You can also package the box for others using
```shell
vagrant box package ....
```
And upload it to a suitable location.

## HDFS on the Vagrant box
```shell
# connect to HDFS:
sudo yum install nfs-utils -y
sudo mkdir /hdfs
sudo mount -t nfs -o vers=3,proto=tcp,nolock  dice-io-37-01.acrc.bris.ac.uk:/ /hdfs
# run tests
```

## Vagrant troubleshooting
### GuestAdditions versions on your host (XXX) and guest (YYY) do not match.
To solve this problem follow: http://kvz.io/blog/2013/01/16/vagrant-tip-keep-virtualbox-guest-additions-in-sync/

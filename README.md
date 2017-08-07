NTupleProduction
================

## Brief Description
Software for nTuples production from MiniAOD files for ttbar+X differential cross section analysis.
The master branch corresponds to the Run 2 analysis path.
For the Run 1 analysis path, please refer to branch 'run1' as well as the relevant releases.

## General Recipe
To setup the code:
```
git clone git@github.com:BristolTopGroup/NTupleProduction.git
cd NTupleProduction
source bin/env.sh
ntp setup
```
which should create the folders`external` and `workspace`.
Some git cms-merge-topics can add unwanted packages (e.g. Fireworks). Remove them from `/workspace/CMSSW_VERSION/src/` before compiling, to save time and effort.
For available commands and how to use them type `ntp help`.

### Testing
To check if all is OK you can run
```
./test/test.sh
```

### Generate the configs
python python/crab/generate_datasets.py

## Notes
More information can be found at [Bristol Ntuple Recipes twiki page](https://twiki.cern.ch/twiki/bin/view/CMS/BristolNTuplerRecipes), although it's outdated.

## Bugs
Please report any problems on our [issues page](https://github.com/BristolTopGroup/NTupleProduction/issues).

# Vagrant (work in progress)
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
cmsrel CMSSW_7_4_10_patch1
```
Because CMSSW does not like symlinks we have to exit the Vagrant box now and change the mount point.
Edit the Vagrant file to adjust your path to your CMSSW area, i.e.
```config.vm.synced_folder ".", "/home/vagrant/CMSSW_7_0_9_patch2/src/NTupleProduction"```
and restart the Vagrant box (```vagrant halt && vagrant up```).
Now ssh into the box again and go into the CMSSW src folder
```shell
cd /home/vagrant/CMSSW_7_4_10_patch1/src
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

#!/bin/bash
set -o errexit -o nounset -o pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install build-essential software-properties-common -y
add-apt-repository ppa:ubuntu-toolchain-r/test -y
apt-get update -y
apt-get install build-essential software-properties-common -y
apt-get update
apt-get install gcc-5 g++-5 -y
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 60 --slave /usr/bin/g++ g++ /usr/bin/g++-5
update-alternatives --config gcc 

apt-get install git python wget -y
apt-get install ninja-build fontconfig libfontconfig1-dev libglu1-mesa-dev curl zip ninja-build -y
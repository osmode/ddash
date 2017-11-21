#!/bin/bash
# DDASH Network Utility
# Author: Omar N. Metwally, MD
# omar.metwally@gmail.com
# https://github.com/osmode/ddash
# USAGE:  ./installer.sh 

finished=false
pwd=$(pwd)

while [ $finished = false ] 
do
	read -p "
Welcome to the DDASH Installer. What would you like to do?
1: Install DDASH and DDASH Network Utility
2: Reset chain data
3: Exit

Your choice> " choice

    if [ "$choice" = 1 ]; then
	echo Installing dependencies...
	echo ""

	apt-get update
	apt-get install unzip
	apt-get install zip
	apt-get install software-properties-common
	add-apt-repository -y ppa:ethereum/ethereum
	apt-get install ethereum
	add-apt-repository ppa:ethereum/ethereum
	apt-get update
	apt-get install solc

	if [ ! -f /usr/local/bin/ipfs ]; then
	    wget https://dist.ipfs.io/go-ipfs/v0.4.10/go-ipfs_v0.4.10_linux-386.tar.gz
	    tar xvfz go-ipfs_v0.4.10_linux-386.tar.gz
	    mv go-ipfs/ipfs /usr/local/bin/ipfs
	    rm go-ipfs_v0.4.10_linux-386.tar.gz
	fi

	ipfs init
	apt-get install python-pip
	pip install web3
	pip install ipfsapi
	pip install python-gnupg


	if [ ! -d $pwd/ddash ]; then
	    mkdir -p $pwd/ddash;
	    mkdir -p $pwd/ddash/data;
	    mkdir -p $pwd/ddash/source;
	fi

	read -p "Please specify chainId (do not use 0 or 1): " chainId
	read -p "Please specify mining difficulty (or leave blank for default): " diff

	echo "{" >> $pwd/ddash/genesis.json
	echo "  \"config\":  {" >> $pwd/ddash/genesis.json
	echo "        \"chainId\": $chainId, " >> $pwd/ddash/genesis.json
	echo "        \"homesteadBlock\": 0," >> $pwd/ddash/genesis.json
	echo "        \"eip155Block\": 0,">> $pwd/ddash/genesis.json
	echo "        \"eip158Block\": 0" >> $pwd/ddash/genesis.json
	echo "    }," >> $pwd/ddash/genesis.json
	echo "  \"alloc\": {" >> $pwd/ddash/genesis.json
	echo "  }," >> $pwd/ddash/genesis.json
	echo "  \"coinbase\"   : \"0x0000000000000000000000000000000000000000\", " >> $pwd/ddash/genesis.json

	# if no difficulty is specified, use default
	if [ ! -z $diff ]; then
	    echo "  \"difficulty\" : \"0xF4240\", " >> $pwd/ddash/genesis.json
	else
	    echo "  \"difficulty\" : \"$diff\", " >> $pwd/ddash/genesis.json

	fi

	echo "  \"extraData\"  : \"\", " >> $pwd/ddash/genesis.json
	echo "  \"gasLimit\"   : \"0x2fefd8\", " >> $pwd/ddash/genesis.json
	echo "  \"nonce\"      : \"0x000000$RANDOM\", " >> $pwd/ddash/genesis.json
	echo "  \"mixhash\"    : \"0x0000000000000000000000000000000000000000000000000000000000000000\", " >> $pwd/ddash/genesis.json
	echo "  \"parentHash\" : \"0x0000000000000000000000000000000000000000000000000000000000000000\", " >> $pwd/ddash/genesis.json
	echo "  \"timestamp\"  : \"0x00\" " >> $pwd/ddash/genesis.json
	echo "}" >> $pwd/ddash/genesis.json

	geth --datadir=$pwd/ddash/data init $pwd/ddash/genesis.json
    fi

    if [ "$choice" = 2 ]; then
	rm -r $pwd/ddash/data/geth
	rm $pwd/ddash/genesis.json
	echo Chain data cleared from $pwd/ddash/data/geth. Genesis file deleted.
    fi

    if [[ "$choice" = 3 ]] || [[ "$choice" == "exit" ]] || [[ "$choice" == "quit" ]]; then
	exit
    fi

done

#!/bin/bash
# DDASH Network Utility
# Author: Omar N. Metwally, MD
# omar.metwally@gmail.com
# https://github.com/osmode/ddash
# USAGE:  ./install.sh 
# Installs DDASH dependencies

finished=false
pwd=$(pwd)

while [ $finished = false ] 
do
	read -p "
Welcome to the DDASH Installer. What would you like to do?
1: Install DDASH and DDASH Network Utility
2: Reset chain data and delete all Ethereum accounts
3: Exit

Your choice> " choice

    if [ "$choice" = 1 ]; then
	tmux kill-session -t geth
	#tmux kill-session -t ipfs
	echo -e "\033[1;32mDDASH will now attempt to install necessary dependencies on your machine. \033[0m"

	echo ""
	os="$(uname -s)"
	if [ "$os" = 'Darwin' ]; then
		echo "It appears you're installing DDASH on a Mac."

		while true; do
		read -p "Would you like to install Homebrew? Enter Y/n: " answer1
			if [[ "$answer1" = 'y' ]] || [[ "$answer1" = 'Y' ]] || [[ "$answer1" = 'n' ]] || [[ "$answer1" = 'N' ]]; then
				break
			fi
		done
			
		if [[ "$answer1" = 'Y' ]] || [[ "$answer1" = 'y' ]]; then
		    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
		    brew update
		fi

		while true; do
		read -p "Would you like to install Python3? Enter Y/n: " answer_python3
			if [[ "$answer_python3" = 'y' ]] || [[ "$answer_python3" = 'Y' ]] || [[ "$answer_python3" = 'n' ]] || [[ "$answer_python3" = 'N' ]]; then
				break
			fi
	
	 
		done
		if [[ "$answer_python3" = 'y' ]] || [[ "$answer_python3" = 'Y' ]]; then
			brew install python3
		fi

		while true; do
		read -p "Would you like to install the Go compiler? Enter Y/n: " answer2
			if [[ "$answer2" = 'y' ]] || [[ "$answer2" = 'Y' ]] || [[ "$answer2" = 'N' ]] || [[ "$answer2" = 'n' ]]; then
				break
			fi
		done

		if [[ "$answer2" = 'Y' ]] || [[ "$answer2" = 'y' ]]; then
		    brew update
		    brew install go
		fi

		while true; do
		read -p "Would you like to install the Go Ethereum client? Enter Y/n: " answer3
			if [[ "$answer3" = 'y' ]] || [[ "$answer3" = 'Y' ]] || [[ "$answer3" = 'N' ]] || [[ "$answer3" = 'n' ]]; then
				break
			fi
		done	

		if [[ "$answer3" = 'Y' ]] || [[ "$answer3" = 'y' ]]; then
		    brew tap ethereum/ethereum
		    brew install ethereum
		fi

		while true; do
		read -p "Would you like to install Node and npm? Enter Y/n: " answer4
			if [[ "$answer4" = 'y' ]] || [[ "$answer4" = 'Y' ]] || [[ "$answer4" = 'N' ]] || [[ "$answer4" = 'n' ]]; then
				break
			fi
		done	
		if [[ "$answer4" = 'Y' ]] || [[ "$answer4" = 'y' ]]; then
		    brew install node
		fi
		while true; do
		read -p "Would you like to install the solC compiler? Enter Y/n: " answer5
			if [[ "$answer5" = 'y' ]] || [[ "$answer5" = 'Y' ]] || [[ "$answer5" = 'N' ]] || [[ "$answer5" = 'n' ]]; then
				break
			fi
		done	
		if [[ "$answer5" = 'Y' ]] || [[ "$answer5" = 'y' ]]; then
		    npm install -g solc	    
		fi
		while true; do
		read -p "Would you like to install tmux? Enter Y/n: " answer6
			if [[ "$answer6" = 'y' ]] || [[ "$answer6" = 'Y' ]] || [[ "$answer6" = 'N' ]] || [[ "$answer6" = 'n' ]]; then
				break
			fi	
		done
		if [[ "$answer6" = 'Y' ]] || [[ "$answer6" = 'y' ]]; then
		    brew install tmux
		fi

	fi
	if [ "$os" = 'Linux' ]; then
		echo "Installing Ubuntu dependencies..."
		apt-get update
		apt-get install unzip
		apt-get install zip
		apt-get install software-properties-common
		add-apt-repository -y ppa:ethereum/ethereum
		apt-get install ethereum
		add-apt-repository ppa:ethereum/ethereum
		apt-get update
		apt-get install solc
	    apt-get install python3-pip
	fi

	#if [ ! -f /usr/local/bin/ipfs ]; then
	#    wget https://dist.ipfs.io/go-ipfs/v0.4.10/go-ipfs_v0.4.10_linux-386.tar.gz
	#    tar xvfz go-ipfs_v0.4.10_linux-386.tar.gz
	#    mv go-ipfs/ipfs /usr/local/bin/ipfs
	#    rm go-ipfs_v0.4.10_linux-386.tar.gz
	#fi

	#ipfs init
	pip3 install web3
	#pip3 install ipfsapi
	#pip3 install python-gnupg


	if [ ! -d $pwd/ddash ]; then
	    mkdir -p $pwd/ddash;
	    mkdir -p $pwd/ddash/data;
	    mkdir -p $pwd/ddash/source;
	fi

	#echo "Resetting static-nodes.json"
	#if [ -f $PWD/ddash/data/static-nodes.json ];then
	#	rm $PWD/ddash/data/static-nodes.json
	#fi
	#echo "[" >> $PWD/ddash/data/static-nodes.json
	#echo "]" >> $PWD/ddash/data/static-nodes.json

	read -p "Please specify chainId (or leave blank for default): " chainId
	if [ -z $chainId ]; then
		chainId=32
	fi		
	read -p "Please specify mining difficulty (or leave blank for default): " diff
	read -p "Please specify nonce (or leave blank for default): " nonce
	if [ -z $nonce ]; then
		nonce=32
	fi
	read -p "Please specify a gas limit (leave leave blank for default value 0x5FDFB0): " gaslimit

	if [ -f $PWD/ddash/genesis.json ]; then
	    rm $PWD/ddash/genesis.json
	fi

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
	if [ -z $diff ]; then
	    echo "No difficulty specified. Using default."
	    echo "  \"difficulty\" : \"0xF4240\", " >> $pwd/ddash/genesis.json
	else
	    echo User-defined difficulty: "$diff"
	    echo "  \"difficulty\" : \"$diff\", " >> $pwd/ddash/genesis.json
	fi
	echo "  \"extraData\"  : \"\", " >> $pwd/ddash/genesis.json
	if [ -z $gaslimit ]; then
	    echo "No gas limit specified. Using default..."
	    echo "  \"gasLimit\"   : \"0x5FDFB0\", " >> $pwd/ddash/genesis.json
	else 
	    echo User-defined gas limit: "$gaslimit"	
	    echo "  \"gasLimit\"   : \""$gaslimit"\", " >> $pwd/ddash/genesis.json
	fi

	if [ -z $nonce ]; then
	    echo "  \"nonce\"      : \"0x000000$RANDOM\", " >> $pwd/ddash/genesis.json
	else
	    echo "  \"nonce\"      : \"0x000000$nonce\", " >> $pwd/ddash/genesis.json
	fi

	echo "  \"mixhash\"    : \"0x0000000000000000000000000000000000000000000000000000000000000000\", " >> $pwd/ddash/genesis.json
	echo "  \"parentHash\" : \"0x0000000000000000000000000000000000000000000000000000000000000000\", " >> $pwd/ddash/genesis.json
	echo "  \"timestamp\"  : \"0x00\" " >> $pwd/ddash/genesis.json
	echo "}" >> $pwd/ddash/genesis.json

	geth --datadir=$pwd/ddash/data init $pwd/ddash/genesis.json

        read -p "Enter your network id (or leave blank for default value 4828): " networkId
        read -p "Enter port (or leave blank for default value 30303): " port
        read -p "Enter rpc port (or leave blank for default value 8545): " rpcport

        if [ -z "$networkId" ]; then
            networkId=4828
        fi
        if [ -z "$port" ]; then
            port=30303
        fi
        if [ -z "$rpcport" ]; then
            rpcport=8545
        fi

        echo "exit" | geth --verbosity 2 --datadir=$PWD/ddash/data --networkid "$networkId" --port "$port" --rpc --rpcport "$rpcport" console

	#rm -r $PWD/go-ipfs
	# save enode information
	./log_nodeInfo.sh
    fi  # end if [ "$choice" =1 ]

    if [ "$choice" = 2 ]; then
	rm -r $PWD/ddash/data/geth
	rm -r $PWD/ddash/data_mainnet/geth
	rm $pwd/ddash/genesis.json
	rm $PWD/ddash/nodeInfo.ds
	echo Chain and account data cleared from $pwd/ddash/data/geth. Genesis file deleted.
    fi

    if [[ "$choice" = 3 ]] || [[ "$choice" == "exit" ]] || [[ "$choice" == "quit" ]]; then
	exit
    fi
done

echo -e "\033[1;32mCongratulations! DDASH has been installed on your machine. I will now attempt to start the GUI. \033[0m"

python3 gui.py


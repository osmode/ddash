#!/bin/bash

finished=false

if [ ! $finished = false ]; then
    echo finished is false
fi

while [ $finished = false ]
do

 read -p "Welcome to the DDASH Network Utility. What would you like to do?
1: Create new Ethereum account
2: Show existing Ethereum accounts
3: Start mining
4: Compile and deploy contract
5: Start DDASH
6: Exit

> " choice

    if [ "$choice" = 1 ]; then
	tmux kill-session -t geth
	tmux kill-session -t ipfs

	read -sp "Choose a password: " pass        
	echo "personal.newAccount(\"$pass\")" | geth --verbosity 1 --datadir=$PWD/ddash/data console 
    fi
    if [ "$choice" = 2 ]; then
	tmux kill-session -t geth
	tmux kill-session -t ipfs

	geth --verbosity 1 --datadir=$PWD/ddash/data console <<< $'eth.accounts'

	echo $PID
    fi
    if [ "$choice" = 3 ]; then
	tmux kill-session -t geth
	tmux kill-session -t ipfs
	geth --datadir=$PWD/ddash/data --mine --minerthreads=1 
    fi
    if [ "$choice" = 4 ]; then
	tmux kill-session -t geth
	tmux kill-session -t ipfs

	./deploy.sh
    fi

    # start DDASH    
    if [ "$choice" = 5 ]; then
	
	# before starting DDASH, need to start IPFS and geth daemons
	tmux new-session -d -s geth "geth --verbosity 2 --datadir=$PWD/ddash/data --networkid 4828 --port 30303 --rpcapi=\"db,eth,net,personal,web3\" --rpc --rpcport 8545 console"
	
	tmux new-session -d -s ipfs 'ipfs daemon'
	sleep 5

	python $PWD/ddash/main.py
    fi

    if [[ "$choice" = 6 ]] || [[ "$choice" == "exit" ]] || [[ "$choice" == "quit" ]]; then
        finished=true
    fi
done
exit 0

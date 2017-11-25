#!/bin/bash

finished=false

if [ ! $finished = false ]; then
    echo finished is false
fi

while [ $finished = false ]
do

 read -p "
Welcome to the DDASH Network Utility. What would you like to do?
1: Create new Ethereum account
2: Show existing Ethereum accounts
3: Start mining
4: Compile and deploy contract
5: Start DDASH
6: Show network settings
7: Add peer
8: Launch private network
9: Exit

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

	read -p "Enter your Ethereum address (without quotes). E.g. 0x...
> " addr
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
	geth --verbosity 3 --datadir=$PWD/ddash/data --mine --minerthreads=1 --etherbase "$addr"

    fi
    if [ "$choice" = 4 ]; then
	tmux kill-session -t geth
	tmux kill-session -t ipfs

	./deploy.sh
    fi

    # start DDASH    
    if [ "$choice" = 5 ]; then
	
	# before starting DDASH, need to start IPFS and geth daemons
	#tmux new-session -d -s geth "geth --verbosity 2 --datadir=$PWD/ddash/data --networkid 4828 --port 30303 --rpcapi=\"db,eth,net,personal,web3\" --rpc --rpcport 8545 console"

        tmux new-session -d -s geth "geth --verbosity 3 --datadir=$PWD/ddash/data --networkid $networkId --port $port  --rpcapi=\"db,eth,net,personal,web3\" --rpc --rpcport $rpcport --mine --minerthreads=1 console"
 
	tmux new-session -d -s ipfs 'ipfs daemon'
	sleep 5

	python $PWD/ddash/main.py
    fi

    if [[ "$choice" = 6 ]]; then

	output="$(geth --datadir=$PWD/ddash/data console <<< $'admin.nodeInfo')"
	echo ""
	echo ""
	echo ""
	if [[ "$output" =~ \"enode[^,]* ]]; then
    		echo "your enode is:  ${BASH_REMATCH[0]}"
	fi

	genesis=`cat $PWD/ddash/genesis.json`

	if [[ "$genesis" =~ difficulty[^,]* ]]; then
		diff=${BASH_REMATCH[0]:15:6}
		echo difficulty: "$diff"
	fi

	if [[ "$genesis" =~ nonce[^,]* ]]; then
		nonce=${BASH_REMATCH[0]:15}
		echo nonce: \""$nonce"
	fi

	if [[ "$genesis" =~ chainId[^,]* ]]; then
		chainId=${BASH_REMATCH[0]:9:6}
		echo chainId: "$chainId"
	fi
	echo ""
	echo ""
	echo ""

    fi

    if [[ "$choice" = 7 ]]; then
	read -p "Enter enode address (without quotes). Example:  enode://... 
" enode

	num_lines=`cat $PWD/ddash/data/static-nodes.json | wc -l`
	i=0

	while IFS= read -r line 
	do
	    if [[ $num_lines -gt 2 ]] && [[ $i -eq $[num_lines-2] ]]; then
	        echo add comma
		echo "$line", >> $PWD/ddash/data/static-nodes2.json
	    else
		echo "$line" >> $PWD/ddash/data/static-nodes2.json
	    fi

	    if [ $i = $[$num_lines-2] ]; then
	        echo \""$enode"\" >> $PWD/ddash/data/static-nodes2.json
	    fi
	    i=$[i+1]

	done < "$PWD/ddash/data/static-nodes.json"

	mv $PWD/ddash/data/static-nodes2.json $PWD/ddash/data/static-nodes.json

    fi

    if [[ "$choice" = 8 ]]; then
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
       geth --verbosity 2 --datadir=$PWD/ddash/data --networkid "$networkId" --port "$port" --rpc --rpcport "$rpcport" console
   fi

    if [[ "$choice" = 9 ]] || [[ "$choice" == "exit" ]] || [[ "$choice" == "quit" ]]; then
        finished=true
    fi

done
exit 0

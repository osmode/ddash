#!/bin/bash

#output="$(geth --datadir=$PWD/ddash/data console <<< $'admin.nodeInfo')"

#if [[ "$output" =~ \"enode[^,]* ]]; then
#    echo "matched part is ${BASH_REMATCH[0]}"
#    echo "end of match"
#fi

genesis=`cat $PWD/ddash/genesis.json`

if [[ "$genesis" =~ difficulty[^,]* ]]; then
    echo "matched part is ${BASH_REMATCH[0]}"
    echo "end of match"
    diff=${BASH_REMATCH[0]:15:6}
    echo difficulty: "$diff"
fi

if [[ "$genesis" =~ nonce[^,]* ]]; then
    echo "matched part is ${BASH_REMATCH[0]}"
    echo "end of match"
    diff=${BASH_REMATCH[0]:15}
    echo nonce: "$diff"
fi

if [[ "$genesis" =~ chainId[^,]* ]]; then
    echo "matched part is ${BASH_REMATCH[0]}"
    echo "end of match"
    diff=${BASH_REMATCH[0]:9:6}
    echo chainId: "$diff"
fi





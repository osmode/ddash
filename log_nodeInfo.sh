#!/bin/bash
rm $PWD/ddash/nodeInfo.ds

output="$(geth --datadir=$PWD/ddash/data console <<< $'admin.nodeInfo')"

if [[ "$output" =~ \"enode[^,]* ]]; then
    echo "your enode is:  ${BASH_REMATCH[0]}"
    echo "${BASH_REMATCH[0]}" >> $PWD/ddash/nodeInfo.ds
fi

output="$(ifconfig)"

#if [[ "$output" =~ inet[^,]*[B] ]]; then
#    echo "your ip address is:  ${BASH_REMATCH[0]}"
#fi

#echo "$output" | grep -oE '(((inet addr:)1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){3}(1?[0-9][0-9]?|2[0-4][0-9]|25[0-5]) '  >> $PWD/ddash/nodeInfo.ds

result=$(echo "$output" | grep -oE '(((inet addr:)1?[0-9][0-9]?|2[0-4][0-9]|25[0-5])\.){3}(1?[0-9][0-9]?|2[0-4][0-9]|25[0-5][^\s]) ')
echo your ip address is: ${result:10} 
echo ${result:10} >> $PWD/ddash/nodeInfo.ds

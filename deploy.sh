#!/bin/bash
# DDASH Network Utility
# Author: Omar N. Metwally, MD
# omar.metwally@gmail.com
# https://github.com/osmode/ddash
# USAGE:  ./manager.sh your_contract_name (without .sol extension)
#
pwd=$(pwd)
# compile contract
if [ ! $1 ]; then
    read -p "Please specify a contract name (without the .sol extension): " contract_name

else
    contract_name=$1
fi

read -p "Please enter the amount of gas for deployment (e.g. 1000000): " gas

echo "$contract_name"
echo Deleting old ABIs and data...

echo Compiling $PWD/ddash/source/"$contract_name".sol
rm $PWD/ddash/source/*.abi
rm $PWD/ddash/source/*/bin

solc --bin --abi -o $PWD/ddash/source $PWD/ddash/source/"$contract_name".sol

if [ -f $PWD/ddash/source/"$contract_name".js ]; then
    rm $PWD/ddash/source/"$contract_name".js
fi

output_file=$PWD/ddash/source/"$contract_name".js
data_dir=$PWD/ddash/data

contract_abi=$(<$PWD/ddash/source/"$contract_name".abi)
data=$(<$PWD/ddash/source/"$contract_name".bin)
echo ""
echo contract_abi: "$contract_abi"
echo ""
echo data: "$data"
echo ""
echo var contract_abi=web3.eth.contract\("$contract_abi"\)\; >> "$output_file"
echo "" >> "$output_file"

echo var contract_obj = contract_abi.new\( >> "$output_file"
echo    { >> "$output_file"
echo	from: web3.eth.accounts[0], >> "$output_file"
echo	data: \'0x"$data"\', >> "$output_file"
echo	gas: \'"$gas"\' >> "$output_file"
echo    }, function \(e, contract\) { >> "$output_file"
echo	console.log\(e, contract\)\; >> "$output_file"
echo	if \(typeof contract.address !== \'undefined\'\) { >> "$output_file"
echo	    console.log\(\'Contract mined! address: \' + contract.address + \' transactionHash: \' + contract.transactionHash\)\; >> "$output_file"
echo    } >> "$output_file"
echo    }\) >> "$output_file"

if [ ! -f "$output_file" ]; then
    echo Failed to create contract deployment script in "$output_file"
    exit 1
else

    # deploy contract
    echo Deploying contract "$output_file"
    read -sp "Please enter your Ethereum account password: " pass
    geth --exec "personal.unlockAccount(eth.accounts[0],\"$pass\");loadScript('/root/ddash/source/$contract_name.js')" --datadir=/root/ddash/data console

    geth --datadir=$PWD/ddash/data --mine --minerthreads=1 console

fi

$SHELL

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
    read -p "Please specify a contract name without the .sol extension (or leave blank for blackswan): " contract_name
    if [ -z "$contract_name" ]; then
        contract_name="blackswan"
    fi
else
    contract_name=$1
fi

read -p "Please enter the amount of gas for deployment (or leave blank for default): " gas
if [ -z "$gas" ]; then
gas=2000000
fi

echo "$contract_name"
echo Deleting old ABIs and data...

echo Compiling $PWD/ddash/source/"$contract_name".sol
echo Removing old files named "$contract_name".js...
if [ -f $PWD/ddash/source/$contract_name.js ]; then
	rm $PWD/ddash/source/$contract_name.js
fi

# compilation on Ubuntu uses solc compiler
# compilation on Mac OS X uses solcjs
os="$(uname -s)"
if [ "$os" = 'Darwin' ]; then
echo Compiling "$contract_name".sol using solcjs...
solcjs --bin --abi -o $PWD/ddash/source $PWD/ddash/source/"$contract_name".sol

sleep 2

# need to convert all *abi and *bin files to lowercase to prevent errors
for file in $PWD/ddash/source/*.abi; do mv $file $PWD/ddash/source/"$(basename $file | tr '[:upper:]' '[:lower:]')"; done
for file in $PWD/ddash/source/*.bin; do mv $file $PWD/ddash/source/"$(basename $file | tr '[:upper:]' '[:lower:]')"; done

# convert ABI and BIN files to short names
for file in $PWD/ddash/source/*$contract_name.abi; 
    do mv "$file" $PWD/ddash/source/$contract_name.abi;
done
for file in $PWD/ddash/source/*$contract_name.bin
	do mv "$file" $PWD/ddash/source/$contract_name.bin;
done

fi

if [ "$os" = 'Linux' ]; then
solc --bin --abi -o $PWD/ddash/source $PWD/ddash/source/"$contract_name".sol
fi

output_file=$PWD/ddash/source/"$contract_name".js
data_dir=$PWD/ddash/data

contract_abi=$(<$PWD/ddash/source/"$contract_name".abi)
data=$(<$PWD/ddash/source/"$contract_name".bin)

# if ABI and BIN files exist (compilation was successful), propmt
# for contract constructor arguments
if [[ -f $PWD/ddash/source/"$contract_name".abi ]] && [[ -f $PWD/ddash/source/"$contract_name".bin ]]; then
	read -p "Enter contract constructor arguments separated by commas (optional): " constructor_args
fi

 # clean up junk name files
rm $PWD/ddash/source/_users_*
   
echo ""
echo contract_abi: "$contract_abi"
echo ""
echo data: "$data"
echo ""
echo var contract_abi=web3.eth.contract\("$contract_abi"\)\; >> "$output_file"
echo "" >> "$output_file"

if [ -z "$constructor_args" ]; then
	echo var contract_obj = contract_abi.new\( >> "$output_file"
else
	echo var contract_obj = contract_abi.new\( "$constructor_args", >> "$output_file"
fi

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
    #echo Deploying contract "$output_file"
    #read -sp "Please enter your Ethereum account password: " pass
    #geth --exec "personal.unlockAccount(eth.accounts[0],\"$pass\");loadScript('/root/ddash/source/$contract_name.js')" --datadir=/root/ddash/data console

    #geth --datadir=$PWD/ddash/data --mine --minerthreads=1 console

fi

$SHELL

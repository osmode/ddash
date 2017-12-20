# DDASH 

## What is DDASH?
---
DDASH is a protocol for information exchange across Ethereum networks. 


* Interface between private net Ether and main net Ether

* One-click creation of self-propagating Ethereum networks (no need for manual enode entry)

* One-click compilation and deployment of Ethereum contracts to any Ethereum blockchain 

* Optionally allows DApps to interface with the Interplanetary File System ([IPFS](https://github.com/ipfs/ipfs)) to minimize on-chain storage 


## SwapCoin
SwapCoin is the utility token that powers DDASH, enabling the exchange of information and value across Ethereum networks. SwapCoin is based on the ERC20 standard but differs slightly in the nomenclature of its methods. The SWAP ABI and contract are located in the source directory and can be directly inspected at address 0xeD8C634aC8C2fa3694C32Cb01b96A6912f8a7738.

SwapCoin and Ether can be exchanged using the DDASH client, which can be launched by running 
```
python3 gui.py 
```

## Why DDASH?
DDASH combines the benefits of private Ethereum networks with the benefits of the Ethereum main network. DDASH allows Ethereum applications to run cheaply and securely on private Ethereum networks while enabling their integration with the main Ethereum network. The result is greatly reduced development and operational costs associated with private Ethereum networks, combined with the ability to transfer Ether among the main Ethereum network and private Ethereum networks.

### In its usual siloed state, data is a liability rather than an asset.

### DDASH turns data into digital assets.

Our goals are to:

### Eliminate barriers to information exchange within and among organizations.
### Build economies around knowledge and information

## Prerequisites
---
This project builds on work by the [Ethereum](https://www.ethereum.org), [web3.py](https://github.com/pipermerriam/web3.py), [IPFS](https://github.com/ipfs/ipfs) and [py-ipfs](https://github.com/ipfs/py-ipfs-api) communities. 

The DDASH Installer, which currently supports Ubuntu 16.04 and Mac OS, installs all dependencies (including the Go Ethereum client).

## Precautions
The technologies used here are still in alpha, and this software is still in development. 

## Quickstart 
DDASH, the DDASH Installer, and the DDASH Network Utility currently support Ubuntu 16.04 and Mac OS X.

Before you start, be sure you're running these scripts with appropriate permissions (usually sudo on Unix systems) and change file permissions of the *install.sh*, *deploy.sh*, *gui.sh* and *manager.sh* bash scripts to allow execution:

```
chmod u+x install.sh deploy.sh dnu.sh gui.sh
```

Navigate to the directory where you want to install DDASH and run:
```
./install.sh
```
This will install the Go Ethereum client and the necessary Python modules to allow DDASH to interface with these clients. 

To start the DDASH Networking Utility, run:
```
./dnu.sh
```

To start *Twin Peaks*, DDASH's Graphical User Interface, run:
```
python3 gui.py
```


## Directory structure
The directory structure is important because DDASH and the DDASH Networking Utility look for certain files in certain directories. Your application will look something like this:
```
/your_working_directory
	README.md
	install.sh
	dnu.sh
	deploy.sh
	log_nodeInfo.sh
	load_mainnet.sh
	load_blackswan.sh 

	/ddash
		crypto.py
		genesis.json
		bcinterface.py
		fsinterface.py
		ipfs.py
		main.py
		nodeInfo.ds
		
        /source
		/data
	    	static-nodes.json

	/share
	/swap

```
Save Ethereum contracts in the *source* directory with the .sol extension.
Meta-data (MD5 hashes, filenames, and file descriptions) of the *share* directory's contents are saved on chain.
*By default, locally hosted files are not uploaded to IPFS; only meta-data are shared with the network.*

## How to acquire SwapCoin
Use the DDASH GUI  exchange Ether for SwapCoin. 
![SwapCoin](https://s3-us-west-1.amazonaws.com/ddash/mainnet.png)


## The DDASH Command Line Interface
```
        _____  _____           _____ _    _ 
       |  __ \|  __ \   /\    / ____| |  | |
       | |  | | |  | | /  \  | (___ | |__| |
       | |  | | |  | |/ /\ \  \___ \|  __  |
       | |__| | |__| / ____ \ ____) | |  | |
       |_____/|_____/_/    \_\_____/|_|  |_|
                                                                
    ::: Distributed Data Sharing Hyperledger :::

    Welcome to the DDASH Command Line Interface.

[1]		ddash> peer count
[2]		ddash> upload
[3]		ddash> download
[4]		ddash> hello
[5]		ddash> listen
[6]		ddash> broadcast
[7]		ddash> quit
[8]		ddash> show accounts
[9]		ddash> use account 0

```
The above commands:

[1]  returns number of enodes found on chain

[2]  upload meta-data of *share* directory's contents to blockchain 

[3]  query blockchain for file meta-data

[5] query blockchain for peer enodes

[6] broadcast client enode to blockchain

[8] enumerate Ethereum accounts

[9] set current Ethereum account to zero-index account (last argument refers to account index)


## Contribute
### Use cases
If you or your organization use DDASH to do something that would otherwise be impossible using a centralized system, please share your experience!

### Bug reports
You can submit bug reports using the [GitHub issue tracker](https://github.com/osmode/ddash/issues).

### Pull requests
Pull requests are welcome.

## License
MIT License (see *LICENSE* file for details).


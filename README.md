# Distributed Data Sharing Hyperledger (DDASH)

             _____  _____           _____ _    _ 
            |  __ \|  __ \   /\    / ____| |  | |
            | |  | | |  | | /  \  | (___ | |__| |
            | |  | | |  | |/ /\ \  \___ \|  __  |
            | |__| | |__| / ____ \ ____) | |  | |
            |_____/|_____/_/    \_\_____/|_|  |_|
                                             

:earth_americas: :rocket: :boom: :rocket: :earth_asia: :boom: :rocket: :boom: :earth_africa: :rocket: :boom: :rocket: :earth_americas:


## What is DDASH?
---
DDASH is a protocol for exchange of distributed data in blockchain networks.

* One-click Ethereum coinification of any digital resource

* One-click creation of self-propagating Ethereum networks (no need for manual enode entry)

* One-click compilation and deployment of Ethereum contracts to any Ethereum blockchain 

* Allows DApps to interface with the Interplanetary File System ([IPFS](https://github.com/ipfs/ipfs)) to minimize on-chain storage 

* Upload and download data to/from an Etheruem blockchain with one click

## DDASH Walkthrough 
[![DDASH Walkthrough Video](https://s3-us-west-1.amazonaws.com/ddash/intro.png)](https://youtu.be/dV0Uel2M4kQ)
 

## Why DDASH?
Despite the wealth of data produced by academic institutions, research labs, hospitals, and corporations, only a small percentage of data is used to its fullest potential. DDASH is an emerging blockchain networking protocol that interfaces between common data formats and the Ethereum blockchain, between the Ethereum blockchain and IPFS, and for private Ethereum networking.

### In its usual siloed state, data is a liability rather than an asset.

### DDASH turns data into digital assets.

DDASH allows network administrators to quickly create, maintain, and grow private Ethereum networks. Data can be uploaded to a blockchain and downloaded from a blockchain with a single command. DDASH also interfaces with IPFS to allow network administrators to host resources on IPFS and use the Ethereum blockchain as a permissions manager. No longer confined to a single machine, data hosted on the IPFS network flows perputually through network nodes, rendering it persistent and rapidly accessible. Permissions are managed via PGP keypair encryption and stored on the Ethereum blockchain. 

Our goals are to:

1. Eliminate barriers to information exchange within and among organizations.
2. Provide granular permission control.
3. Build economies around knowledge and information


## Prerequisites
---
This project is built on awesome work by the [IPFS](https://github.com/ipfs/ipfs), [Ethereum](https://www.ethereum.org), [OpenPGP](https://www.openpgp.org), [web3.py](https://github.com/pipermerriam/web3.py), and [py-ipfs](https://github.com/ipfs/py-ipfs-api) communities. 

The DDASH Installer, which currently supports Ubuntu 16.04 and Mac OS, installs all dependencies (including the Go Ethereum client, IPFS, the Python IPFS API, and gnupg).

## Precautions
The technologies used here are still in alpha. If you own cryptoassets such as Bitcoin and Ether, make sure you keep these on a completely separate machine. This software is still in development and has not been audited for security. Be very careful when enabling RPC while your accounts are unlocked. This can lead to Ethereum wallet attacks, hence the recommendation to keep your development environment completely separate from any real Ether you might own.

## Quickstart 
DDASH, the DDASH Installer, and the DDASH Network Utility currently support Ubuntu 16.04 and Mac OS X.

Use default settings to connect to the blackswan network.

Before you start, be sure you're running these scripts with appropriate permissions (usually sudo on Unix systems) and change file permissions of the *install.sh*, *deploy.sh*, and *manager.sh* bash scripts to allow execution:

```
chmod u+x install.sh deploy.sh dnu.sh
```

Navigate to the directory where you want to install DDASH and run:
```
./install.sh
```
This will install the Go Ethereum client, IPFS, and the necessary Python modules to allow DDASH to interface with these clients. 

To start the DDASH Networking Utility, run:
```
./dnu.sh
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

	/ddash
		crypto.py
		genesis.json
		bcinterface.py
		fsinterface.py
		ipfs.py
		main.py
		nodeInfo.ds
		
		/upload
		/download
        /source
		/data
	    	static-nodes.json

```
Save Ethereum contracts in the *source* directory with the .sol extension.
Contents of the *upload* directory are uploaded using the DDASH command with the same name. Blockchain contents are downloaded to the *download* directory using the DDASH command with the same name.

```
        _____  _____           _____ _    _ 
       |  __ \|  __ \   /\    / ____| |  | |
       | |  | | |  | | /  \  | (___ | |__| |
       | |  | | |  | |/ /\ \  \___ \|  __  |
       | |__| | |__| / ____ \ ____) | |  | |
       |_____/|_____/_/    \_\_____/|_|  |_|
                                                                
    ::: Distributed Data Sharing Hyperledger :::

    Welcome to the DDASH Command Line Interface.

[1]		ddash> sanity check
[2]		ddash> peer count
[3]		ddash> upload
[4]		ddash> download
[5]		ddash> hello
[6]		ddash> listen
[7]		ddash> broadcast
[8]		ddash> quit

```
The above commands:

[1]  check if IPFS daemon and Go Ethereum client are running

[2]  returns number of enodes found on chain

[3]  upload contents of *upload* directory to IPFS and save meta-data to blockchain.

[4]  query blockchain for file meta-data and download files from IPFS to *download* directory

[6] query blockchain for peer enodes

[7] broadcast client enode to blockchain


## Permissions management 
Data on the IPFS network cannot be removed and can be accessed by anyone who has your content hash. DDASH utilizes PGP keypair encryption to control permissions. This feature is still under development.

## Contribute
### Use cases
If you or your organization use DDASH to do something that would otherwise be impossible using a centralized system, please share your experience!

### Bug reports
You can submit bug reports using the [GitHub issue tracker](https://github.com/osmode/ddash/issues).

### Pull requests
Pull requests are welcome.

## Authors
MIT License (see *LICENSE* file for details).


# DDASH 
![DDASH Introduction](https://s3-us-west-1.amazonaws.com/ddash/ddash_intro.png)

:earth_americas: :rocket: :boom: :rocket: :earth_asia: :boom: :rocket: :boom: :earth_africa: :rocket: :boom: :rocket: :earth_americas:


## What is DDASH?
---
DDASH is a networking protocol for the exchange of distributed/locally hosted data and meta-data.

* One-click Ethereum coinification of any digital resource

* One-click creation of self-propagating Ethereum networks (no need for manual enode entry)

* One-click compilation and deployment of Ethereum contracts to any Ethereum blockchain 

* Optionally allows DApps to interface with the Interplanetary File System ([IPFS](https://github.com/ipfs/ipfs)) to minimize on-chain storage 

* Convert between private net Ether and main net Ether


## Legal Notice
This is a research protocol being developed at UCSF. This is not a tool for launching Initial Coin Offerings or issuing securities. Please familiarize yourself with laws that apply to your use case. U.S. users should refer to the U.S. Securities and Exchange Commission's [Statement on Cryptocurrencies and Initial Coin Offerings](https://www.sec.gov/news/public-statement/statement-clayton-2017-12-11). By using this software, you assume all responsibility for your actions. 

## Why DDASH?
Despite the wealth of data produced by academic institutions, research labs, hospitals, and corporations, only a small percentage of data is used to its fullest potential. DDASH is a blockchain networking protocol for exchanging data and meta-data in the form of Ethereum-based tokens.

### In its usual siloed state, data is a liability rather than an asset.

### DDASH turns data into digital assets.

DDASH enables one-click deployment of Ethereum networks. MD5 hashes of local or distributed data resources are hosted on chain against Ethereum-based tokens. DDASH optionally interfaces with IPFS to allow network administrators to host resources on IPFS and use the Ethereum blockchain as a permissions manager. 

Our goals are to:

1. Eliminate barriers to information exchange within and among organizations.
2. Provide granular permission control.
3. Build economies around knowledge and information


## Prerequisites
---
This project builds on work by the [Ethereum](https://www.ethereum.org), [web3.py](https://github.com/pipermerriam/web3.py), [IPFS](https://github.com/ipfs/ipfs) and [py-ipfs](https://github.com/ipfs/py-ipfs-api) communities. 

The DDASH Installer, which currently supports Ubuntu 16.04 and Mac OS, installs all dependencies (including the Go Ethereum client).

## Precautions
The technologies used here are still in alpha. If you own cryptoassets such as Bitcoin and Ether, make sure you keep these on a completely separate machine. This software is still in development. Be cautious when enabling RPC while your accounts are unlocked. This can lead to Ethereum wallet attacks, hence the recommendation to keep your development environment completely separate from any real Ether you might own.


## Quickstart 
DDASH, the DDASH Installer, and the DDASH Network Utility currently support Ubuntu 16.04 and Mac OS X. Use default settings to connect to the blackswan network.

Before you start, be sure you're running these scripts with appropriate permissions (usually sudo on Unix systems) and change file permissions of the *install.sh*, *deploy.sh*, *gui.sh* and *manager.sh* bash scripts to allow execution:

```
chmod u+x install.sh deploy.sh dnu.sh gui.sh
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

```
The above commands:

[1]  returns number of enodes found on chain

[2]  upload meta-data of *share* directory's contents to blockchain 

[3]  query blockchain for file meta-data

[5] query blockchain for peer enodes

[6] broadcast client enode to blockchain


## Contribute
### Use cases
If you or your organization use DDASH to do something that would otherwise be impossible using a centralized system, please share your experience!

### Bug reports
You can submit bug reports using the [GitHub issue tracker](https://github.com/osmode/ddash/issues).

### Pull requests
Pull requests are welcome.

## License
MIT License (see *LICENSE* file for details).


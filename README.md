DDASH - Ethereum Operating System
======================================================
[Github repository](https://github.com/osmode/ddash)

[Whitepaper](https://arxiv.org/abs/1709.07390)
------------------------------------------------------

![DDASH gif](https://s3-us-west-1.amazonaws.com/ddash/home.png)

## What is DDASH?
---
DDASH is an Ethereum operating system built around information exchange

* Transfer value and information among Ethereum networks

* Abstract creation of GUI interfaces for Ethereum contracts

* Sysadmin for Ethereum networks  

* Automate compilation and deployment of Ethereum contracts to any Ethereum blockchain 

* Optionally allows DApps to interface with the Interplanetary File System ([IPFS](https://github.com/ipfs/ipfs)) to minimize on-chain storage 


## Mission Statement

### Our goal is to build open economies for information exchange within and among organizations.

![DDASH - Ethereum operating system revolving around information exchange](https://s3-us-west-1.amazonaws.com/ddash/luxor.png)

## Manifesto 
The Manifesto contract allows participants to create a manifesto through a transparent voting process. Anyone can submit and vote on proposals. To interface with your own custom voting contracts (on any Ethereum network), simply replace the default Manifesto.sol address with your contract's address.


![Manifesto Contract](https://s3-us-west-1.amazonaws.com/ddash/manifesto5.png)

## Why DDASH?
DDASH combines the benefits of private Ethereum networks with the benefits of the Ethereum main network. DDASH allows Ethereum applications to run cheaply and securely on private Ethereum networks while enabling their integration with the main Ethereum network. The result is greatly reduced development and operational costs associated with private Ethereum networks, combined with the ability to transfer value and information among the main Ethereum network and private Ethereum networks.

## NFO Coin
NFO Coin is the utility token that powers DDASH, enabling the exchange of information and value across Ethereum networks. NFO Coin is based on the ERC20 standard. The NFO ABI and contract are located in the source directory and can be directly inspected at address 0x3100047369b54c34042B9DC138C02A0567D90A7a on the Ethereum main network.

### totalSupply: 10,000,000
### tokenName: NFO Coin
### tokenSymbol: NFO

There are 10,000,000 NFO Coin in circulation, which can be exchanged for Ether at a rate of 1,000 NFO Coin per 1 Ether.

NFO Coin and Ether can be exchanged using the DDASH client, which can be launched by running 
```
python3 gui.py 
```
## Quickstart 
DDASH, the DDASH Installer, and the DDASH Network Utility currently support Ubuntu 16.04 and Mac OS X.

Downlod or clone this repository to your machine, and navigate to that directory. Run:  
```
./install.sh
```
This will install the Go Ethereum client and the necessary Python modules to allow DDASH to interface with the client. The installation process can take a long time depending on which dependencies and libraries your machine already has. The installer will explicitly ask for permission to install each dependency via yes/no prompts.   

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

## How to acquire NFO Coin
Use the DDASH GUI to exchange Ether for NFO Coin. 
![NFO Coin](https://s3-us-west-1.amazonaws.com/ddash/nfocoin3.png)


## The DDASH Command Line Interface
DDASH also enables deployment of private Ethereum networks that can be joined without manually entering enode addresses via the DDASH Command Line Interface.
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
[2]		ddash> listen
[3]		ddash> broadcast

```
The above commands:

[1]  returns number of enodes found on chain

[2] query blockchain for peer enodes

[3] broadcast client enode to blockchain


## Contribute
Please take a look at our [contribution documentation](https://github.com/osmode/ddash/blob/master/docs/CONTRIBUTING.md) for information on how to report bugs, suggest enhancements, and contribute code. If you or your organization use DDASH to do something that would otherwise be impossible using traditional system, please share your experience! 

## Code of conduct
In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation. Read the full [Contributor Covenant](https://github.com/osmode/ddash/blob/master/docs/CODE_OF_CONDUCT.md). 

## Prerequisites
This project builds on work by the [Ethereum](https://www.ethereum.org), [web3.py](https://github.com/pipermerriam/web3.py), [IPFS](https://github.com/ipfs/ipfs) and [py-ipfs](https://github.com/ipfs/py-ipfs-api) communities. 

The DDASH Installer, which currently supports Ubuntu 16.04 and Mac OS, installs all dependencies (including the Go Ethereum client).

## License
[MIT License](https://github.com/osmode/ddash/blob/master/LICENSE) 


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
DDASH is a command line utility for Ethereum networking and blockchain application development. DDASH allows you to:

* Rapidly and automatically create private Ethereum networks

* Easily deploy Ethereum contracts to any Ethereum blockchain with a single command

* Allows DApps to interface with the Interplanetary File System ([IPFS](https://github.com/ipfs/ipfs)) to minimize on-chain storage 

* Upload and download data from commonly used formats (such as CSV) to an Etheruem blockchain, and vice versa


## Why DDASH?
---
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
DDASH, the DDASH Installer, and the DDASH Network Utility currently support Ubuntu 16.04. 

Before you start, be sure you're running these scripts with appropriate permissions (usually sudo on Unix systems) and change file permissions of the *installer.sh*, *deploy.sh*, and *manager.sh* bash scripts to allow execution:

```
chmod u+x installer.sh deploy.sh manager.sh
```

Navigate to the directory where you want to install DDASH and run:
```
./ installer.sh
```
This will install the Go Ethereum client, IPFS, and the necessary Python modules to allow DDASH to interface with these clients. 

To start the DDASH Networking Utility, run:
```
./ manager.sh
```

## Directory structure
The directory structure is important because DDASH and the DDASH Networking Utility look for certain files in certain directories. Your application will look something like this:
```
 /your_working_directory
     /ddash
	crypto.py
	genesis.json
	interface.py
	ipfs.py
	main.py

        /data
	    static-nodes.json

        /source
```
Save Ethereum contracts in the *source* directory with the .sol extension.

```
python main.py

        _____  _____           _____ _    _ 
       |  __ \|  __ \   /\    / ____| |  | |
       | |  | | |  | | /  \  | (___ | |__| |
       | |  | | |  | |/ /\ \  \___ \|  __  |
       | |__| | |__| / ____ \ ____) | |  | |
       |_____/|_____/_/    \_\_____/|_|  |_|
                                                                
    ::: Distributed Data Sharing Hyperledger :::

    Welcome to the DDASH Command Line Interface.

[1]   ddash> sanity check
      IPFS and geth appear to be running.
[2]   ddash> set directory /home/ucsf/ddash/gnupg
[3]   ddash> new key
[4]   ddash> show keys
[5]   ddash> use key 0
[6]   ddash> show accounts
[7]   ddash> use account 0
[8]   ddash> set recipient your_recipient's_pubkey_id 
[9]   ddash> set file /path/to/clinical/trial/data.csv
[10]  ddash> encrypt
[11]  ddash> upload
[12]  ddash> checkout QmUahy9JKE6Q5LSHArePowQ91fsXNR2yKafTYtC9xQqhwP
```
The above commands:

[1]  check if IPFS daemon and Go Ethereum client are running

[2]  specify working directory (need to have read/write permission)

[3]  generate a new PGP keypair 

[4]  list all PGP keypairs on your machine

[5]  uses the first (index 0) keypair as your identity

[6]  list Ethereum accounts

[7]  specify index of Ethereum account to use for transactions

[8]  specify an intended recipient's public key

[9]  upload the file to IPFS and create transaction containing the hash, user id of the person who uploaded the file, and recipient's public key id (or "public" indicating that it's not encrypted).

[10] encrypt file from step [9] using public key from step [8]

[11] upload file from [9] to IPFS network

[12] query blockchain using IPFS has as handle 


## Permissions management 
Data on the IPFS network cannot be removed and can be accessed by anyone who has your content hash. DDASH utilizes PGP keypair encryption to control permissions. The above examples demonstrated how to share data at IPFS address *QmRmE1vnc7mbEiqQv5SjrW3ctAmXXt4MQqbykenJmSqPuk*. If I only want Steven to be able to view the contents of this file, I'll encrypt the file using Steven's public key and upload it IPFS. The resulting IPFS hash, a description of the file, the owner, and the recipient's pubkey fingerprint (or "public") are saved on the blockchain.

## Contribute
### Use cases
If you or your organization use DDASH to do something that would otherwise be impossible using a centralized system, please share your experience!

### Bug reports
You can submit bug reports using the [GitHub issue tracker](https://github.com/osmode/ddash/issues).

### Pull requests
Pull requests are welcome.

## License
MIT License (see *LICENSE* file for details).


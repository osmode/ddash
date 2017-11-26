'''
:::  interface.py                                   :::
    ::: IPFS <> blockchain interface                :::
'''

import ipfsapi, os, json
from web3 import Web3, HTTPProvider, IPCProvider
from random import randint

# ipfs daemon needs to be running first


class Interface:

    # construct points to ddash contract address on blackswan Ethereum network
    # by default

    def __init__(self,host='localhost',port=5001):
        self.last_hash_added = None
        self.api = ipfsapi.connect(host='127.0.0.1',port=8080)
        # self.web3 = Web3(HTTPProvider('http://localhost:8545'))
	ipc_path = os.path.dirname(os.path.realpath(__file__))+'/data/geth.ipc'
	print "IPCProvider path: ",ipc_path
	self.web3 = Web3(IPCProvider(ipc_path))
        self.blockNumber = self.web3.eth.blockNumber
        self.eth_accounts = self.web3.personal.listAccounts
	self.account_index = 0
        
        self.tx = {}

        print "Initializing a DDASH Interface object."

    # contract_name is without the sol extension
    def load_contract(self,contract_name,sender_address=None,contract_address="0x535a338d14df9513909ec4d010ad3d2946da4014"):

	if not sender_address:
		sender_address = self.eth_accounts[0]

        self.tx['to'] = contract_address
        self.tx['from'] = sender_address
	abi = ''
	contract_name_lower = contract_name.lower()+'.abi'
	abi_path = os.path.dirname(os.path.realpath(__file__))+'/source/'+contract_name_lower
	
	print "Loading contract "+contract_name_lower
	print "from directory: "+abi_path
	print "Sender address: "+sender_address
	print "Contract address: "+contract_address
	print abi_path
	with open(abi_path,'r') as myfile:
		abi+=myfile.read()

        json_abi = json.loads(abi)
        self.contract = self.web3.eth.contract(abi=json_abi,address=contract_address)
        if self.contract: 
            print "You are now interfacing with contract at address "+contract_address



    def show_eth_accounts(self):
	if len(self.eth_accounts) ==0:
		print "You have no Ethereum accounts. Create a new account by typing 'new account'"
		return 0
	print "I found the following Ethereum accounts:"
	for i, acc in enumerate(self.eth_accounts):
		print i,"\t\t",acc

    def sanity_check(self):
        if not (self.api):
           print "I don't see IPFS running. Please make sure IPFS daemon is running first."
           return 1
        if not (self.blockNumber):
            print "I don't see geth running. Please run the go Ethereum client in the background."
            return 1
        if self.api and self.blockNumber:
            print "IPFS and geth appear to be running."
            return 0

    def random(self):
        assert(self.contract)
        assert(self.tx)

        i = randint(0,9)

        return self.contract.transact(self.tx).randomGen(i)

    def heyo(self):
        assert(self.contract)

        i = randint(0,4)
        print self.contract.call().greet_omar(i)
        return 0


    def upload(self,filepath):
        assert(os.path.isfile(filepath))
        assert(self.api)
        
        self.last_hash_added = result = self.api.add(filepath)
        if self.last_hash_added:
            print "'"+result['Name']+"' was uploaded to IPFS with hash:\n "+result['Hash']
            return result['Name'],result['Hash']

        print "Failed to upload file "+str(filepath)+" to IPFS"
        return 1


    # retrieve entry from blockchain using ipfs hash as handle
    def get_record(self,ipfs_hash):
	assert(self.contract)
        assert(self.tx)

	record = self.contract.call().get_record(ipfs_hash)
	if len(record) >0:
		print "I found this record:"		
		print "Row id: ",record[0]
		print "IPFS hash: ",record[1]
		print "Description: ",record[2]
		print "Shared with: ",record[3]
		print "Shared by: ",record[4]
		
		return record
	else:
		print "I didnt' find a record on the blockchain with that IPFS hash."
	return 0

    def push_ipfs_hash_to_chain(self,ipfs_hash,description,sender_id,recipient_id):
        assert(self.contract)
        assert(self.tx)
        if not self.last_hash_added: 
            print "You must upload a file to IPFS first. Try Interface.upload(filepath)."
            return 1
        if not (ipfs_hash): 
            print "No IPFS hash specified. You must specify an IPFS hash to add to the blockchain."
            return 1
        if not (description):
            print "No description provided. You must describe the IPFS hash you're adding to the blockchain."
            return 1
        if not sender_id:
            print "No sender provided. You must specify a sender's pubkey id." 
            return 1
        if not recipient_id:
            print "No recipient provided. YOu must specify the recipient's pubkey id (if the resource is encrypted) or \'public\'."
            return 1

        tx_hash = self.contract.transact(self.tx).add_record(ipfs_hash,description,recipient_id,sender_id)

        print "New record added to blockchain. Object at IPFS hash "+ipfs_hash+" was shared with "+recipient_id+" by user "+sender_id+"."

        return tx_hash

    # unlock selected Ethereuma account
    def unlock_account(self, password):
	if len(self.eth_accounts) ==0: 
	    print "No Ethereum account found. Create a new account by typing 'new account'"
	else:
	    self.web3.personal.unlockAccount(self.eth_accounts[self.account_index],password)    


    # select Ethereum account
    def set_account(self,index):
	if len(self.eth_accounts) ==0:
		print "No Ethereum account found. Create a new account by typing 'new account'"

	elif index >= len(self.eth_accounts):
		print "Invalid index."
	else:
		self.account_index = index
		#self.load_contract(sender_address=self.eth_accounts[self.account_index])
		

    # get number of enodes on the blockchain
    def friend_count(self):
	print str(self.contract.call().get_entity_count())+" enodes found on the blockchain."
	return 0


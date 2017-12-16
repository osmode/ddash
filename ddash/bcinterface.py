'''
:::  interface.py								   :::
	::: IPFS <> blockchain interface				:::
'''

import ipfsapi, os, json
from web3 import Web3, HTTPProvider, IPCProvider
from random import randint

# ipfs daemon needs to be running first


class BCInterface:

	# construct points to ddash contract address on blackswan Ethereum network
	# by default

	def __init__(self,host='localhost',port=5001,mainnet=False):
		self.last_hash_added = None
		#self.api = ipfsapi.connect(host='127.0.0.1',port=port)
		# self.web3 = Web3(HTTPProvider('http://localhost:8545'))
		if mainnet:
			ipc_path=os.path.dirname(os.path.realpath(__file__))+'/data_mainnet/geth.ipc'
		else:
			ipc_path = os.path.dirname(os.path.realpath(__file__))+'/data/geth.ipc'
		print("IPCProvider path: ",ipc_path)
		self.web3 = Web3(IPCProvider(ipc_path))
		self.blockNumber = self.web3.eth.blockNumber
		self.eth_accounts = self.web3.personal.listAccounts
		self.account_index = 0
		self.ethereum_acc_pass = None
		
		self.tx = {}

		print("Initializing a DDASH Interface object.")

		# log Ethereum accounts to ddash/swap/
		self.write_ethereum_address(mainnet)

	# contract_name is without the sol extension
	def load_contract(self,contract_name,sender_address=None,contract_address="0x40a4dcb3fdcbaa00848d2c14386abed56797bf61"):

		if not sender_address:
			sender_address = self.eth_accounts[0]

		self.tx['to'] = contract_address
		self.tx['from'] = sender_address
		abi = ''
		contract_name_lower = contract_name.lower()+'.abi'
		abi_path = os.path.dirname(os.path.realpath(__file__))+'/source/'+contract_name_lower
	
		print("Loading contract "+contract_name_lower)
		print("from directory: "+abi_path)
		print("Sender address: "+sender_address)
		print("Contract address: "+contract_address)
		print(abi_path)
		with open(abi_path,'r') as myfile:
			abi+=myfile.read()

		json_abi = json.loads(abi)
		self.contract = self.web3.eth.contract(abi=json_abi,address=contract_address)
		if self.contract: 
			print("You are now interfacing with contract at address "+contract_address)


	def show_eth_accounts(self):
		if len(self.eth_accounts) ==0:
			print("You have no Ethereum accounts. Create a new account by typing 'new account'")
			return 0

		print("I found the following Ethereum accounts:")
		for i, acc in enumerate(self.eth_accounts):
			print(i,"\t\t",acc)
	
	def get_eth_accounts(self):
		if len(self.eth_accounts) == 0:
			print("You have no Ethereum accounts. Create a new account by typing 'new account'")
			return 0
		return self.eth_accounts

	def sanity_check(self):
		if not (self.api):
		   print("I don't see IPFS running. Please make sure IPFS daemon is running first.")
		   return 1
		if not (self.blockNumber):
			print("I don't see geth running. Please run the go Ethereum client in the background.")
			return 1
		if self.api and self.blockNumber:
			print("IPFS and geth appear to be running.")
			return 0

	def random(self):
		assert(self.contract)
		assert(self.tx)

		i = randint(0,9)

		return self.contract.transact(self.tx).randomGen(i)

	def heyo(self):
		assert(self.contract)

		i = randint(0,4)
		print(self.contract.call().greet_omar(i))
		return 0


	def upload_to_ipfs(self,filepath):
		assert(os.path.isfile(filepath))
		assert(self.api)
		
		self.last_hash_added = result = self.api.add(filepath)
		if self.last_hash_added:
			print("'"+result['Name']+"' was uploaded to IPFS with hash:\n "+result['Hash'])
			return result['Name'],result['Hash']

		print("Failed to upload file "+str(filepath)+" to IPFS")
		return 1


	def add_record(self,owner_address,filename,ipfs_hash,description):
		print("adding record to blockchain:")
		print("owner_adddress:",owner_address)
		print("filename:",filename)
		print("ipfs_hash:",ipfs_hash)
		print("description",description)

		return self.contract.transact(self.tx).addRecord(ipfs_hash,filename,description)

	def get_record_by_row(self,row):
	
		self.contract.transact(self.tx).getRecordByRow(row)
		return self.contract.call().getRecordByRow(row)

	def get_record_by_ipfs_hash(self,ipfs_hash):
		self.contract.transact(self.tx).get_record_by_ipfs_hash(ipfs_hash)
		return self.contract.call().get_record_by_ipfs_hash(ipfs_hash)

	def get_record_count(self):
		self.contract.transact(self.tx).getRecordCount()
		return self.contract.call().getRecordCount()

   # unlock selected Ethereum account
	def unlock_account(self, password):
		if len(self.eth_accounts) ==0: 
			print("No Ethereum account found. Create a new account by typing 'new account'")
		else:
			print("Attempting to unlock account ",str(self.eth_accounts[self.account_index]))

			self.web3.personal.unlockAccount(self.eth_accounts[self.account_index],password)	


		# select Ethereum account
	def set_account(self,index):
		if len(self.eth_accounts) ==0:
			print("No Ethereum account found. Create a new account by typing 'new account'")

		elif index >= len(self.eth_accounts):
			print("Invalid index.")
		else:
			print("You are now using account index ",index)
			self.account_index = index
		#self.load_contract(sender_address=self.eth_accounts[self.account_index])
		
	# get number of enodes on the blockchain
	def peer_count(self):
		print(str(self.contract.call().get_entity_count())+" enodes found on the blockchain.")
		return 0

	def get_balance(self):
		return self.web3.eth.getBalance(self.eth_accounts[0])

	def get_address(self):
		return self.eth_accounts[0]

	def write_ethereum_address(self,mainnet=False):
	
		swap_path = os.path.dirname(os.path.realpath(__file__))+'/swap/eth_addresses.ds'
		file_text=''

		if os.path.isfile(swap_path):
			with open(swap_path,'r') as myfile:
				file_text+=myfile.read()
		
		if self.eth_accounts[0]:
			if self.eth_accounts[0] not in file_text:
				with open(swap_path,'a') as fileout:
					if mainnet:
						fileout.write('mn:'+self.eth_accounts[0]+'\n')
					else:
						fileout.write('pn:'+self.eth_accounts[0]+'\n')

			
	def get_ethereum_address(self):
		swap_path = os.path.dirname(os.path.realpath(__file__))+'/swap/eth_addresses.ds'
		file_text=''
		mainnet_eth_address = None
		privatenet_eth_address = None

		if os.path.isfile(swap_path):
			with open(swap_path,'r') as myfile:
				file_text+=myfile.read()
				x = file_text.split('pn:')
				y = x[1].split('mn:')
				privatenet_eth_address = y[0]
				mainnet_eth_address = y[1]

		self.privatenet_eth_address = privatenet_eth_address
		self.mainnet_eth_address = mainnet_eth_address

		return privatenet_eth_address, mainnet_eth_address

	def increase_gas(self,exp):
		if 'gas' not in self.tx.keys():
			self.tx['gas'] = 10000
		new_gas_value = self.tx['gas'] * 10**exp
		print("Increasing gas to ", new_gas_value)
		self.tx['gas'] = new_gas_value
		return new_gas_value

	def decrease_gas(self,exp):
		if 'gas' not in self.tx.keys():
			self.tx['gas'] = 10000
		new_gas_value = self.tx['gas'] / 10**exp
		print("Decreasing gas to ", new_gas_value)
		self.tx['gas'] = new_gas_value
		return new_gas_value



			

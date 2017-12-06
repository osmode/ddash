'''
:::  swapinterface.py								   :::
:::  The SWAP Protocol is outlined here: 
:::  https://omarmetwally.blog/2017/12/05/converting-between-private-net-ether-and-real-ether-the-ddash-protocol/ 
:::  SWAP.sol is a contract that allows 2 different blockchains to sync
:::  and transfer value. The contract is deployed on both blockchains, and
:::  the synchronization process involves the local filesystem.
:::  @class SwapInterface() interfaces with the Go-Ethereum client
:::  and inherits from @class BCInterface
:::  Author:  Omar Metwally, MD (omar.metwally@gmail.com)
'''

import ipfsapi, os, json
from web3 import Web3, HTTPProvider, IPCProvider
from random import randint
from bcinterface import *

# ipfs daemon needs to be running first


class SwapInterface(BCInterface):

	# construct points to ddash contract address on blackswan Ethereum network
	# by default
	def __init__(self,host='localhost',port=5001,mainnet=False):
		BCInterface.__init__(self,host='localhost',port=5001,mainnet=False)

	# contract_name is without the sol extension
	def load_contract(self,contract_name='swap',sender_address=None,contract_address="0xfe1d9f990d92a73e0851e863921838453f235ff4"):

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

	def write_swap_transactions_to_file(self):
		swap_path = os.path.dirname(os.path.realpath(__file__))+'/swap/swap_transactions.ds'

		file_text=''
		privatenet_eth_address,mainnet_eth_address = self.get_ethereum_address()
		if not (privatenet_eth_address and mainnet_eth_address):
			print("No Ethereum account addresses found for private net(s) and mainnet.")	
			return 1

		if os.path.isfile(swap_path):
			with open(swap_path,'r') as myfile:
				file_text+=myfile.read()

		num_swap_tx = self.contract.call().get_transaction_count()
		i=0
		fileout = open(swap_path,'a')

		while i < num_swap_tx:
			row = self.contract.call().get_transaction_by_row(i)

			# check if transaction has already exists in local file
			if row[6] in file_text:
				print("skipping swap transaction with hash: "+row[6])
				return 1

			for index, val in row:
					fileout.write(val+'\t')
			fileout.write('\n')


	def read_swap_transactions_from_file(self):
		swap_path = os.path.dirname(os.path.realpath(__file__))+'/swap/swap_transactions.ds'		
		if not os.path.isfile(swap_path):
			print("file /swap/swap_transactions.ds was not found.")
			return 1
	
		for line in open(swap_path):
			fields=line.split('\t')
			if len(fields) < 7:
				print("Invalid number of fields decoded from /swap/swap_transactions.ds")
				return 1

			pvn_to_ether_amt = fields[0]
			eth_to_pvn_amt = fields[1]
			eth_address = fields[2]
			pvn_address = fields[3]
			exchange_rate = fields[4]
			timestamp = fields[5]
			swap_tx_hash = fields[6]

			print("Entering transaction into blockchain if it doesn't already exist: ")
			print(pvn_to_ether_amt,eth_to_pvn_amt,eth_address,pvn_address,exchange_rate,timestamp,swap_tx_hash)
			self.contract.transact(self.tx).new_transaction(pvn_to_ether_amt,eth_to_pvn_amt,eth_address,pvn_address,exchange_rate,timestamp,swap_tx_hash)


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

import os, json
from web3 import Web3, HTTPProvider, IPCProvider
from random import randint
from bcinterface import *
from time import sleep

mainnet_swap_address = "0xed8c634ac8c2fa3694c32cb01b96a6912f8a7738"
blackswan_swap_address = "0x5fced4408a9ff19091a97a616e8432d00b808098"

class SwapInterface(BCInterface):

	# construct points to ddash contract address on blackswan Ethereum network
	# by default
	def __init__(self,host='localhost',port=5001,mainnet=False):
		BCInterface.__init__(self,host='localhost',port=5001,mainnet=mainnet )

	# contract_name is without the sol extension
	def load_contract(self, mainnet, contract_name='swap2', contract_address=None):
	
		if mainnet:
			contract_address = mainnet_swap_address
		else:
			contract_address = blackswan_swap_address

		sender_address = self.eth_accounts[self.account_index]

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

	def new_swap_transaction(self, pvn_to_eth_token_amt, eth_to_pvn_token_amt, eth_address, pvn_address, tx_hash):
		self.contract.transact(self.tx).swap_transaction( pvn_to_eth_token_amt, eth_to_pvn_token_amt, eth_address, pvn_address, tx_hash)

	def get_transaction_count(self):
		num_tx = self.contract.call().get_transaction_count()
		print(num_tx," SWAP transactions found on chain.")
	
	def get_transaction_by_row(self, row):
		print("SWAP transaction: ",str(row))
		return self.contract.call().get_transaction_by_row(row)
		
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
		print(num_swap_tx," SWAP transactions found on chain.")
		i=0
		fileout = open(swap_path,'a')

		while i < num_swap_tx:
			row = self.contract.call().get_transaction_by_row(i)
			print("write_swap_transactions_to_file row:",str(row))

			# check if transaction has already exists in local file
			if row[6] in file_text:
				print("skipping swap transaction with hash: "+row[6])
				return 1

			for i,v in enumerate(row):
				if type(v) is int:
					fileout.write(str(v)+'\t')
				elif i ==6:
					fileout.write( v )
					fileout.write('\t')
				else:
					fileout.write(v+'\t')
			fileout.write('\n')
			i+=1


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

			pvn_to_eth_amt = int(fields[0])
			eth_to_pvn_amt = int(fields[1])
			# CAVEAT - web3py does not recognize addresses
			# as such unless all characters are lowercase
			eth_address = str(fields[2]).lower()
			pvn_address = str(fields[3]).lower()
			exchange_rate = int(fields[4])
			timestamp = int(fields[5])
			swap_tx_hash = bytes(fields[6], encoding='utf8').decode("utf8")
			print("swap_tx_hash ",swap_tx_hash," is type ")
			print(type(swap_tx_hash))

			print("Entering transaction into blockchain if it doesn't already exist: ")
			print(pvn_to_eth_amt,eth_to_pvn_amt,eth_address,pvn_address,exchange_rate,timestamp,swap_tx_hash)
			# THIS NEEDS FIXING 
			# need a way to convert bytes object swap_tx_hash into bytes32
			self.contract.transact(self.tx).swap_transaction(pvn_to_eth_amt,eth_to_pvn_amt,eth_address,pvn_address,swap_tx_hash) 
			sleep(1000)

	'''
	@method my_token_balance 
	returns SwapCoin balance for currently selected Ethereum account
	'''
	def my_token_balance(self):
		token_balance = self.contract.call().get_token_balance(self.eth_accounts[self.account_index])
		print("Your Ethereum address: ",self.eth_accounts[self.account_index])
		print("Your SwapCoin balance: ",token_balance)
		
		return token_balance

	def get_token_balance(self, address):
		token_balance = self.contract.call().get_token_balance(address)
		print("Main net Ethereum address: ",address)
		print("Main net SwapCoin balance: ",token_balance)
		return token_balance

	def get_pvn_token_balance(self, address):
		pvn_token_balance = self.contract.call().get_pvn_token_balance(address)
		print("Black Swan Ethereum address: ",address)
		print("Black Swan SwapCoin balance: ",pvn_token_balance)
		return token_balance

	def buy_tokens(self, amount):
		print("Trying to buy ",amount," tokens...")
		self.tx['value'] = int(amount)
		tx = self.contract.transact(self.tx).buy()
		return tx


	def sell_tokens(self, amount):
		print("Trying to sell ",amount," tokens...")
		tx = self.contract.transact(self.tx).sell(int(amount)) 
		return tx

	def transfer_token(self, recipient_address, amount):
		print("Trying to transfer ",amount," tokens to ",recipient_address)
		tx = self.contract.transact(self.tx).transfer_token(recipient_address, amount)
		return tx

	# Send SwapCoin between 2 different Ethereum networks
	def swap_transaction(self, pvn_to_eth_token_amt, eth_to_pvn_token_amt, eth_addr, pvn_addr, txHash):
		print("Initiated SWAP transaction...")
		tx = self.contract.transact(self.tx).swap_transaction( pvn_to_eth_token_amt, eth_to_pvn_token_amt, eth_addr, pvn_addr, txHash)
		return tx

	def set_gas(self, value):
		print("Setting gas to: ",value)
		if 'gas' not in self.tx.keys():
			self.tx['gas'] = value 
		self.tx['gas'] = value



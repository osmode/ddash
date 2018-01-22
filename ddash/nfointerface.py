'''
--------------------------------------------
nfointerface.py
--------------------------------------------
Distributed Data Sharing Hyperledger (DDASH)
NFO Coin Interface to interact with NFO Coin 
contract. The NFO Coin Protocol is outlined 
here:
https://omarmetwally.blog/2017/12/05/converting-between-private-net-ether-and-real-ether-the-ddash-protocol/ 
nfocoin.sol is a contract that allows 2 different blockchains to sync
and transfer value. The contract is deployed on both blockchains, and
the synchronization process involves the local filesystem.
@class NFOInterface() interfaces with the Go-Ethereum client
and inherits from @class BCInterface
--------------------------------------------
Omar Metwally, MD (omar.metwally@gmail.com)
https://github.com/osmode/ddash
--------------------------------------------
'''
import os, json
from web3 import Web3, HTTPProvider, IPCProvider
from random import randint
from bcinterface import *
from time import sleep
from time import time

mainnet_nfo_address = "0x3100047369b54c34042b9dc138c02a0567d90a7a"
blackswan_nfo_address = "0x38a779dd481b5f812b76b039cb2077fb124677a7" 

class NFOInterface(BCInterface):

	# construct points to ddash contract address on blackswan Ethereum network
	# by default
	def __init__(self,host='localhost',port=5001,mainnet=False):
		BCInterface.__init__(self,host='localhost',port=5001,mainnet=mainnet )

	# contract_name is without the sol extension
	def load_contract(self, mainnet, contract_name='nfocoin', contract_address=None):
	
		if mainnet:
			contract_address = mainnet_nfo_address
		else:
			contract_address = blackswan_nfo_address

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

	def new_nfo_transaction(self, pvn_to_eth_token_amt, eth_to_pvn_token_amt, eth_address, pvn_address, tx_hash):
		self.contract.transact(self.tx).nfo_transaction( pvn_to_eth_token_amt, eth_to_pvn_token_amt, eth_address, pvn_address, tx_hash)

	def get_transaction_count(self):
		num_tx = self.contract.call().get_transaction_count()
		print(num_tx," NFO transactions found on chain.")
	
	def get_transaction_by_row(self, row):
		print("NFO transaction: ",str(row))
		return self.contract.call().get_transaction_by_row(row)
		
	def write_nfo_transaction_to_file(self, send_nfocoin_amount, send_nfocoin_address, send_nfo_tx_hash):
		nfo_path = os.path.dirname(os.path.realpath(__file__))+'/nfo/nfo_transactions.ds'
		file_text=''
		sender_address = self.tx['from']
		if not (sender_address and send_nfocoin_address):
			print("Please specify sender and recipient addresses.")
			return 1

		if os.path.isfile(nfo_path):
			with open(nfo_path,'r') as myfile:
				file_text+=myfile.read()
		row = [0, send_nfocoin_amount, sender_address, send_nfocoin_address, 1000, int(str(time()).split('.')[0]), send_nfo_tx_hash]
		# check if transaction has already exists in local file
		if row[6] in file_text:
			print("skipping nfo transaction with hash: "+row[6])
			return 1
	
		print("Attempting to write send NFO Coin transaction to file:",row)
		fileout = open(nfo_path,'a')
		for i,v in enumerate(row):
			if type(v) is int:
				fileout.write(str(v)+'\t')
			elif i ==6:
				fileout.write( v )
				fileout.write('\t')
			else:
				fileout.write(v+'\t')
		fileout.write('\n')

	def write_nfo_transactions_to_file(self):
		nfo_path = os.path.dirname(os.path.realpath(__file__))+'/nfo/nfo_transactions.ds'

		file_text=''
		privatenet_eth_address,mainnet_eth_address = self.get_ethereum_address()
		if not (privatenet_eth_address and mainnet_eth_address):
			print("No Ethereum account addresses found for private net(s) and mainnet.")	
			return 1

		if os.path.isfile(nfo_path):
			with open(nfo_path,'r') as myfile:
				file_text+=myfile.read()

		num_nfo_tx = self.contract.call().get_transaction_count()
		print(num_nfo_tx," NFO transactions found on chain.")
		i=0
		fileout = open(nfo_path,'a')

		while i < num_nfo_tx:
			row = self.contract.call().get_transaction_by_row(i)
			print("write_nfo_transactions_to_file row:",str(row))

			# check if transaction has already exists in local file
			if row[6] in file_text:
				print("skipping nfo transaction with hash: "+row[6])
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


	def read_nfo_transactions_from_file(self):
		nfo_path = os.path.dirname(os.path.realpath(__file__))+'/nfo/nfo_transactions.ds'		
		if not os.path.isfile(nfo_path):
			print("file /nfo/nfo_transactions.ds was not found.")
			return 1
	
		for line in open(nfo_path):
			fields=line.split('\t')
			if len(fields) < 7:
				print("Invalid number of fields decoded from /nfo/nfo_transactions.ds")
				return 1

			pvn_to_eth_amt = int(fields[0])
			eth_to_pvn_amt = int(fields[1])
			# CAVEAT - web3py does not recognize addresses
			# as such unless all characters are lowercase
			eth_address = str(fields[2]).lower()
			pvn_address = str(fields[3]).lower()
			exchange_rate = int(fields[4])
			timestamp = int(fields[5])
			nfo_tx_hash = bytes(fields[6], encoding='utf8').decode("utf8")
			print("nfo_tx_hash ",nfo_tx_hash," is type ")
			print(type(nfo_tx_hash))

			print("Entering transaction into blockchain if it doesn't already exist: ")
			print(pvn_to_eth_amt,eth_to_pvn_amt,eth_address,pvn_address,exchange_rate,timestamp,nfo_tx_hash)
			# THIS NEEDS FIXING 
			# need a way to convert bytes object nfo_tx_hash into bytes32
			self.contract.transact(self.tx).nfo_transaction(pvn_to_eth_amt,eth_to_pvn_amt,eth_address,pvn_address,nfo_tx_hash) 
			sleep(1000)

	'''
	@method my_token_balance 
	returns NFOCoin balance for currently selected Ethereum account
	'''
	def my_token_balance(self):
		token_balance = self.contract.call().get_token_balance(self.eth_accounts[self.account_index])
		#print("Your Ethereum address: ",self.eth_accounts[self.account_index])
		#print("Your NFOCoin balance: ",token_balance)
		
		return token_balance

	def get_token_balance(self, address):
		token_balance = self.contract.call().get_token_balance(address)
		#print("Main net Ethereum address: ",address)
		#print("Main net NFOCoin balance: ",token_balance)
		return token_balance

	def get_pvn_token_balance(self, address):
		pvn_token_balance = self.contract.call().get_pvn_token_balance(address)
		print("Black Swan Ethereum address: ",address)
		print("Black Swan NFOCoin balance: ",pvn_token_balance)
		return token_balance

	def buy_tokens(self, amount):
		print("Trying to buy tokens worth "+str(amount)+" ether.")
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

	# Send NFOCoin between 2 different Ethereum networks
	def nfo_transaction(self, pvn_to_eth_token_amt, eth_to_pvn_token_amt, eth_addr, pvn_addr, txHash):
		print("Initiated NFO transaction...")
		tx = self.contract.transact(self.tx).nfo_transaction( pvn_to_eth_token_amt, eth_to_pvn_token_amt, eth_addr, pvn_addr, txHash)
		return tx

	def set_gas(self, value):
		if 'gas' not in self.tx.keys():
			self.tx['gas'] = value 
		self.tx['gas'] = value



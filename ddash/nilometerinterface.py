'''
:::  nilometer.py								   
:::  Nilometer.sol is a contract for trading commodities based on
:::  the Nile River's water levels.
:::  Building Ethereum Dapps for a peaceful and prosperous African continent.
:::  Author:  Omar Metwally, MD (omar.metwally@gmail.com)
'''
import os, json
from web3 import Web3, HTTPProvider, IPCProvider
from random import randint
from bcinterface import *
from time import sleep

#mainnet_manifesto = "0xed8c634ac8c2fa3694c32cb01b96a6912f8a7738"
mainnet_nilometer_address = "0x0"
blackswan_nilometer_address = "0xa26d59d26d3d66c0988fad233c5a21a608566dbd"

class NilometerInterface(BCInterface):

	# construct points to ddash contract address on blackswan Ethereum network
	# by default
	def __init__(self,host='localhost',port=5001,mainnet=False):
		BCInterface.__init__(self,host='localhost',port=5001,mainnet=mainnet )

	# contract_name is without the sol extension
	def load_contract(self, mainnet, contract_name='nilometer', contract_address=None):
	
		if mainnet and not contract_address:
			contract_address = mainnet_nilometer_address
		if not mainnet and not contract_address:
			contract_address = blackswan_nilometer_address

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

	def new_record(self, waterlevel):
		print("Saving new waterlevel "+str(waterlelve)+" on the blockchain with timestamp "+str(timestamp))
		tx = self.contract.transact(self.tx).newRecord(waterlevel)
		return tx

	def new_proposal(self, minWaterLevel, supportAmount): 
		tx = self.contract.transact(self.tx).newProposal(minWaterLevel, supportAmount) 
		return tx
	
	def get_vote_count(self):
		count = self.contract.call().get_vote_count()
		return count

	# count how many votes (and how much associated Ether) support a Nile water level
	# of at least waterlevel
	def tally_votes_over(self, waterlevel):
		proposal = self.contract.call().get_proposal_by_row(row)
		return proposal

	def set_gas(self, value):
		if 'gas' not in self.tx.keys():
			self.tx['gas'] = value 
		self.tx['gas'] = value



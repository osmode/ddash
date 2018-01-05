'''
:::  manifestointerface.py								   :::
:::  Manifesto.sol is a contract that allows stakeholders to submit proposals
:::  and vote on proposals.
:::  @class ManifestoInterface() interfaces with the Go-Ethereum client
:::  and inherits from @class BCInterface
:::  Author:  Omar Metwally, MD (omar.metwally@gmail.com)
'''
import os, json
from web3 import Web3, HTTPProvider, IPCProvider
from random import randint
from bcinterface import *
from time import sleep

#mainnet_manifesto = "0xed8c634ac8c2fa3694c32cb01b96a6912f8a7738"
mainnet_manifesto_address = "0x0"
blackswan_manifesto_address = "0xf6e870db7475ad404e963f9ab63a9084c85257e7"

class ManifestoInterface(BCInterface):

	# construct points to ddash contract address on blackswan Ethereum network
	# by default
	def __init__(self,host='localhost',port=5001,mainnet=False):
		BCInterface.__init__(self,host='localhost',port=5001,mainnet=mainnet )

	# contract_name is without the sol extension
	def load_contract(self, mainnet, contract_name='manifesto', contract_address=None):
	
		if mainnet and not contract_address:
			contract_address = mainnet_manifesto_address
		if not mainnet and not contract_address:
			contract_address = blackswan_manifesto_address

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

	def new_proposal(self, description):
		print("self.contract.transact(self.tx).newProposal("+description+")")

		tx = self.contract.transact(self.tx).newProposal(description)
		return tx

	def vote(self, proposalID, vote):
		tx = self.contract.transact(self.tx).vote(proposalID, vote)
		return tx
	
	def tally_votes(self, proposalID):
		tx = self.contract.transact(self.tx).executeProposal(proposalID)
		return tx

	def changeVotingRules(self, minimumSharesToPassAVote, minutesForDebate):
		tx = self.contract.transact(self.tx).changeVotingRules(minimumSharesToPassAVote, minutesForDepate)
		return tx

	def setShares(self, shareholder, shares):
		tx = self.contract.transact(self.tx).setShares(shareholder, shares)
		return tx

	def get_proposal_count(self):
		count = self.contract.call().get_proposal_count()
		return count

	def get_proposal_by_row(self,row):
		proposal = self.contract.call().get_proposal_by_row(row)
		return proposal

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
	'''

	def set_gas(self, value):
		if 'gas' not in self.tx.keys():
			self.tx['gas'] = value 
		self.tx['gas'] = value



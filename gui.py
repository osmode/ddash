'''
--------------------------------------------
gui.py
--------------------------------------------
Distributed Data Sharing Hyperledger (DDASH)
Twin Peaks graphical user interface for
--------------------------------------------
Omar Metwally, MD (omar.metwally@gmail.com)
https://github.com/osmode/ddash
--------------------------------------------
'''
from tkinter import simpledialog, messagebox
from tkinter import *
from tkinter.font import Font
from tkinter import ttk
import subprocess, os
from subprocess import call
import sys, datetime

sys.path.insert(0, os.path.join(os.getcwd(),'ddash'))
from bcinterface import *
from fsinterface import * 
from nfointerface import *
from manifestointerface import *
from nilometerinterface import *
from getpass import getpass
import time, atexit


# Flags to instruct DDASH to broadcast enode address to blockchain
# and query blockchain for peer enodes
BROADCAST=False
LISTEN=False
blackswan_contract_address="0x5ff2ce40e82e52d370fa9a0ddf49aeee32184756"
#recordmanager_contract_address="0xcc109bf72338909ead31a5bf46d8d8fa455ff09b"
mainnet_nfo_address = "0x3100047369b54c34042b9dc138c02a0567d90a7a"
blackswan_nfo_address = "0x38a779dd481b5f812b76b039cb2077fb124677a7"

# available Ethereum networks
NETWORK_OPTIONS = [ "Black Swan network", "Main Ethereum network" ]
# list of available contracts to interface with
CONTRACT_OPTIONS = [ "Manifesto", "NFO Coin", "Nilometer" ]
# list of Ethereum accounts, popuated at runtime
ACCOUNT_OPTIONS = []
# list of proposals from the Manifesto.sol contract
PROPOSALS = []
# logo displayed in upper left corner
intro = r"""ddash"""

'''
@class TwinPeaks
Represents the ddash graphical user interface 
Built on tkinter (Python 3)
'''
class TwinPeaks:
	def __init__(self, master):
		self.master = master
		master.title("ddash")
		# @variable self.network can be main net, blackswan, or another private net
		self.network=None
		# @variable self.context represents the current contract, or the home screen
		self.context = "home"
		# @variable self.network_variable populates the Ethereum network
		# dropdown on the home screen. Default is main net
		self.network_variable = StringVar()
		self.network_variable.set(NETWORK_OPTIONS[1])
		self.account_variable = StringVar(self.master)
		# @variable self.bci is initialized to a @class BCInterface object
		# which interfaces with Ethereum contracts pythonically via web3
		self.bci = None
		# @variable self.fsi is initialized to a @class FSInterface object,
		# which interfaces with the local file system
		self.fsi = None
		# @variable self.nfointerface is initialized to a @class NFOInterface object
		# which interfaces with the NFO Coin Ethereum contract pythonically  via web3
		self.nfointerface = None
		# remember the last Ethereum account password entered
		self.ethereum_acc_pass = None
		self.ready = False
		# in the Manifesto.sol context, used to tally votes
		self.last_selected_proposalID = None

	'''
	@method handle_send_nfocoin [NFO Coin Context]
	Transfer NFO Coin within a network (Intra-Network) or between
	two networks (Inter-Network).
	Called when the "Send" button is clicked
	'''
	def handle_send_nfocoin(self):
		if not hasattr(self,'nfointerface'):
			print("No nfointerface object.")
			return
		print("Attempting to unlock account...")
		self.nfointerface.unlock_account(self.ethereum_acc_pass)

		send_transaction_type = send_nfocoin_choice.get()
		if not send_transaction_type:
			print("No transaction type selected. Please select Intra-Network or Intra-Network NFO Coin transfer")
			return
		send_nfocoin_amount = int(send_nfocoin_amount_entry.get())
		if not send_nfocoin_amount:
			print("No NFO Coin amount specified.")
			return
		send_nfocoin_address = str(send_nfocoin_address_entry.get())
		if not send_nfocoin_address:
			print("No NFO Coin recipient address specified.")
			return
		timestamp=int(str(time.time()).split('.')[0])
		# transfer value on the same network
		if send_transaction_type == "intra":
			print("Initiating Intra-Network NFO Coin transfer...")
			print("Recipient: ",send_nfocoin_address)
			print("NFO Coin amount: ",send_nfocoin_amount)
			# transfer NFO Coin and return transaction hash
			return self.nfointerface.transfer_token(send_nfocoin_address, send_nfocoin_amount)

		# transfer value between 2 different networks
		if send_transaction_type == "inter":
			print("Initiating Inter-Network NFO Coin transfer...")
			print("Recipient: ",send_nfocoin_address)
			print("NFO Coin amount: ",send_nfocoin_amount)
			# generate hash 
			print("make_hash_parameters:")
			print("From: ",self.nfointerface.tx['from'])
			print("timestamp: ", timestamp)
			send_nfocoin_tx_hash = self.nfointerface.contract.call().make_hash(int(0), send_nfocoin_amount, str(self.nfointerface.tx['from']), send_nfocoin_address, int(1000), timestamp)
			# transfer NFO Coin and create record of transfer on blockchain
			self.nfointerface.new_nfo_transaction(0, send_nfocoin_amount, self.nfointerface.tx['from'], send_nfocoin_address, send_nfocoin_tx_hash)
			# write transaction to local file system
			self.nfointerface.write_nfo_transaction_to_file(send_nfocoin_amount, send_nfocoin_address, send_nfocoin_tx_hash)
			# transfer NFO Coin:w and return transaction hash
			#return self.nfointerface.transfer_token(send_nfocoin_address, send_nfocoin_amount)
			return send_nfocoin_tx_hash

	'''
	@method handle_selected_contract
	Place checkmark next to contract name when it's seleced in menu bar	
	@parameter mn is the Contract menubar
	@parameter index corresponds to the index of the contract selected in 
	global list CONTRACT_OPTIONS
	'''
	def handle_selected_contract(self, mn, index):
		for i,v in enumerate(CONTRACT_OPTIONS):
			mn.entryconfigure(i, label=v)
		mn.entryconfigure(index, label=u'\u2713 '+CONTRACT_OPTIONS[index])

	'''
	@method handle_nilometer_proposal [Nilometer Context]
	Called when a new proposal is submitted 
	Returns the web3py transaction object
	'''
	def handle_nilometer_proposal(self):
		print("Submitting new Nilometer proposal...")
		minWaterLevel = water_level_entry.get()
		supportingAmount = supporting_amount_entry.get()

		self.nilometerinterface.unlock_account(self.ethereum_acc_pass)
		tx = self.nilometerinterface.new_proposal(minWaterLevel, supportingAmount)
		return tx

	'''
	@method handle_tally [NFO Coin Context]
	Called when the tally votes button is clicked
	'''
	def handle_tally(self):
		if not hasattr(self, 'last_selected_proposalID'):
			print("No proposal selected.")
			return

		self.manifestointerface.unlock_account(self.ethereum_acc_pass)
		self.manifestointerface.tally_votes(self.last_selected_proposalID)

	'''
	@method handle_buy_nfocoin [NFO Coin Context]
	Submits transaction to purchase NFO Coin against Ether
	'''
	def handle_buy_nfocoin(self):
		eth_amt_in_wei = buy_nfocoin_entry.get()
		if not eth_amt_in_wei:
			return
		print("Attempting to buy "+str(eth_amt_in_wei)+" wei worth of NFO Coin")

		self.nfointerface.unlock_account(self.ethereum_acc_pass)
		self.nfointerface.buy_tokens(eth_amt_in_wei)

	'''
	@method handle_sell_nfocoin [NFO Coin Context]
	Submits transaction to sell NFO Coin 
	'''
	def handle_sell_nfocoin(self):
		nfocoin_amt = sell_nfocoin_entry.get()
		if not nfocoin_amt:
			print("Please specify amount of NFO Coin to sell.")
			return 
		print("Attempting to sell "+str(nfocoin_amt)+" NFO Coin.")
		self.nfointerface.unlock_account(self.ethereum_acc_pass)
		self.nfointerface.sell_tokens(nfocoin_amt)

	'''
	@method handle_set_gas [NFO Coin Context and Manifesto Context]
	Changes the gas amount set with all transactions
	Called when "Change Gas Amount" button is clicked
	'''
	def handle_set_gas(self):
		new_gas = gas_entry.get()
		if new_gas:
			new_gas=int(new_gas)

			if self.context == "manifesto":
				self.manifestointerface.set_gas(new_gas)
			if self.context == "nfocoin":
				self.nfointerface.set_gas(new_gas)

	'''
	@method handle_vote [Manifesto Context]
	Called when a user votes yes/no on the selected proposal
	'''
	def handle_vote(self):
		proposalID = vote_proposalID_entry.get()
		if vote_choice.get() == "yes": vote = "yes"
		elif vote_choice.get() == "no": vote = "no"
		else: vote = None

		if vote:
			index = PROPOSALS.index(proposal_listbox.get(ACTIVE)) 
		
		proposalID = index
		print("proposalID: ",proposalID)
		print("vote: ",vote)
		self.manifestointerface.unlock_account(self.ethereum_acc_pass)

		if vote=='yes':
			self.manifestointerface.vote(int(proposalID),True)
		if vote=='no':
			self.manifestointerface.vote(int(proposalID),False)
		
	'''
	@method handle_new_proposal [Manifesto Context]
	Called when the "Submit Proposal" button is clicked to create new proposal
	'''
	def handle_new_proposal(self):
		description = new_proposal_text.get(1.0,END).strip()
		print("New Proposal: ",description)
		if "Enter a new proposal" in description:
			return

		self.manifestointerface.unlock_account(self.ethereum_acc_pass)
		self.manifestointerface.new_proposal(description)

	'''
	@class BCInterface @method handle_new_account
	Interfaces with tkinter "New Account" button
	'''
	def handle_new_account(self):
		password = None
		while not password:
			password = simpledialog.askstring("DDASH","Choose a password for your new account: ")
		print("Attempting to unlock account...")
		self.bci.web3.personal.newAccount(password)

	'''
	@class BCInterface @method handle_unlock_account
	Interfaces with tkinter "Unlock Account" button
	'''
	def handle_unlock_account(self):
		password = None
		while not password:
			password = simpledialog.askstring("DDASH","Enter your Ethereum account password: ")

		self.ethereum_acc_pass=password
		self.ethereum_acc_pass = password
		self.bci.unlock_account(password)
		self.manifestointerface.unlock_account(password)
	'''
	@method handle_show_accounts 
	Updates the Account menu bar with a current list of Ethereum accounts 
	Called periodically with each clock() cycle
	'''
	def handle_show_accounts(self):
		if self.bci:
			for a in self.bci.eth_accounts:
				if a not in ACCOUNT_OPTIONS:
					ACCOUNT_OPTIONS.append(a)
					accountmenu.add_command(label=a,command=self.dynamic_account_handler(a))

	'''
	@method dynamic_account_handler
	Dynamically creates functions that are used as handlers when an Ethereum
	account is selected from the Account menu bar
	@parameter addr is an Ethereum address contained in the global list 
	ACCOUNT_OPTIONS
	'''
	def dynamic_account_handler(self,addr):
		def _function():
			index = ACCOUNT_OPTIONS.index(addr) 
			i=2
			while i < 2+len(ACCOUNT_OPTIONS):
				accountmenu.entryconfigure(i, label=ACCOUNT_OPTIONS[i-2])
				i+=1
			# when an account is selected, clear the Ethereum password from memory
			self.ethereum_acc_pass = None
			# place checkmark next to selected Ethereum address from Account menu bar
			accountmenu.entryconfigure(index+2, label=u'\u2713 '+ACCOUNT_OPTIONS[index])
			self.bci.set_account(index)
			if hasattr(self, 'nfointerface'):
				self.nfointerface.set_account(index)
			if hasattr(self, 'manifestointerface'):
				self.manifestointerface.set_account(index)
			if hasattr(self, 'nilometerinterface'):
				self.nilometerinterface.set_account(index)

		return _function


	'''
	@method launch
	Loads the Ethereum network selected in the Home context
	Called when the "Launch" button is clicked
	@TODO (low priority) 
		currently mining occurs using the zero-indexed Ethereum account
		as the coinbase account; need to change this to allow easy changing of
		the default coinbase account
	'''
	def launch(self):
		self.ready = True
		choice = self.network_variable.get()

		if choice == NETWORK_OPTIONS[0]: #Black Swan network selected
				self.network="blackswan"
				print("Loading ",choice) 
				cmd = "./load_blackswan.sh" 
				process = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				process.stdin.write("\n".encode())
				process.stdin.write("\n".encode())
				process.stdin.close()
				print (process.stdout.read())
			
				self.bci = BCInterface(mainnet=False)
				self.fsi = FSInterface()
				self.nfointerface = NFOInterface(mainnet=False)
				self.contract_address=blackswan_contract_address
				self.nfointerface.load_contract(mainnet=False,contract_name='nfocoin',contract_address=blackswan_nfo_address) 


		if choice == NETWORK_OPTIONS[1]: #Main Ethereum network
				self.network="mainnet"
				print("Loading ",choice)
				cmd = "./load_mainnet.sh"
				process = subprocess.Popen(cmd,stdin=subprocess.PIPE,
					stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				process.stdin.write("\n".encode())
				process.stdin.write("\n".encode())
				process.stdin.close()
				print (process.stdout.read())
					
				self.bci = BCInterface(mainnet=True)
				self.fsi = FSInterface()
				self.nfointerface = NFOInterface(mainnet=True)
				self.contract_address=blackswan_contract_address
				self.nfointerface.load_contract(mainnet=True, contract_name="nfocoin", contract_address=mainnet_nfo_address)

		messagebox.showinfo("Success", "You are connected to "+self.network+". Select a contract from the top menu bar.")
		current_network_label.config(text="You are connected to "+self.network)
		network_label.grid_remove()
		network_option.grid_remove()
		launch_button.grid_remove()

	'''
	@method handle_proposal_click [Manifesto Context]
	Display description of the selected proposal
	Called when a proposal is selected
	'''
	def handle_proposal_click(self, event):
		widget = event.widget
		selection = widget.curselection()
		value = widget.get(selection[0])
		row = proposalID = selection[0]
		self.last_selected_proposalID = int(row)
		
		text = "Proposal voting period: 60 minutes.\nNumber of votes needed to pass: 10.\n\n"
		p = twinpeaks.manifestointerface.get_proposal_by_row(row)
		text+="Proposal ID: "+str(row)+"\n"
		text+="Proposal description: "+p[0].strip()+"\n"
		text+="Current time: "+str(time.time()).split('.')[0] +"\n"

		if time.time() > p[1]:
			text+="Status: Expired\n"
		else:
			text+="Status: Voting period open\n"

		text+="Voting deadline: "+str(p[1])+"\n"
		#text+="Executed: "+str(p[2])+"\n"
		text+="Passed: "+str(p[3])+"\n"
		text+="Number of votes: "+str(p[4])+"\n\n"
		
		new_proposal_label.configure(text=text)


	'''
	@method nilometer_context
	Configures the GUI for the Nilometer Context to allow user to 
	interface with the Nilometer.sol contract 
	'''
	def nilometer_context(self):
		if not self.ready:
			return
		self.context = "nilometer"

		if not self.ethereum_acc_pass:
			answer = simpledialog.askstring("DDASH","Enter your Ethereum account password: ")
			self.ethereum_acc_pass = answer

		if not hasattr(self, 'nilometerinterface'):
			self.nilometerinterface = NilometerInterface(mainnet=False)
			self.nilometerinterface.load_contract(mainnet=False)
	
		root.geometry('{}x{}'.format(950, 800))
		self.nilometerinterface.unlock_account(self.ethereum_acc_pass)

		lake_nasser_label.grid()
		current_network_label.grid()
		current_network_label.config(text="Your are connected to "+self.network)
		gas_label.grid()
		gas_entry.grid()
		set_gas_button.grid()

		top_frame.grid()
		nilometer_frame.grid()
		network_frame.grid()
	
	'''
	@method manifesto_context
	Configures the GUI for the Manifesto Context to allow user to 
	interface with the Manifesto.sol contract 
	'''
	def manifesto_context(self):
		if not self.ready:
			return
		self.context = "manifesto"

		if not self.ethereum_acc_pass:
			answer = simpledialog.askstring("DDASH","Enter your Ethereum account password: ")
			self.ethereum_acc_pass = answer

		if not hasattr(self, 'manifestointerface'):
			self.manifestointerface = ManifestoInterface(mainnet=False)
			self.manifestointerface.load_contract(mainnet=False)
		root.geometry('{}x{}'.format(950, 800))
		self.manifestointerface.unlock_account(self.ethereum_acc_pass)

		manifesto_address_label.grid()
		manifesto_address_entry.grid()
		proposal_listbox.grid()
		new_proposal_label.grid()
		new_proposal_text.grid() 
		new_proposal_button.grid()
		vote_button.grid()
		current_network_label.grid()
		current_network_label.config(text="Your are connected to "+self.network)
		gas_label.grid()
		gas_entry.grid()
		set_gas_button.grid()
		tally_button.grid() 

		vote_yes_radio.grid()
		vote_no_radio.grid()

		top_frame.grid()
		manifesto_frame.grid()
		network_frame.grid()
			
	'''
	@method nfocoin_context
	Configures the GUI for the NFO Coin Context to allow user to 
	interface with the nfocoin.sol contract 
	'''
	def nfocoin_context(self):
		if not self.ready:
			return
		self.context="nfocoin"
		root.geometry('{}x{}'.format(800, 750))
		address_label.grid()
		address_entry.grid()
		balance_label.grid()
		nfocoin_balance_label.grid()
		buy_nfocoin_label.grid()
		buy_nfocoin_entry.grid()
		sell_nfocoin_label.grid()
		sell_nfocoin_entry.grid()
		sell_nfocoin_button.grid()
		send_nfocoin_label.grid()
		send_nfocoin_amount_entry.grid()
		send_nfocoin_button.grid()
		intranet_nfocoin_radio.grid()
		internet_nfocoin_radio.grid()
		gas_label.grid()
		gas_entry.grid()
		account_label.grid()
		new_account_button.grid()
		unlock_account_button.grid()

		top_frame.grid()
		center_frame.grid()
		transaction_frame.grid()
		network_frame.grid() 
			
		current_network_label.grid()
		current_network_label.config(text="Your are connected to "+self.network)
		gas_label.grid()
		gas_entry.grid()
		set_gas_button.grid()
		buy_nfocoin_button.grid()

		if not self.ethereum_acc_pass:
			answer = simpledialog.askstring("DDASH","Enter your Ethereum account password: ")
			self.ethereum_acc_pass = answer

	'''
	@method clear_screen
	Clears all frames from the GUI. Called when changing contexts
	'''
	def clear_screen(self):
		if not self.ready:
			return

		gif_label.grid_remove()
		proposal_listbox.grid_remove()
		manifesto_address_label.grid_remove()
		manifesto_address_entry.grid_remove()
		new_proposal_text.grid_remove()
		new_proposal_label.grid_remove()
		new_proposal_button.grid_remove()
		vote_proposalID_label.grid_remove()
		vote_proposalID_entry.grid_remove()
		vote_label.grid_remove()
		vote_entry.grid_remove()
		vote_button.grid_remove()
		gas_label.grid_remove()
		gas_entry.grid_remove()
		set_gas_button.grid_remove()

		address_label.grid_remove()
		address_entry.grid_remove()
		balance_label.grid_remove()
		nfocoin_balance_label.grid_remove()
		buy_nfocoin_label.grid_remove()
		buy_nfocoin_entry.grid_remove()
		gas_label.grid_remove()
		gas_entry.grid_remove()
		account_label.grid_remove()
		new_account_button.grid_remove()
		unlock_account_button.grid_remove()
		network_label.grid_remove()
		network_option.grid_remove()
		launch_button.grid_remove()
		manifesto_frame.grid_remove()

		nilometer_address_label.grid_remove()
		nilometer_address_entry.grid_remove()
		lake_nasser_label.grid_remove()

		# clear frames
		top_frame.grid_remove()
		center_frame.grid_remove()
		transaction_frame.grid_remove()
		account_frame.grid_remove()
		network_frame.grid_remove()
		nilometer_frame.grid_remove()

	
	'''
	@method clock
	Updates the display. Called periodically every X seconds
	'''
	def clock(self):

		time = datetime.datetime.now().strftime("Time: %H:%M:%S")
		twinpeaks.handle_show_accounts()

		if hasattr(self,'manifestointerface'):
			if len(self.manifestointerface.eth_accounts)==0:
				address_entry.delete(0, END)
				address_entry.insert(0, "No Ethereum account found.")
				balance_label.configure(text="Balance: 0 Ether")

				answer = messagebox.askyesno("DDASH","I don't see any Ethereum accounts. Would you like to create one?")
				if answer:
					answer = simpledialog.askstring("DDASH","Choose a password: ")
					answer2 = simpledialog.askstring("DDASH","Enter your password again: ")
					if answer == answer2:
						# create new Ethereum account
						self.manifestointerface.web3.personal.newAccount(answer)
						self.ethereum_acc_pass=answer

			if not self.manifestointerface.is_valid_contract_address(manifesto_address_entry.get()):
				manifesto_address_entry.delete(0,END)
				manifesto_address_entry.insert(0, blackswan_manifesto_address)

			if self.manifestointerface.last_contract_address != manifesto_address_entry.get():
				proposal_listbox.delete(0, END)
				new_proposal_label.configure(text="")
				PROPOSALS.clear() 	
				self.manifestointerface.last_contract_address = self.manifestointerface.tx['to']
			num_proposals = self.manifestointerface.get_proposal_count()
			text = ""
			text+="Number of proposals: "+str(num_proposals)+"\n\n"
			i = 0
			while i < num_proposals:
				p = self.manifestointerface.get_proposal_by_row(i)
				text+="Proposal ID: "+str(i)+"\n"
				text+="Proposal description: "+p[0]+"\n"
				text+="Voting deadline: "+str(p[1])+"\n"
				text+="Executed: "+str(p[2])+"\n"
				text+="Passed: "+str(p[3])+"\n"
				text+="Number of votes: "+str(p[4])+"\n\n"

				if p[0] not in PROPOSALS:
					proposal_listbox.insert('end', p[0])
					PROPOSALS.append(p[0])

				i+=1

			if not gas_entry.get():
				gas_entry.delete(0,END)
				gas_entry.insert(0,"4000000")

			if gas_entry.get():
				self.manifestointerface.set_gas(int(gas_entry.get()))

			self.manifestointerface.load_contract(contract_name='manifesto', contract_address=self.manifestointerface.is_valid_contract_address(manifesto_address_entry.get().strip()) or blackswan_manifesto_address,mainnet=False)

		if hasattr(self,'nfointerface'):
			if self.bci:
				balance_label.configure(text="Ether Balance: "+str(self.bci.get_balance()))
				nfocoin_balance_label.configure(text="NFO Coin Balance: "+str(self.nfointerface.my_token_balance()))

			if self.nfointerface:
				if len(self.nfointerface.eth_accounts) >0:
					address_entry.delete(0,END)
					address_entry.insert(0,self.nfointerface.eth_accounts[self.nfointerface.account_index])

				if not gas_entry.get():
					if self.network == "blackswan":
						gas_entry.insert(0,"4000000")
					elif self.network == "mainnet":
						gas_entry.insert(0,"70000")

				if gas_entry.get():
					self.nfointerface.set_gas(int(gas_entry.get()))

		self.master.after(5000,self.clock)

def Nilometer():
	if twinpeaks.network != "blackswan":
		messagebox.showinfo("Error", "The Nilometer.sol contract is only available on the Black Swan network, not the Ethereum main net.")
		return

	twinpeaks.clear_screen()
	twinpeaks.nilometer_context()
	twinpeaks.handle_selected_contract(contractmenu, 2)

def Manifesto():
	if twinpeaks.network != "blackswan":
		messagebox.showinfo("Error", "The Manifesto.sol contract is only available on the Black Swan network, not the Ethereum main net.")
		return

	twinpeaks.clear_screen()
	twinpeaks.manifesto_context()
	twinpeaks.handle_selected_contract(contractmenu, 0)

def NFOCoin():
	twinpeaks.clear_screen()
	twinpeaks.nfocoin_context()
	twinpeaks.handle_selected_contract(contractmenu, 1)

def About():
	text = "DDASH\nInitial work: Omar Metwally\nomar.metwally@gmail.com\n\nhttps://github.com/osmode/ddash"
	messagebox.showinfo("About DDASH", text)
    
root = Tk()
root.geometry('{}x{}'.format(500, 600))

twinpeaks = TwinPeaks(root)
menubar = Menu(root)
# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

twinpeaks.clock()

# Create menu bars at the top of the screen
contractmenu = Menu(menubar)
contractmenu.add_command(label=CONTRACT_OPTIONS[0], command=Manifesto )
contractmenu.add_command(label=CONTRACT_OPTIONS[1], command=NFOCoin)
contractmenu.add_command(label=CONTRACT_OPTIONS[2], command=Nilometer)
contractmenu.add_separator()
menubar.add_cascade(label="Contract", menu=contractmenu)

accountmenu = Menu(menubar)
accountmenu.add_command(label="New Account", command=twinpeaks.handle_new_account)
accountmenu.add_separator()
menubar.add_cascade(label="Account", menu=accountmenu)

helpmenu = Menu(menubar)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

root.config(menu=menubar)

# shooting star gif
gif_path = os.getcwd()+'/images/ss.gif'
frames = [PhotoImage(file=gif_path,format="gif -index %i" %(i)) for i in range(36)]
gif_label = Label(root) #, image=frames[0])

def update(ind):

	frame = frames[ind%36]
	gif_label.configure(image=frame)
	if ind%36==0 and twinpeaks.context=="home":
		gif_label.grid(row=1,column=0, padx=20, sticky="w")
	elif twinpeaks.context != "home" and ind%36==0:
		gif_label.grid_remove()

	ind+=1

	root.after(100,update,ind)

def on_close():
	process=subprocess.Popen("tmux kill-session -t geth".split())
	print("Quitting DDASH and killing geth...")
	#process=subprocess.Popen("tmux kill-session -t ipfs".split())
	twinpeaks.master.quit()
	print("Done.")


manifesto_frame = Frame(root) 
manifesto_frame.grid(row=1,padx=(100,10), sticky=NW)
manifesto_frame.grid_remove()

nilometer_frame = Frame(root)
nilometer_frame.grid(row=1,padx=(100,10), sticky=NW)
nilometer_frame.grid_remove()

top_frame = Frame(root, bg='white', width=1000, height=150, relief="sunken")
top_frame.grid(row=0, sticky="sew", padx=(50,10), pady=(50,10))

center_frame = Frame(root, bg='white')
center_frame.grid(row=1,sticky="new", padx=(50,10) )
center_frame.grid_remove()
transaction_frame = Frame(root, bg='white', width=1000, height=100,padx=40, pady=20, relief="sunken", borderwidth=2)
transaction_frame.grid(row=2,sticky="new", padx=(50,50), pady=(50,50))
transaction_frame.grid_remove()
account_frame = Frame(root, bg='white', width=1000, height=100,padx=40, pady=20, relief="sunken")
account_frame.grid(row=3,sticky="ew")
account_frame.grid_remove()
network_frame = Frame(root, bg='white', width=1000, height=100,padx=40, pady=20, relief="sunken",borderwidth=2)
network_frame.grid(row=4,sticky="ew")

# arrange elements within frames

## TOP FRAME 
intro_label = Label(top_frame, text=intro,font="Courier 60")
intro_label.grid(row=0)
## CENTER FRAME 
address_label = Label(center_frame, text="Your Ethereum address: ")
address_label.grid(row=1, sticky="w")
address_label.grid_remove()
address_entry = Entry(center_frame)  
address_entry.grid(row=2)
address_entry.config(width=45)
address_entry.grid_remove()

balance_label = Label(center_frame,text="Ether Balance: " )
balance_label.grid(row=3, column=0, sticky="w", pady=10)
balance_label.grid_remove()
nfocoin_balance_label = Label(center_frame,text="NFO Coin Balance: ")
nfocoin_balance_label.grid(row=4, column=0, sticky="w",pady=10)
nfocoin_balance_label.grid_remove()

## transaction fraome
buy_nfocoin_label = Label(transaction_frame,text="Buy NFO Coin with this amount of Ether in wei (1 wei = 1e-18 Ether): ")
buy_nfocoin_label.grid(row=5,column=0, sticky=W)
buy_nfocoin_label.grid_remove()
buy_nfocoin_entry = Entry(transaction_frame) 
buy_nfocoin_entry.grid(row=6, column=0)
buy_nfocoin_entry.config(width=50)
buy_nfocoin_entry.grid_remove()
buy_nfocoin_button = Button(transaction_frame, text="Buy",command=twinpeaks.handle_buy_nfocoin) 
buy_nfocoin_button.grid(row=6,column=1,sticky="w")
buy_nfocoin_button.grid_remove()

sell_nfocoin_label = Label(transaction_frame,text="Sell this amount of NFO Coin (1000 NFO Coin = 1 Ether):")
sell_nfocoin_label.grid(row=7,column=0, pady=20, sticky=W)
sell_nfocoin_label.grid_remove()
sell_nfocoin_entry = Entry(transaction_frame) 
sell_nfocoin_entry.grid(row=8, column=0)
sell_nfocoin_entry.config(width=50)
sell_nfocoin_entry.grid_remove()
sell_nfocoin_button = Button(transaction_frame, text="Sell", command=twinpeaks.handle_sell_nfocoin) 
sell_nfocoin_button.grid(row=8,column=1,sticky="w")
sell_nfocoin_button.grid_remove()

send_nfocoin_label = Label(transaction_frame,text="Send NFO Coin", pady=20)
send_nfocoin_label.grid(row=9, column=0, sticky=W)
send_nfocoin_amount_entry = Entry(transaction_frame)
send_nfocoin_amount_entry.grid(row=10, column=0)
send_nfocoin_amount_entry.config(width=50)
send_nfocoin_address_entry = Entry(transaction_frame)
send_nfocoin_address_entry.grid(row=11,column=0)
send_nfocoin_address_entry.config(width=50)
send_nfocoin_button = Button(transaction_frame, text="Send", command=twinpeaks.handle_send_nfocoin)
send_nfocoin_button.grid(row=10, column=2, sticky="NS")
send_nfocoin_address_entry.delete(0, END)
send_nfocoin_address_entry.insert(0, "Recipient Ethereum address (e.g. 0x...)")
send_nfocoin_amount_entry.delete(0,END)
send_nfocoin_amount_entry.insert(0, "Number of NFO Coin to send (1000 NFO Coin = 1 Ether)")


send_nfocoin_choice = StringVar() 
intranet_nfocoin_radio = Radiobutton(transaction_frame, indicatoron=0, text="Intra-Network", variable=send_nfocoin_choice, value='intra')
internet_nfocoin_radio = Radiobutton(transaction_frame, indicatoron=1, text="Inter-Network", variable=send_nfocoin_choice, value='inter')
intranet_nfocoin_radio.grid(row=10, column=1,sticky=W)
internet_nfocoin_radio.grid(row=11,column=1,sticky=W)

account_label = Label(account_frame, text="Account: ",padx=20,pady=40)
account_label.grid(row=7,column=0)
account_label.grid_remove()

new_account_button = Button(account_frame, text="New Account", command=twinpeaks.handle_new_account)
new_account_button.grid(row=8,column=0)
new_account_button.grid_remove()
unlock_account_button = Button(account_frame, text="Unlock Account", command=twinpeaks.handle_unlock_account)
unlock_account_button.grid(row=8, column=1)
unlock_account_button.grid_remove()

network_label = Label(network_frame, text="Network: ", bg='white')
network_label.grid(row=9 )

network_option = OptionMenu(network_frame, twinpeaks.network_variable, *NETWORK_OPTIONS, command=None) 
network_option.grid(row=9,column=1,pady=20)

launch_button = Button(network_frame, text="Launch", command=twinpeaks.launch, bg='white')
launch_button.grid(row=10, column=1)

# NILOMETER layout
nilometer_address_label = Label(nilometer_frame,text="Nilometer.sol address:")
nilometer_address_label.grid(row=2,column=0,sticky=NW)
nilometer_address_label.grid_remove()
nilometer_address_entry = Entry(nilometer_frame)
nilometer_address_entry.grid(row=2,column=0,columnspan=3)
nilometer_address_entry.config(width=40)
nilometer_address_entry.grid_remove() 

# MANIFESTO layout
manifesto_address_label = Label(manifesto_frame,text="Manifesto.sol address:")
manifesto_address_label.grid(row=2,column=0,sticky=NW)
manifesto_address_label.grid_remove()
manifesto_address_entry = Entry(manifesto_frame)
manifesto_address_entry.grid(row=2,column=0,columnspan=3)
manifesto_address_entry.config(width=40)
manifesto_address_entry.grid_remove() 

proposals_scrollbar = Scrollbar(manifesto_frame) 
proposals_scrollbar.grid(row=3, column=0)
proposals_text = Text(manifesto_frame, wrap=WORD, yscrollcommand=proposals_scrollbar.set,height=6,borderwidth=1)

proposal_listbox = Listbox(manifesto_frame, width=5, height=10)
proposal_listbox.bind("<<ListboxSelect>>", twinpeaks.handle_proposal_click)
proposal_listbox.grid(column=0,row=3,sticky=(N,W,E,S))
proposal_scrollbar = Scrollbar(manifesto_frame, orient=VERTICAL)
proposal_scrollbar.config(command=proposal_listbox.yview)
proposal_scrollbar.grid(row=3, column=0, sticky=(N,E,S))
proposal_listbox['yscrollcommand'] = proposal_scrollbar.set

more_info_label = Label(manifesto_frame, text="ProposalID: \nVotes: ")
more_info_label.grid(row=4, column=0)
more_info_label.grid_remove()
vote_label = Label(manifesto_frame, text="Vote: ")
vote_label.grid(row=2,column=1)
vote_label.grid_remove()

vote_choice = StringVar() 
vote_yes_radio = Radiobutton(manifesto_frame, indicatoron=0, text="yes", variable=vote_choice, value='yes')
vote_yes_radio.grid(row=3,column=3,sticky=W)
vote_yes_radio.grid_remove()
vote_no_radio = Radiobutton(manifesto_frame, text="no", variable=vote_choice, value='no',indicatoron=0)
vote_no_radio.grid(row=3,column=2,sticky=E)
vote_no_radio.grid_remove()

vote_button = Button(manifesto_frame, text="Vote", command=twinpeaks.handle_vote)
vote_button.grid(row=3,column=1,sticky=E)
vote_button.grid_remove()
tally_button = Button(manifesto_frame, text="Tally Votes", command=twinpeaks.handle_tally)
tally_button.grid(row=4,column=1,sticky=W)
tally_button.grid_remove() 

new_proposal_label = Label(manifesto_frame,text="", justify=LEFT)
new_proposal_label.grid(row=4,column=0, sticky=W)
new_proposal_label.grid_remove()
new_proposal_text = Text(manifesto_frame, wrap=WORD, yscrollcommand=proposals_scrollbar.set,height=5,borderwidth=1)
myFont = Font(family="Arial", size=14)
new_proposal_text.configure(font=myFont)
new_proposal_text.insert(END,"Enter a new proposal here...")
new_proposal_text.grid(row=5,column=0)
new_proposal_text.grid_remove() 
new_proposal_button = Button(manifesto_frame, text="Submit Proposal", command=twinpeaks.handle_new_proposal)
new_proposal_button.grid(row=6,column=0,sticky=W )
new_proposal_button.grid_remove()

vote_proposalID_label = Label(manifesto_frame, text="ProposalID: ")
vote_proposalID_label.grid(row=5,column=0)
vote_proposalID_label.grid_remove()
vote_proposalID_entry = Entry(manifesto_frame)
vote_proposalID_entry.grid(row=5,column=1)
vote_proposalID_entry.grid_remove()
vote_label = Label(manifesto_frame, text="Vote (yes/no):")
vote_label.grid(row=5,column=2)
vote_label.grid_remove()
vote_entry = Entry(manifesto_frame)
vote_entry.grid(row=5,column=3)
vote_entry.grid_remove()

current_network_label = Label(network_frame, text="")
current_network_label.grid(row=8,column=1,sticky='sw')

gas_label = Label(network_frame, text="Gas: ")
gas_label.grid(row=9,column=0, sticky="se")
gas_label.grid_remove()
gas_entry = Entry(network_frame)
gas_entry.grid(row=9,column=1, sticky=W)
gas_entry.grid_remove()
set_gas_button = Button(network_frame, text="Change Gas Amount",command=twinpeaks.handle_set_gas)
set_gas_button.grid(row=9,column=2,sticky=E)
set_gas_button.grid_remove()

lake_nasser_plot_path = os.getcwd()+'/images/lake_nasser_plot.gif'
lake_nasser_image = PhotoImage(file=lake_nasser_plot_path)
lake_nasser_label = Label(nilometer_frame,image=lake_nasser_image)
lake_nasser_label.grid(row=1,column=0, padx=20, sticky="w")

nilometer_proposal_label = Label(nilometer_frame, text="New Proposal", font="Arial 20")
nilometer_proposal_label.grid(row=2,column=0,  sticky="w")
water_level_label = Label(nilometer_frame, text="Minimum Nile water level in centimeters: ")
water_level_label.grid(row=3,column=0, sticky="w")
water_level_entry = Entry(nilometer_frame)
water_level_entry.grid(row=4, column=0, sticky="w")
water_level_entry.config(width=20)
supporting_amount_label = Label(nilometer_frame, text="Supporting amount in wei (= 10^-18 Ether): ")
supporting_amount_label.grid(row=5, column=0, sticky="w")
supporting_amount_entry = Entry(nilometer_frame)
supporting_amount_entry.config(width=50)
supporting_amount_entry.grid(row=6, column=0, sticky="w")
nilometer_proposal_button = Button(nilometer_frame, text="Submit New Proposal", command=twinpeaks.handle_nilometer_proposal)
nilometer_proposal_button.grid(row=7,column=0, sticky="w")

# handle X-ing window
root.protocol("WM_DELETE_WINDOW", on_close)
# handle quit
atexit.register(on_close)

root.after(0,update,0)
root.mainloop()


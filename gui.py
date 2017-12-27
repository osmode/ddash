from tkinter import simpledialog, messagebox
from tkinter import *
import subprocess, os
from subprocess import call
import sys, datetime

sys.path.insert(0, os.path.join(os.getcwd(),'ddash'))
from bcinterface import *
from fsinterface import *
from nfointerface import *
from manifestointerface import *
from getpass import getpass


# Flags to instruct DDASH to broadcast enode address to blockchain
# and query blockchain for peer enodes
BROADCAST=False
LISTEN=False
blackswan_contract_address="0x5ff2ce40e82e52d370fa9a0ddf49aeee32184756"
recordmanager_contract_address="0xcc109bf72338909ead31a5bf46d8d8fa455ff09b"
mainnet_nfo = "0x3100047369b54c34042b9dc138c02a0567d90a7a"
blackswan_nfo_address = "0x38a779dd481b5f812b76b039cb2077fb124677a7"

NETWORK_OPTIONS = [
	"Black Swan network",
	"Main Ethereum network"
]

NFO_TX_OPTIONS = [
	"Buy NFO Coin",
	"Sell NFO Coin"
]

ACCOUNT_OPTIONS = {}
account_option = None

'''
intro = r"""

    _____  _____       	   _____ _    _ 
   |  __ \|  __ \   /\    / ____| |  | |
   | |  | | |  | | /  \  | (___ | |__| |
   | |  | | |  | |/ /\ \  \___ \|  __  |
   | |__| | |__| / ____ \ ____) | |  | |
   |_____/|_____/_/    \_\_____/|_|  |_|
                                             
   ::: Distributed Data Sharing Hyperledger :::
"""
'''
intro = r"""
   ddash   
"""

def get_value_from_index(input_phrase,index,convert_to='integer'):
    input_phrase = input_phrase.split()
    value =None

    try:
        if convert_to is 'string': value = str(input_phrase[index])
        elif convert_to is 'integer': value = int(input_phrase[index])
        else: value = int(input_phrase[index])

    except:
        print("ValueFromIndex Error.")

    return value

class TwinPeaks:
	def __init__(self, master):
		self.master = master
		master.title("DDASH")
		self.network=None
		self.last_account_index = 0 
		self.last_nfo_tx_amount = 0
		self.network_variable = StringVar()
		self.network_variable.set(NETWORK_OPTIONS[1])
		self.account_variable = StringVar(self.master)
		self.bci = None
		self.fsi = None
		self.nfointerface = None

		# self.ready changes to True when Launch button is clicked
		self.ready = False

		'''
		cmd = "./gui.sh"
		process = subprocess.Popen('./gui.sh',stdin=subprocess.PIPE,
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		process.stdin.write("\n".encode())
		process.stdin.write("\n".encode())
		#process.stdin.write("peer count".encode())

		process.stdin.close()
		print (process.stdout.read())
	
		self.bci = BCInterface()
		self.fsi = FSInterface()
		self.contract_name='blackswan'
		self.contract_address=blackswan_contract_address
		self.bci.load_contract(contract_name=self.contract_name, contract_address=self.contract_address)
		'''

	def dropdown(self, value):
		pass

	def nfotxdropdown(self, choice):
		amount = self.nfo_tx_entry.get()
		print("nfotxdropdown value: ",amount)
		if choice == NFO_TX_OPTIONS[0]: # Buy NFO Coin
			print("Trying to purchase tokens using ",amount," Ether.")
			self.last_nfo_tx_amount = amount
			tx = self.nfointerface.buy_tokens(self.gas_entry.get())
			return tx

			try:
				self.nfointerface.tx['gas'] = 100000
				self.nfointerface.set_gas(self.gas_entry.get())
				tx = self.nfointerface.buy_tokens(amount)
			except:
				tx = None
				print("Failed to buy tokens")
				pass

			return tx
		if choice == NFO_TX_OPTIONS[1]: # Sell NFO Coin
			self.nfointerface.tx['gas'] = 10000
			print("Trying to sell ", amount, " tokens.")
			self.last_nfo_tx_amount = amount
			#self.nfointerface.decrease_gas(3)
			tx = self.nfointerface.sell_tokens(self.gas_entry.get())
			return tx

			try:
				self.nfointerface.set_gas(self.gas_entry.get())
				tx = self.nfointerface.sell_tokens(self.gas_entry.get())
			except:
				tx = None
				print("Failed to sell tokens")
				pass

	def handle_set_gas(self):
		new_gas = manifesto_gas_entry.get()
		if new_gas:
			print("Setting gas to: ",new_gas)
			new_gas=int(new_gas)
			self.manifestointerface.set_gas(new_gas)

	def handle_execute_proposal(self):
		self.manifestointerface.unlock_account(self.manifestointerface.ethereum_acc_pass)
		proposalID = self.execute_proposal_entry.get()
		print("Attemtping to execute proposalID ",proposalID)
		if proposalID:
			self.manifestointerface.executeProposal(int(proposalID))

	def handle_vote(self):
		proposalID = self.vote_proposalID_entry.get()
		vote = self.vote_entry.get()
		vote = vote.lower()
		print("proposalID: ",proposalID)
		print("vote: ",vote)
		self.manifestointerface.unlock_account(self.manifestointerface.ethereum_acc_pass)

		if vote[0]=='y':
			self.manifestointerface.vote(int(proposalID),True)
		if vote[0]=='n':
			self.manifestointerface.vote(int(proposalID),False)
		

	'''
	@class TwinPeaks @method handle_new_proposal
	Responds to button when clicked to submit new proposal
	'''
	def handle_new_proposal(self):
		description = self.new_proposal_text.get(1.0,END)
		print("New Proposal: ",description)
		self.manifestointerface.unlock_account(self.manifestointerface.ethereum_acc_pass)
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

		self.bci.ethereum_acc_pass=password
		self.bci.unlock_account(password)

	'''
	@class BCInterface @method handle_account_dropdown
	Handles changes to the dropdown menu with a list of Ethereum accounts.
	Utilizes the ACCOUNT_OPTIONS dictionary to map accounts with account indices
	'''
	def handle_account_dropdown(self, value):
		if len(self.bci.eth_accounts) > 0:
			accounts = self.bci.get_eth_accounts()
			for index, acc in enumerate(accounts):
				ACCOUNT_OPTIONS[acc] = index

		if value not in ACCOUNT_OPTIONS.keys():
			print(value+" was not recognized as a valid Ethereum account.")
			return 1
		index = ACCOUNT_OPTIONS[value]
		print("Last account index: ",index)
		self.last_account_index = index
		self.bci.set_account(index)

	def launch(self):

		self.ready = True
		self.nfocoin_context()

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
				print("NFO Interface created")
				self.contract_name='blackswan'
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
				self.contract_name='blackswan'
				self.contract_address=blackswan_contract_address
				self.nfointerface.load_contract(mainnet=True, contract_name="nfocoin", contract_address=mainnet_nfo_address)

		ACCOUNT_OPTIONS = self.bci.eth_accounts
		self.account_variable.set(ACCOUNT_OPTIONS[0])

		# ugly hack
		global account_option
		account_option = OptionMenu(account_frame, self.account_variable, *ACCOUNT_OPTIONS, command=self.handle_account_dropdown)
		account_option.grid(row=7,column=1,pady=20)


	def close(self):
		process=subprocess.Popen("tmux kill-session -t geth".split())
		#process=subprocess.Popen("tmux kill-session -t ipfs".split())
		self.master.quit()

	def manifesto_context(self):
		if not self.ready:
			return

		self.manifestointerface = ManifestoInterface(mainnet=False)
		self.manifestointerface.load_contract(mainnet=False)

		if not self.manifestointerface.ethereum_acc_pass:
			answer = simpledialog.askstring("DDASH","Enter your Ethereum account password: ")
			self.manifestointerface.ethereum_acc_pass=answer

		self.manifestointerface.unlock_account(self.manifestointerface.ethereum_acc_pass)


		manifesto_address_label.grid()
		manifesto_address_entry.grid()
		proposals_scrollbar.grid()
		proposals_text.grid()
		new_proposal_label.grid()
		new_proposal_scrollbar.grid()
		new_proposal_text.grid() 
		new_proposal_button.grid()
		vote_proposalID_label.grid()
		vote_proposalID_entry.grid()
		vote_label.grid()
		vote_entry.grid()
		vote_button.grid()
		execute_proposal_label.grid()
		execute_proposal_entry.grid()
		execute_proposal_button.grid() 
		manifesto_gas_label.grid()
		manifesto_gas_entry.grid()
		manifesto_set_gas_button.grid()

		top_frame.grid()
		manifesto_frame.grid()
		network_frame.grid()

	def nfocoin_context(self):
		if not self.ready:
			return

		address_label.grid()
		address_entry.grid()
		balance_label.grid()
		nfocoin_balance_label.grid()
		buy_nfocoin_label.grid()
		nfo_tx_entry.grid()
		gas_label.grid()
		gas_entry.grid()
		account_label.grid()
		new_account_button.grid()
		unlock_account_button.grid()
		network_label.grid()
		close_button.grid()
		launch_button.grid()

		top_frame.grid()
		center_frame.grid()
		transaction_frame.grid()
		account_frame.grid()
		account_frame.grid()
		network_frame.grid()
	
	def clear_screen(self):
		if not self.ready:
			return

		proposals_scrollbar.grid_remove() 
		proposals_text.grid_remove()
		manifesto_address_label.grid_remove()
		manifesto_address_entry.grid_remove()
		new_proposal_scrollbar.grid_remove()
		new_proposal_text.grid_remove()
		new_proposal_label.grid_remove()
		new_proposal_button.grid_remove()
		vote_proposalID_label.grid_remove()
		vote_proposalID_entry.grid_remove()
		vote_label.grid_remove()
		vote_entry.grid_remove()
		vote_button.grid_remove()
		execute_proposal_label.grid_remove()
		execute_proposal_entry.grid_remove()
		execute_proposal_button.grid_remove() 
		manifesto_gas_label.grid_remove()
		manifesto_gas_entry.grid_remove()
		manifesto_set_gas_button.grid_remove()

		address_label.grid_remove()
		address_entry.grid_remove()
		balance_label.grid_remove()
		nfocoin_balance_label.grid_remove()
		buy_nfocoin_label.grid_remove()
		nfo_tx_entry.grid_remove()
		gas_label.grid_remove()
		gas_entry.grid_remove()
		account_label.grid_remove()
		new_account_button.grid_remove()
		unlock_account_button.grid_remove()
		network_label.grid_remove()
		account_option.grid_remove()
		network_option.grid_remove()
		launch_button.grid_remove()
		manifesto_frame.grid_remove()

		# clear frames
		top_frame.grid_remove()
		center_frame.grid_remove()
		transaction_frame.grid_remove()
		account_frame.grid_remove()
		network_frame.grid_remove()

		gif_label.grid_remove()
	
	def clock(self):

		#self.nfocoin_balance_label.grid_remove() 
		#self.nfocoin_balance_label.grid()

		time = datetime.datetime.now().strftime("Time: %H:%M:%S")
		'''
		if self.nfo_tx_entry:
			self.nfo_tx_entry.delete(0,END)
			self.nfo_tx_entry.insert(0,self.last_nfo_tx_amount)
		'''

		if hasattr(self,'manifestointerface'):
			if len(self.manifestointerface.eth_accounts)==0:
				address_entry.delete(0, END)
				address_entry.insert(0, "No Ethereum account found.")
				#self.address_label.configure(text="No Ethereum account found.")
				balance_label.configure(text="Balance: 0 Ether")

				answer = messagebox.askyesno("DDASH","I don't see any Ethereum accounts. Would you like to create one?")
				if answer:
					answer = simpledialog.askstring("DDASH","Choose a password: ")
					answer2 = simpledialog.askstring("DDASH","Enter your password again: ")
					if answer == answer2:
						# create new Ethereum account
						self.manifestointerface.web3.personal.newAccount(answer)
						self.manifestointerface.ethereum_acc_pass=answer
			else: # account(s) found
				if self.bci.ethereum_acc_pass:
					self.manifestointerface.ethereum_acc_pass = self.bci_ethereum_acc_pass
				else:
					if not self.manifestointerface.ethereum_acc_pass:
						answer = simpledialog.askstring("DDASH","Enter your Ethereum account password: ")

						self.manifestointerface.ethereum_acc_pass=answer
	

			self.manifestointerface.load_contract(contract_name='manifesto', contract_address=blackswan_manifesto_address,mainnet=False)
			manifesto_address_entry.delete(0,END)
			manifesto_address_entry.insert(0, self.manifestointerface.tx['to'])

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
				i+=1

			proposals_text.delete(1.0,END)
			proposals_text.insert(1.0, text)
			
			# populate default gas price
			# note this is  manually set - need a way to automatically calculate
			if not manifesto_gas_entry.get():
				manifesto_gas_entry.delete(0,END)
				manifesto_gas_entry.insert(0,"62136")

		if hasattr(self,'nfointerface'):
			if self.bci:
				balance_label.configure(text="Ether Balance:\n "+str(self.bci.get_balance()))
				nfocoin_balance_label.configure(text="NFO Coin Balance:\n "+str(self.nfointerface.my_token_balance()))

			if self.nfointerface:
				if len(self.nfointerface.eth_accounts) >0:
					address_entry.delete(0,END)
					address_entry.insert(0,self.nfointerface.eth_accounts[self.nfointerface.account_index])



		self.master.after(30000,self.clock)

def Manifesto():
	if twinpeaks.network != "blackswan":
		messagebox.showinfo("Error", "The Manifesto.sol contract is only available on the Black Swan network, not the Ethereum main net.")
		return

	twinpeaks.clear_screen()
	twinpeaks.manifesto_context()

def NFOCoin():
	twinpeaks.clear_screen()
	twinpeaks.nfocoin_context()

def About():
	print("This is a simple example of a menu")
    
root = Tk()
root.geometry('{}x{}'.format(1000, 800))

twinpeaks = TwinPeaks(root)
menubar = Menu(root)
root.config(menu=menubar)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

menubar.add_command(label="Hello!",command=root.quit)
menubar.add_command(label="Quit!", command=root.quit)
twinpeaks.clock()

filemenu = Menu(menubar)
menubar.add_cascade(label="Contract", menu=filemenu)
filemenu.add_command(label="Manifesto", command=Manifesto)
filemenu.add_command(label="NFO Coin", command=NFOCoin)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=twinpeaks.close())
helpmenu = Menu(menubar)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

# the artwork

# frames
gif_path = os.getcwd()+'/images/ss.gif'
frames = [PhotoImage(file=gif_path,format="gif -index %i" %(i)) for i in range(36)]
gif_label = Label(root) #, image=frames[0])

def update(ind):

	frame = frames[ind%36]
	gif_label.configure(image=frame)
	if ind==0:
		gif_label.grid(row=1,column=0)

	ind+=1

	root.after(100,update,ind)


manifesto_frame = Frame(root) 
manifesto_frame.grid(row=1,stick="ew")
manifesto_frame.grid_remove()

top_frame = Frame(root, bg='white', width=1000, height=200, relief="sunken")
top_frame.grid(row=0, sticky="ew")


#top_frame.grid_remove()
center_frame = Frame(root, bg='white', width=1000, height=200,padx=40, pady=40, relief="sunken")
center_frame.grid(row=1,sticky="ew")
center_frame.grid_remove()
transaction_frame = Frame(root, bg='white', width=1000, height=100,padx=40, pady=20, relief="sunken", borderwidth=2)
transaction_frame.grid(row=2,sticky="ew")
transaction_frame.grid_remove()
account_frame = Frame(root, bg='white', width=1000, height=100,padx=40, pady=20, relief="sunken")
account_frame.grid(row=3,sticky="ew")
account_frame.grid_remove()
network_frame = Frame(root, bg='white', width=1000, height=100,padx=200, pady=20, relief="sunken",borderwidth=2)
network_frame.grid(row=4,sticky="ew")
#network_frame.grid_remove()

# arrange elements within frames

## top frame
intro_label = Label(top_frame, text=intro,font="Courier 60")
intro_label.grid(row=0,columnspan=2,column=0)

## center frame
address_label = Label(center_frame, text="Your Ethereum address: ")
address_label.grid(row=1, columnspan=2)
address_label.grid_remove()
address_entry = Entry(center_frame)  
address_entry.grid(row=2, columnspan=3)
address_entry.grid_remove()

balance_label = Label(center_frame,text="Ether Balance: ")
balance_label.grid(row=3, column=1)
balance_label.grid_remove()
nfocoin_balance_label = Label(center_frame,text="NFO Coin Balance: ")
nfocoin_balance_label.grid(row=3, column=0,padx=10,pady=10)
nfocoin_balance_label.grid_remove()

## transaction fraome
nfo_tx_entry = Entry(transaction_frame) 
nfo_tx_entry.grid(row=6, column=0)
nfo_tx_entry.grid_remove()
gas_label = Label(transaction_frame,text="Gas:")
gas_label.grid(row=5,column=1)
gas_label.grid_remove()
gas_entry = Entry(transaction_frame)
gas_entry.grid(row=6,column=1)
gas_entry.insert(0, "62136")
gas_entry.grid_remove()

nfo_tx_variable = StringVar()
nfo_tx_variable.set(NFO_TX_OPTIONS[0])
nfo_tx_option = OptionMenu(transaction_frame, nfo_tx_variable, *NFO_TX_OPTIONS, command=twinpeaks.nfotxdropdown) 

#self.nfo_tx_option.grid(row=5, column=0)
buy_nfocoin_label = Label(transaction_frame,text="Buy NFO Coin with this amount of Ether (in wei = 1e18 Ether): ")
buy_nfocoin_label.grid(row=5,column=0, ipadx=10, ipady=10)
buy_nfocoin_label.grid_remove()

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

network_option = OptionMenu(network_frame, twinpeaks.network_variable, *NETWORK_OPTIONS, command=twinpeaks.dropdown)
network_option.grid(row=9,column=1,pady=20)

launch_button = Button(network_frame, text="Launch", command=twinpeaks.launch, bg='white')
launch_button.grid(row=14, column=1)

close_button = Button(network_frame, text="Close", command=twinpeaks.close, bg='white' )
close_button.grid(row=14, column=0)

# MANIFESTO layout
manifesto_address_label = Label(manifesto_frame,text="Manifesto.sol address:")
manifesto_address_label.grid(row=2,column=0)
manifesto_address_label.grid_remove()
manifesto_address_entry = Entry(manifesto_frame)
manifesto_address_entry.grid(row=2,column=1,columnspan=3)
manifesto_address_entry.grid_remove() 

proposals_scrollbar = Scrollbar(manifesto_frame) 
proposals_scrollbar.grid(row=3, column=0)
proposals_text = Text(manifesto_frame, wrap=WORD, yscrollcommand=proposals_scrollbar.set,height=6,borderwidth=1)
proposals_text.insert(END,"Loading proposals...")

proposals_text.grid(row=3, column=0)
proposals_scrollbar.configure(command=proposals_text.yview)
proposals_text.grid_remove()
proposals_scrollbar.grid_remove() 

new_proposal_label = Label(manifesto_frame,text="New Proposal:")
new_proposal_label.grid(row=4,column=0)
new_proposal_label.grid_remove()
new_proposal_scrollbar = Scrollbar(manifesto_frame)
new_proposal_scrollbar.grid(row=4,column=0)
new_proposal_text = Text(manifesto_frame, wrap=WORD, yscrollcommand=proposals_scrollbar.set,height=5)
new_proposal_text.insert(END,"Enter a new proposal here...")
new_proposal_text.grid(row=4,column=0)
new_proposal_scrollbar.grid_remove()
new_proposal_text.grid_remove() 
new_proposal_button = Button(manifesto_frame, text="Submit Proposal", command=twinpeaks.handle_new_proposal)
new_proposal_button.grid(row=4,column=1)
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

vote_button = Button(manifesto_frame, text="Submit Vote",command=twinpeaks.handle_vote)
vote_button.grid(row=5,column=4)
vote_button.grid_remove()

execute_proposal_label = Label(manifesto_frame, text="Execute proposalD:")
execute_proposal_label.grid(row=6,column=0)
execute_proposal_label.grid_remove()
execute_proposal_entry = Entry(manifesto_frame)
execute_proposal_entry.grid(row=6,column=1)
execute_proposal_entry.grid_remove()
execute_proposal_button = Button(manifesto_frame, text="Execute Proposal",command=twinpeaks.handle_execute_proposal)
execute_proposal_button.grid(row=6,column=2)
execute_proposal_button.grid_remove()

manifesto_gas_label = Label(manifesto_frame, text="Gas: ")
manifesto_gas_label.grid(row=7,column=0)
manifesto_gas_label.grid_remove()
manifesto_gas_entry = Entry(manifesto_frame)
manifesto_gas_entry.grid(row=7,column=1)
manifesto_gas_entry.grid_remove()
manifesto_set_gas_button = Button(manifesto_frame, text="Set Gas Amount",command=twinpeaks.handle_set_gas)
manifesto_set_gas_button.grid(row=7,column=2)
manifesto_set_gas_button.grid_remove()

root.after(0,update,0)
root.mainloop()


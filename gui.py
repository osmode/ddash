from tkinter import *
from tkinter import simpledialog
import subprocess, os
from subprocess import call
import sys, datetime

sys.path.insert(0, os.path.join(os.getcwd(),'ddash'))
from bcinterface import *
from fsinterface import *
from swapinterface import *
from getpass import getpass


# Flags to instruct DDASH to broadcast enode address to blockchain
# and query blockchain for peer enodes
BROADCAST=False
LISTEN=False
blackswan_contract_address="0x5ff2ce40e82e52d370fa9a0ddf49aeee32184756"
recordmanager_contract_address="0xcc109bf72338909ead31a5bf46d8d8fa455ff09b"

mainnet_swap_address = "0xed8c634ac8c2fa3694c32cb01b96a6912f8a7738"
blackswan_swap_address = "0x5fced4408a9ff19091a97a616e8432d00b808098"

NETWORK_OPTIONS = [
	"Black Swan network",
	"Main Ethereum network"
]

SWAP_TX_OPTIONS = [
	"Buy SwapCoin",
	"Sell SwapCoin"
]

ACCOUNT_OPTIONS = {}


intro = r"""

    _____  _____       	   _____ _    _ 
   |  __ \|  __ \   /\    / ____| |  | |
   | |  | | |  | | /  \  | (___ | |__| |
   | |  | | |  | |/ /\ \  \___ \|  __  |
   | |__| | |__| / ____ \ ____) | |  | |
   |_____/|_____/_/    \_\_____/|_|  |_|
                                             
   ::: Distributed Data Sharing Hyperledger :::
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
		self.last_account_index = 0 
		self.last_swap_tx_amount = 0

		self.intro_label = Label(text=intro,relief=RIDGE,font="Courier 14")
		self.intro_label.grid(row=0,columnspan=2,column=0)

		self.address_label = Label(text="Your Ethereum address: ")
		self.address_label.grid(row=1, columnspan=2)
		self.address_label.grid_remove()
		self.address_entry = Entry(self.master)  

		self.address_entry.grid(row=2, columnspan=2)
		self.address_entry.grid_remove()

		self.balance_label = Label(text="Ether Balance: ")
		self.balance_label.grid(row=3, column=1)
		self.balance_label.grid_remove()

		self.swapcoin_balance_label = Label(text="SwapCoin Balance: ")
		self.swapcoin_balance_label.grid(row=3, column=0,padx=100,pady=100)
		self.swapcoin_balance_label.grid_remove()

		self.swap_tx_variable = StringVar(self.master)
		self.swap_tx_variable.set(SWAP_TX_OPTIONS[0])
				
		self.swap_tx_option = OptionMenu(self.master, self.swap_tx_variable, *SWAP_TX_OPTIONS, command=self.swaptxdropdown) 

		#self.swap_tx_option.grid(row=5, column=0)
		self.buy_swapcoin_label = Label(text="Buy SwapCoin with this amount of Ether (in wei = 1e18 Ether): ")
		self.buy_swapcoin_label.grid(row=5,column=0, ipadx=10, ipady=10)
		self.buy_swapcoin_label.grid_remove()

		self.swap_tx_entry = Entry(self.master)
		self.swap_tx_entry.grid(row=6, column=0)
		self.swap_tx_entry.grid_remove()
		self.gas_label = Label(text="Gas:")
		self.gas_label.grid(row=5,column=1)
		self.gas_label.grid_remove()
	
		self.gas_entry = Entry(self.master)
		self.gas_entry.grid(row=6,column=1)
		self.gas_entry.insert(0, "62136")
		self.gas_entry.grid_remove()

		self.account_label = Label(text="Account: ",padx=20,pady=40)
		self.account_label.grid(row=7)
		self.account_label.grid_remove()
		self.new_account_button = Button(self.master, text="New Account", command=self.handle_new_account)
		self.new_account_button.grid(row=8,column=0)
		self.new_account_button.grid_remove()
		self.unlock_account_button = Button(self.master, text="Unlock Account", command=self.handle_unlock_account)
		self.unlock_account_button.grid(row=8, column=1)
		self.unlock_account_button.grid_remove()

		self.network_label = Label(text="Network: ")
		self.network_label.grid(row=9, pady=20 )

		self.network_variable = StringVar(self.master)
		self.network_variable.set(NETWORK_OPTIONS[1])
		self.network_option = OptionMenu(self.master, self.network_variable, *NETWORK_OPTIONS, command=self.dropdown)
		self.network_option.grid(row=9,column=1,pady=20)

		self.greet_button = Button(master, text="Launch", command=self.launch)
		self.greet_button.grid(row=14, column=1)

		self.close_button = Button(master, text="Close", command=self.close,
			pady=20)
		self.close_button.grid(row=14, column=0,pady=20)

		self.bci = None
		self.fsi = None
		self.swapinterface = None

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

	def swaptxdropdown(self, choice):
		amount = self.swap_tx_entry.get()
		print("swaptxdropdown value: ",amount)
		if choice == SWAP_TX_OPTIONS[0]: # Buy SwapCoin
			print("Trying to purchase tokens using ",amount," Ether.")
			#self.swapinterface.increase_gas(2)
			self.last_swap_tx_amount = amount
			tx = self.swapinterface.buy_tokens(self.gas_entry.get())
			return tx

			try:
				self.swapinterface.tx['gas'] = 100000
				self.swapinterface.set_gas(self.gas_entry.get())
				tx = self.swapinterface.buy_tokens(amount)
			except:
				tx = None
				print("Failed to buy tokens")
				pass

			return tx
		if choice == SWAP_TX_OPTIONS[1]: # Sell SwapCoin
			self.swapinterface.tx['gas'] = 10000
			print("Trying to sell ", amount, " tokens.")
			self.last_swap_tx_amount = amount
			#self.swapinterface.decrease_gas(3)
			tx = self.swapinterface.sell_tokens(self.gas_entry.get())
			return tx

			try:
				self.swapinterface.set_gas(self.gas_entry.get())
				tx = self.swapinterface.sell_tokens(self.gas_entry.get())
			except:
				tx = None
				print("Failed to sell tokens")
				pass
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
		if value not in ACCOUNT_OPTIONS.keys():
			print(value+" was not recognized as a valid Ethereum account.")
			return 1
		index = ACCOUNT_OPTIONS[value]
		print("Last account index: ",index)
		self.last_account_index = index
		self.bci.set_account(index)

	def launch(self):

		self.ready = True
		self.reveal()

		choice = self.network_variable.get()

		if choice == NETWORK_OPTIONS[0]: #Black Swan network selected
				print("Loading ",choice) 
				cmd = "./load_blackswan.sh" 
				process = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				process.stdin.write("\n".encode())
				process.stdin.write("\n".encode())
				process.stdin.close()
				print (process.stdout.read())
			
				self.bci = BCInterface()
				self.fsi = FSInterface()
				self.swapinterface = SwapInterface(mainnet=False)
				print("SWAPINTERFACE created")
				self.contract_name='blackswan'
				self.contract_address=blackswan_contract_address
				#self.bci.load_contract(contract_name=self.contract_name, contract_address=self.contract_address)
				#self.swapinterface.load_contract(contract_name="swap2", contract_address=swap_contract_address)
				self.swapinterface.load_contract(mainnet=False,contract_name='swap2',contract_address=blackswan_swap_address) 


		if choice == NETWORK_OPTIONS[1]: #Main Ethereum network
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
				self.swapinterface = SwapInterface(mainnet=True)
				self.contract_name='blackswan'
				self.contract_address=blackswan_contract_address
				#self.bci.load_contract(contract_name=self.contract_name, contract_address=self.contract_address)
				self.swapinterface.load_contract(mainnet=True, contract_name="swap2", contract_address=mainnet_swap_address)


	def close(self):
		process=subprocess.Popen("tmux kill-session -t geth".split())
		#process=subprocess.Popen("tmux kill-session -t ipfs".split())
		self.master.quit()

	def reveal(self):
		if not self.ready:
			return

		self.address_label.grid()
		self.address_entry.grid()
		self.balance_label.grid()
		self.swapcoin_balance_label.grid()
		self.buy_swapcoin_label.grid()
		self.swap_tx_entry.grid()
		self.gas_label.grid()
		self.gas_entry.grid()
		self.account_label.grid()
		self.new_account_button.grid()
		self.unlock_account_button.grid()
		self.network_label.grid()
		

	def clock(self):

		#self.swapcoin_balance_label.grid_remove() 
		#self.swapcoin_balance_label.grid()

		time = datetime.datetime.now().strftime("Time: %H:%M:%S")
		'''
		if self.swap_tx_entry:
			self.swap_tx_entry.delete(0,END)
			self.swap_tx_entry.insert(0,self.last_swap_tx_amount)
		'''

		if self.bci:
			if len(self.bci.eth_accounts) > 0:
				accounts = self.bci.get_eth_accounts()
				for index, acc in enumerate(accounts):
					ACCOUNT_OPTIONS[acc] = index
					
				self.account_variable = StringVar(self.master)
				if self.last_account_index < len(accounts):
					self.account_variable.set(accounts[self.last_account_index])
				else:
					self.account_variable.set(accounts[0])
				self.account_option = OptionMenu(self.master, self.account_variable, *accounts, command=self.handle_account_dropdown)
				self.account_option.grid(row=7,column=1)

			if len(self.bci.eth_accounts)==0:
				self.address_entry.delete(0, END)
				self.address_entry.insert(0, "No Ethereum account found.")
				#self.address_label.configure(text="No Ethereum account found.")
				self.balance_label.configure(text="Balance: 0 Ether")

				answer = messagebox.askyesno("DDASH","I don't see any Ethereum accounts. Would you like to create one?")
				if answer:
					answer = simpledialog.askstring("DDASH","Choose a password: ")
					answer2 = simpledialog.askstring("DDASH","Enter your password again: ")
					if answer == answer2:
						# create new Ethereum account
						self.bci.web3.personal.newAccount(answer)
						self.bci.ethereum_acc_pass=answer
			else: # account(s) found
				if not self.bci.ethereum_acc_pass:
					answer = simpledialog.askstring("DDASH","Enter your Ethereum account password: ")

					self.bci.ethereum_acc_pass=answer

			#self.bci.unlock_account(self.bci.ethereum_acc_pass)

			self.bci.load_contract(contract_name='blackswan', contract_address=blackswan_contract_address)
			self.address_entry.delete(0,END)
			self.address_entry.insert(0, self.bci.get_address())
			#self.address_label.configure(text="Your Ethereum address:\n "+self.bci.get_address())
			self.balance_label.configure(text="Ether Balance:\n "+str(self.bci.get_balance())) 

			if self.swapinterface:
				self.swapcoin_balance_label.configure(text="SwapCoin Balance:\n "+str(self.swapinterface.my_token_balance()))

			#self.gas_entry = Entry(self.master)
				#self.gas_entry.grid(row=5,column=4)

			#self.bci.load_contract(contract_name='recordmanager', contract_address=recordmanager_contract_address)
			#self.fsi.upload_all_files(self.bci)
			#self.fsi.download_all_files(self.bci)

		self.master.after(30000,self.clock)


#default_font=font.nametofont("Courier")
#default_font.configure(size=12)
root = Tk()
#root.option_add("*Font",default_font)
twinpeaks = TwinPeaks(root)
twinpeaks.clock()
root.mainloop()





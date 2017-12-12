from tkinter import *
from tkinter import simpledialog
import subprocess, os
from subprocess import call
import sys, datetime

sys.path.insert(0, os.path.join(os.getcwd(),'ddash'))
from bcinterface import *
from fsinterface import *
from getpass import getpass


# Flags to instruct DDASH to broadcast enode address to blockchain
# and query blockchain for peer enodes
BROADCAST=False
LISTEN=False
blackswan_contract_address="0x5ff2ce40e82e52d370fa9a0ddf49aeee32184756"
recordmanager_contract_address="0xcc109bf72338909ead31a5bf46d8d8fa455ff09b"

MENU_OPTIONS = [
	"Black Swan network",
	"Main Ethereum network"
]


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

		Label(text=intro,relief=RIDGE,font="Courier 14").grid(row=0,columnspan=2,column=0)


		#dialog= simpledialog.askstring(title='question',prompt='please do something')
		#self.label.grid(columnspan=2, sticky=W)
		#self.label = Label(master, text="This is our first GUI!")
		#self.label.pack()

		self.address_label = Label(text="Your Ethereum address: ")
		self.address_label.grid(row=1, columnspan=2)

		self.balance_label = Label(text="Balance: ")
		self.balance_label.grid(row=2, columnspan=2)

		self.variable = StringVar(self.master)
		self.variable.set(MENU_OPTIONS[0])
		self.option = OptionMenu(self.master, self.variable, *MENU_OPTIONS, command=self.dropdown)
		self.option.grid(row=3,columnspan=2)


		self.greet_button = Button(master, text="Launch", command=self.launch)
		self.greet_button.grid(row=4)

		self.close_button = Button(master, text="Close", command=self.close)
		self.close_button.grid(row=4, column=1)


		self.bci = None
		self.fsi = None

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

	def launch(self):

		choice = self.variable.get()

		if choice == MENU_OPTIONS[0]: #Black Swan network selected
				print("Loading ",choice)
				cmd = "./load_blackswan.sh"
				process = subprocess.Popen(cmd,stdin=subprocess.PIPE,
					stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				process.stdin.write("\n".encode())
				process.stdin.write("\n".encode())
				process.stdin.close()
				print (process.stdout.read())
			
				self.bci = BCInterface()
				self.fsi = FSInterface()
				self.contract_name='blackswan'
				self.contract_address=blackswan_contract_address
				self.bci.load_contract(contract_name=self.contract_name, contract_address=self.contract_address)
		if choice == MENU_OPTIONS[1]: #Main Ethereum network
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
				self.contract_name='blackswan'
				self.contract_address=blackswan_contract_address
				self.bci.load_contract(contract_name=self.contract_name, contract_address=self.contract_address)

	def close(self):
		process=subprocess.Popen("tmux kill-session -t geth".split())
		#process=subprocess.Popen("tmux kill-session -t ipfs".split())
		self.master.quit()

	def clock(self):
		time = datetime.datetime.now().strftime("Time: %H:%M:%S")

		if self.bci:
			if len(self.bci.eth_accounts)==0:
				self.address_label.configure(text="No Ethereum account found.")
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

			self.bci.unlock_account(self.bci.ethereum_acc_pass)

			self.bci.load_contract(contract_name='blackswan', contract_address=blackswan_contract_address)
			self.address_label.configure(text="Your Ethereum address:\n "+self.bci.get_address())
			self.balance_label.configure(text="Balance:\n "+str(self.bci.get_balance())) 

			self.bci.load_contract(contract_name='recordmanager', contract_address=recordmanager_contract_address)
			self.fsi.upload_all_files(self.bci)
			self.fsi.download_all_files(self.bci)

		self.master.after(5000,self.clock)


#default_font=font.nametofont("Courier")
#default_font.configure(size=12)
root = Tk()
#root.option_add("*Font",default_font)
twinpeaks = TwinPeaks(root)
twinpeaks.clock()
root.mainloop()



from tkinter import *
import subprocess, os
from subprocess import call
import sys
sys.path.insert(0, os.path.join(os.getcwd(),'ddash'))
import bcinterface

class MyFirstGUI:
	def __init__(self, master):
		self.master = master
		master.title("DDASH")

		intro = r"""
		
		   ____________________________________
		   |  __ \|  __ \   /\    / ____| |  | |
		   | |  | | |  | | /  \  | (___ | |__| |
		   | |  | | |  | |/ /\ \  \___ \|  __  |
		   | |__| | |__| / ____ \ ____) | |  | |
		   |_____/|_____/_/    \_\_____/|_|  |_|
													 
		   ::: Distributed Data Sharing Hyperledger :::

		"""

		Label(text=intro,relief=RIDGE,font="Courier 14").grid(row=0,columnspan=2,column=0)


		#dialog= simpledialog.askstring(title='question',prompt='please do something')
		#self.label.grid(columnspan=2, sticky=W)
		#self.label = Label(master, text="This is our first GUI!")
		#self.label.pack()

		self.greet_button = Button(master, text="Launch", command=self.launch)
		self.greet_button.grid(row=1)

		self.close_button = Button(master, text="Close", command=master.quit)
		self.close_button.grid(row=1, column=1)

	def launch(self):
		print("Greetings!")
		#call(["./log_nodeInfo.sh"])
		#bashCommand = "tmux new-session -d -s geth \"geth --verbosity 3 --datadir="+os.getcwd()+"/ddash/data --networkid 4828 --port 30303 --rpcapi=\"db,eth,net,personal,web3\" --rpc --rpcport 8545 --mine --minerthreads=1 console\""
		#print(bashCommand)
		#call(bashCommand.split())
		cmd = "./gui.sh"
		#call(["./gui.sh"])

		process = subprocess.Popen('./gui.sh',stdin=subprocess.PIPE,
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		process.stdin.write("\n".encode())
		process.stdin.write("\n".encode())
		#process.stdin.write("peer count".encode())

		process.stdin.close()
		print (process.stdout.read())
		#bashCommand = "./log_nodeInfo.sh"
		#process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		#output, error = process.communicate()
		#process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		#output, error=process.communicate()

#default_font=font.nametofont("Courier")
#default_font.configure(size=12)
root = Tk()
#root.option_add("*Font",default_font)
my_gui = MyFirstGUI(root)
root.mainloop()

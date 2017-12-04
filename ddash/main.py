#from crypto import PGPUser
from bcinterface import BCInterface
from getpass import getpass
from fsinterface import *

ethereum_acc_pass = None

# Flags to instruct DDASH to broadcast enode address to blockchain
# and query blockchain for peer enodes
BROADCAST=True
LISTEN=True
blackswan_contract_address="0x5ff2ce40e82e52d370fa9a0ddf49aeee32184756"
recordmanager_contract_address="0xcc109bf72338909ead31a5bf46d8d8fa455ff09b"

intro = r"""

    _____  _____	   _____ _    _ 
   |  __ \|  __ \   /\	  / ____| |  | |
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


print(intro)

def get_contract_name_and_address():
	contract_name=None
	contract_address=None

	contract_name=input("Enter your contract name (leave blank for blackswan)> ")
	while 1:
		contract_address=input("Enter your contract address (leave blank for blackswan)> ")
		if not contract_address: 
			contract_address=blackswan_contract_address

		if not contract_name: 
			contract_name='blackswan' 

		if contract_address and contract_name: break

	return contract_name, contract_address

bci = BCInterface()
fsi = FSInterface()
#u = PGPUser()
#u.load_profile()
contract_name, contract_address = get_contract_name_and_address()
bci.load_contract(contract_name=contract_name, contract_address=contract_address)
loop_counter = 0

while 1:
	result = input("ddash> ")
	BROADCAST=False
	LISTEN=False

	if 'quit' in result or 'exit' in result: break

	if 'sanity check' in result:
		bci.sanity_check()

	'''
	if ('check key' in result) or ('show key' in result) or ('list key' in result):
		u.check_keys()

	if ('set key' in result) or ('use key' in result):
		value = get_value_from_index(result,2)
		u.set_key(value)

	if ('delete key' in result) or ('del key' in result):
		value = get_value_from_index(result,2) 
	   	u.delete_key(value)
		u.save_user()
		u.load_profile()

	if ('new key' in result):
		u.new_keypair()
		u.save_user()
		u.load_profile() 

	if ('set recipient' in result):
		recipient = get_value_from_index(result,2,convert_to='string')
		u.set_recipient(recipient)

	if ('who recipient' in result):
		u.get_recipient()

	if ('set file' in result) or ('use file' in result):
		value = get_value_from_index(result, 2,convert_to="string")
		u.set_file(value)

	if ('which file' in result) or ('get file' in result):
		u.get_current_file()

	if ('which key' in result):
		u.get_current_key() 

	if ('encrypt' in result):
		recipient_pubkey_fingerprint = get_value_from_index(result,1)
		u.encrypt_with_key(recipient_pubkey_fingerprint)

	'''

	if ('upload' in result):
		print("uploading contents of "+os.getcwd()+"/ddash/upload...")
		if not ethereum_acc_pass:
			print("Enter password for account "+bci.eth_accounts[0]+":")
			ethereum_acc_pass=getpass() 
		bci.unlock_account(ethereum_acc_pass)
		bci.load_contract(contract_name='recordmanager',contract_address=recordmanager_contract_address)

		fsi.upload_all_files(bci)
	
	if ('download' in result):
		print("downloading blockchain contents to "+os.getcwd()+"/ddash/download...")
		if not ethereum_acc_pass:
			print("Enter password for account "+bci.eth_accounts[0]+":")
			ethereum_acc_pass=getpass() 
		bci.unlock_account(ethereum_acc_pass)

		bci.load_contract(contract_name='recordmanager',contract_address=recordmanager_contract_address)

		fsi.download_all_files(bci)


	'''
	if ('set directory'  in result):
		workdir = get_value_from_index(result,2,convert_to="string")
		print "Setting directory to", workdir
		u.set_directory(workdir)
	'''

	if ('show account' in result):
		if not ethereum_acc_pass:
			print("Enter password for account "+bci.eth_accounts[0]+":")
			ethereum_acc_pass=getpass() 
		bci.unlock_account(ethereum_acc_pass)

		bci.show_eth_accounts()
	elif ('use account' in result) or ('set account' in result):
		if not ethereum_acc_pass:
			print("Enter password for account "+bci.eth_accounts[0]+":")
			ethereum_acc_pass=getpass() 
		bci.unlock_account(ethereum_acc_pass)

		account_index = get_value_from_index(result,2,convert_to="integer")
		print("Extracted index ",account_index)
		bci.set_account(account_index)
	if ('unlock' in result):
		password = get_value_from_index(result,2,convert_to="string")
		print("Attempting to unlock account...")
		bci.unlock_account(password)

	if ('checkout' in result):
		ipfs_hash = get_value_from_index(result,1,convert_to="string")
		print("Looking for this IPFS hash on the blockchain:",ipfs_hash)
		bci.get_record(ipfs_hash)

	if ( ('broadcast' in result) or BROADCAST):
		if not ethereum_acc_pass:
			print("Enter password for account "+bci.eth_accounts[0]+":")
			ethereum_acc_pass=getpass() 
		bci.unlock_account(ethereum_acc_pass)
		bci.load_contract(contract_name='blackswan',contract_address=blackswan_contract_address)

		enode = fsi.my_enode()  #'myenode123' # my_enode()
		print("Broadcasting enode "+enode+" to the blackswan network.")

		if not ethereum_acc_pass:
			print("Enter password for account "+bci.eth_accounts[0]+":")
			ethereum_acc_pass=getpass() 
		bci.unlock_account(ethereum_acc_pass)
		print(bci.contract.transact(bci.tx).add_entity(enode))

		BROADCAST=False

	if ( ('listen' in result) or LISTEN):
		if not ethereum_acc_pass:
			print("Enter password for account "+bci.eth_accounts[0]+":")
			ethereum_acc_pass=getpass() 
		bci.unlock_account(ethereum_acc_pass)
		bci.load_contract(contract_name='blackswan',contract_address=blackswan_contract_address)

		print("Downloading peer list from blockchain.")
		peers = []
		num_peers = bci.contract.call().get_entity_count()
		if num_peers == 0:
			print("No peers found on chain.")
		else:
			print(str(num_peers)+" peers found on chain.")

		y=0
		while y<num_peers:
			p = bci.contract.call().get_enode_by_row(y)
			print("Adding to list of peers:")
			print(p)
			peers.append(p)
			fsi.update_static_nodes(p)
			y+=1

		LISTEN=False

	# greet omar
	if ('greet omar' in result) or ('omar' in result) or ('hello' in result):
		if not ethereum_acc_pass:
			print("Enter password for account "+bci.eth_accounts[0]+":")
			ethereum_acc_pass=getpass() 
		bci.unlock_account(ethereum_acc_pass)
		bci.load_contract(contract_name='blackswan',contract_address=blackswan_contract_address)

		bci.heyo()

	# format:  contract blackswan 0x...
	if 'contract' in result:
		args = result.split()
		if len(args) != 3:
			print("Example of correct usage:  contract blackswan "+blackswan_contract_address)
		else:
			contract_name = args[1].strip()
			contract_address = args[2].strip()
			bci.load_contract(contract_name=contract_name, contract_address=contract_address)

	if ('friend count' in result) or ('peer count' in result):
		if not ethereum_acc_pass:
			print("Enter password for account "+bci.eth_accounts[0]+":")
			ethereum_acc_pass=getpass() 
		bci.unlock_account(ethereum_acc_pass)
		bci.load_contract(contract_name='blackswan',contract_address=blackswan_contract_address)

		bci.friend_count()

	loop_counter+=1


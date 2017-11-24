from crypto import PGPUser
from interface import Interface
from getpass import getpass
from dynamic import *

ethereum_acc_pass = None

# Flags to instruct DDASH to broadcast enode address to blockchain
# and query blockchain for peer enodes
BROADCAST=True
LISTEN=True

intro = r"""
    _____  _____           _____ _    _ 
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
        print "ValueFromIndex Error."

    return value


print intro
i = Interface()
u = PGPUser()
u.load_profile()
i.load_contract('blackswan')

loop_counter = 0

while 1:
    result = raw_input("ddash> ")
    BROADCAST=True
    LISTEN=True

    if 'quit' in result or 'exit' in result: break

    elif 'sanity check' in result:
        i.sanity_check()

    elif ('check key' in result) or ('show key' in result) or ('list key' in result):
        u.check_keys()

    elif ('set key' in result) or ('use key' in result):
        value = get_value_from_index(result,2)
        u.set_key(value)

    elif ('delete key' in result) or ('del key' in result):
        value = get_value_from_index(result,2) 
        u.delete_key(value)
	u.save_user()
	u.load_profile()

    elif ('new key' in result):
        u.new_keypair()
        u.save_user()
        u.load_profile() 

    elif ('set recipient' in result):
        recipient = get_value_from_index(result,2,convert_to='string')
        u.set_recipient(recipient)

    elif ('who recipient' in result):
        u.get_recipient()

    elif ('set file' in result) or ('use file' in result):
        value = get_value_from_index(result, 2,convert_to="string")
        u.set_file(value)

    elif ('which file' in result) or ('get file' in result):
        u.get_current_file()

    elif ('which key' in result):
        u.get_current_key() 

    elif ('encrypt' in result):
        recipient_pubkey_fingerprint = get_value_from_index(result,1)
        u.encrypt_with_key(recipient_pubkey_fingerprint)

    elif ('upload' in result):
        if not u.file_to_upload: 
            print "No file selected. Please select file using method PGPUser.set_file(filepath)."
        else:
            filename,filehash = i.upload(u.file_to_upload)
            description = get_value_from_index(result, 1, convert_to="string")
            print "Attempting to push the following record to the blockchain:"
            print "filename: ",(filename or description)
            print "filehash: ",filehash
            #print "sender pubkey id",u.keys[u.key_index]['fingerprint']
            print "recipient pubkey id",u.get_recipient()

            i.push_ipfs_hash_to_chain(filehash,(filename or description),u.keys[u.key_index]['fingerprint'],u.get_recipient()) 

    elif ('set directory'  in result):
	workdir = get_value_from_index(result,2,convert_to="string")
	print "Setting directory to", workdir
	u.set_directory(workdir)

    elif ('show account' in result):
	i.show_eth_accounts()

    elif ('use account' in result) or ('set account' in result):
	account_index = get_value_from_index(result,2,convert_to="integer")
	print "Extracted index ",account_index
	i.set_account(account_index)

    elif ('unlock' in result):
	password = get_value_from_index(result,2,convert_to="string")
	print "Attempting to unlock account..."
	i.unlock_account(password)

    elif ('checkout' in result):
	ipfs_hash = get_value_from_index(result,1,convert_to="string")
	print "Looking for this IPFS hash on the blockchain:",ipfs_hash
	i.get_record(ipfs_hash)

    elif ( ('broadcast' in result) or BROADCAST):
	enode = my_enode()  #'myenode123' # my_enode()
	print "Broadcasting enode "+enode+" to the blackswan network."
	if not ethereum_acc_pass:
		print "Enter password for account "+i.eth_accounts[0]+":"
		ethereum_acc_pass=getpass() 
	i.unlock_account(ethereum_acc_pass)
	print i.contract.transact(i.tx).add_entity(enode)
	BROADCAST=False

    elif ( ('listen' in result) or LISTEN):
	if not ethereum_acc_pass:
		print "Enter password for account "+i.eth_accounts[0]+":"
		ethereum_acc_pass=getpass() 

	print "Downloading peer list from blockchain."
	i.unlock_account(ethereum_acc_pass)
	peers = []
	num_peers = i.contract.call().get_entity_count()
	if num_peers == 0:
		print "No peers found on chain."
	else:
		print str(num_peers)+" peers found on chain."

	y=0
	while y<num_peers:
		p = i.contract.call().get_enode_by_row(y)
		print "Adding to list of peers:"
		print p
		peers.append(p)
		update_static_nodes(p)
		y+=1
	LISTEN=False

    loop_counter+=1


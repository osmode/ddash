'''
:::  fsinterface.py									 :::
:::  File system interface to interact with local files :::
'''
import os
from HTMLParser import HTMLParser
from subprocess import Popen, PIPE

class FSInterface:

	def __init__(self):
		return

	# class FSInterface method 'download_all_files' queries blockchain,
	# downloads all files, and reconstructs *.dsc files
	# argument bci is a BCInterface object
	def download_all_files(self,bci,walk_dir=None):
		num_records = bci.contract.call().getRecordCount()
		i=0
		while i < num_records:
			record=bci.get_record_by_row(i)
			owner_address=record[0]
			ipfs_hash=record[1]
			filename=record[2]
			description=record[3]

			# download from IPFS network
			bci.api.get(ipfs_hash)
			bashcommand="mv "+ipfs_hash+" "+os.path.join(os.getcwd(),'download')+"/"+filename

			p=Popen(bashcommand.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
			output, err=p.communicate()

			i+=1


		print "Downloaded "+str(num_records)+" records from the blockchain."



	# argument bci is a BCInterface object
	def upload_all_files(self,bci,walk_dir=None):
		all_files=[]
		if not walk_dir:
			walk_dir=os.path.join(os.getcwd(), 'upload') 		
			print "walk_dir:",walk_dir
		for root, subdirs, files in os.walk(walk_dir):	
			for f in files:
				print f
				file_path=os.path.join(root,f)
				print self.get_ipfs_hash(file_path)

				dsc_file_path=file_path+".dsc"
				all_files.append(file_path)
				if os.path.isfile(dsc_file_path):
					parser=DSCParser()
					with open(dsc_file_path,"r") as dsc_file:
						content=dsc_file.read()
						parser.feed(content.replace('\n',''))
					(owner,description,ipfs,shared_with)= parser.get_dsc_attributes()
					print "tags: ", (owner,description,ipfs,shared_with)
					if 'yes' in ipfs:
						filename,ipfs_hash=bci.upload_to_ipfs(file_path)
					else:
						filename=f
						ipfs_hash=get_ipfs_hash(file_path)
					if not (owner and description and ipfs and shared_with):
						print "Invalid *.dsc file does not contain required fields: owner, description, ipfs, shared_with"
					else:
						print "adding record to blockchain:"
						print "owner_account:",bci.eth_accounts[0]
						print "filename:",filename
						print "ipfs_hash:",ipfs_hash
						print "description:",description

						print bci.add_record(bci.eth_accounts[0],filename,ipfs_hash,description)

					#print "dsc files contents: ",content


		return all_files

	def get_ipfs_hash(self,file_path):
		bashcommand = "ipfs add -n "+file_path.replace('\n','')		
		p=Popen(bashcommand.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE)	
		output, err=p.communicate()
		result=output.split()
		if len(result)!=3:
			print "Unable to generate IPFS hash."
			return 1
		return result[1]

	# function my_enode returns a string with the local machine's enode address
	# using the contents of the nodeInfo.ds file

	def my_enode(self):
		fname=os.getcwd()+'/ddash/nodeInfo.ds'
		with open(fname) as f:
			content=f.readlines()

		enode = content[0].strip().replace('"','').replace('\n','')
		ip = content[1].strip().replace('\n','')

		print enode
		print ip

		# typically [::] is present when running on Ubuntu
		# need to process the enode in this case
		if '[::]' in enode:
			final_enode = enode.replace('[::]',ip).replace('\n','')
		# typically the machine's actual ip address is already appended to enode
		# on Mac OS X 
		else:
			final_enode = enode
			start=enode.find('@')+1
			end=len(enode[enode.find('@'):])+start
			ip=enode[start:end]
		
		print final_enode
		return final_enode

	def file_len(fname):
		with open(fname) as f:
			for i, l in enumerate(f):
				pass
		return i + 1


	def update_static_nodes(enode):
		fname_path=os.getcwd()+'/ddash/data/static-nodes.json'	   
		# avoid duplicate enode entries
		if enode in open(fname_path).read():
			print "enode already exists!"
			return 1

		num_lines = file_len(fname_path)
		line_number = 0
		temp_file_path=os.getcwd()+'/ddash/data/static-nodes2.json'
		temp_file = open(temp_file_path,'w+')

		with open(fname_path) as f:
			for line in f:
				if (num_lines > 2) and line_number == (num_lines-2) : 
					#print "line number: "+str(line_number)+". printing: "+line.strip()
			
					temp_file.write(line.strip()+",\n")
				else:
					#print "line number: "+str(line_number)+". printing: "+line
					temp_file.write(line.strip()+"\n")
		
				if (line_number == (num_lines-2)):
					#print "printing enode: "+enode+"\n"
					temp_file.write('"'+enode.strip()+'"\n')

				line_number+=1

		os.remove(fname_path)
		os.rename(temp_file_path, fname_path)

		return 0
				
# DSCParser is a class that parses *.dsc files
# File information (including IPFS upload status, description,
# and fingerprint_shared_with/fingerprint_shared_by are
# specified in the *.dsc file
class DSCParser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.owner=None
		self.description=None
		self.ipfs=None
		self.shared_with=None
		self.last_tag=None
			
	def handle_starttag(self, tag, attrs):
		self.last_tag=tag
		#print ("Encountered a start tag: ",tag)
	def handle_endtag(self, tag):
		#print ("Encountered an end tag: ",tag)
		pass
	def handle_data(self, data):
		print ("last tag: ",self.last_tag)
		print ("data: ",data)
		if 'owner' in self.last_tag: self.owner=data
		if 'description' in self.last_tag: self.description=data
		if 'ipfs' in self.last_tag: self.ipfs=data
		if 'shared_with' in self.last_tag: self.shared_with=data
		
	def get_dsc_attributes(self):
		return (self.owner, self.description, self.ipfs, self.shared_with)

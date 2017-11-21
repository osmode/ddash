'''

:::  crypto.py 				        :::
::: Easy gnupg keypair encryption/decryption    :::

'''

import gnupg
import os.path, random

class PGPUser:
	""" Instantiate PGP user """
	
	"""
	.. function:: __init__(self, workdir)
	:workdir is the working directory and must be set
	"""
	def __init__(self, workdir='/gnupg'):
		self.workdir = workdir
                self.encrypted_file_store = self.workdir + '/encrypted_file_store'
		self.identities_filename = "identity.pkl"
                self.keypair_filename = "keypair.asc"
		self.identities_path = self.workdir+'/'+self.identities_filename
                self.keypair_path = self.workdir+'/'+self.keypair_filename
		self.gpg = gnupg.GPG(gnupghome=workdir)
		self.keys = self.gpg.list_keys() or [] 
                self.key_index = 0
                self.file_to_upload = None
                self.recipient_pubkey_fingerprint = None
        	
	def set_directory(self, workdir):
		self.workdir = workdir
		self.gpg = gnupg.GPG(gnupghome=self.workdir)
		self.keys = self.gpg.list_keys() or [] 


        # check if PGP keys present on machine
        def check_keys(self):
           #self.keys = self.gpg.list_keys()
           if len(self.keys) > 0: 
               print "The following PGP keys were found: "
               for index,key in enumerate(self.keys):
                   print "key "+str(index)+", keyid: "+key['keyid']+", fingerprint: ",key['fingerprint'] 
               return self.keys
           print "No PGP keys were found."
           return 1

        # choose which PGP key to use
        def set_key(self,index):
            assert(len(self.keys) >0)
            assert(index < len(self.keys))

            self.key_index = index
            print "You're now using keyid "+str(self.keys[self.key_index]['keyid'])

        def delete_key(self,index):
            assert(len(self.keys) > 0)
            assert(index < len(self.keys))

            fp = self.keys[index]['fingerprint']
            print "Deleting private key "+str(index)+"..."
            print str(self.gpg.delete_keys(fp,True))  # delete private key
            print "Deleting public key "+str(index)+"..."
            print str(self.gpg.delete_keys(fp))       # delete pubkey
            return 0

        def load_profile(self):
		# an identities.kc file (located in workdir) 
		# associates aliases with PGP pubkey fingerpints
		# check to see if one already exists on loading
		if os.path.isfile(self.identities_path): 
			with open(self.identities_path,'rb') as f:
			    print "File identities.pkl found in: "+identities_path
                            pass
			    # self.users = pickle.load(f)
                        
                        # print "Loaded user: \'"+self.users.keys()[0]
                        import_result =self.gpg.recv_keys('pgp.mit.edu',self.keys[self.key_index]['fingerprint'])

                if os.path.isfile(self.keypair_path):
                    key_data = open(self.keypair_path).read()
                    import_result = self.gpg.import_keys(key_data)

		    print "Loaded keypair file \'keypair.asc\'"

                self.keys = self.gpg.list_keys() or [] 

                return True



	def new_keypair(self,key_type="RSA",key_length=1024):
		input_data = self.gpg.gen_key_input(key_type=key_type, key_length=key_length)
		self.key = self.gpg.gen_key(input_data)
		print "New keypair was generated, ",self.key
		print "Attempting to save progress.."

		self.save_user()

                print "New PGP key created: "+str(self.key) 

	# method save_user saves an asc file to disk
	# and pickles the identities dict populated with 
	# (key,value) = (alias,pubkey fingerprint)
        # it also uploads the pubkey to a public keyserver
	def save_user(self):
		ascii_armored_public_keys = self.gpg.export_keys(str(self.keys[self.key_index]))
		ascii_armored_private_keys = self.gpg.export_keys(str(self.keys[self.key_index]),True) 
                with open(self.keypair_path,'w') as f:
                    f.write(ascii_armored_public_keys)
                    f.write(ascii_armored_private_keys)

                '''
		with open(self.identities_path,'wb') as f:
			pickle.dump(self.users,f,pickle.HIGHEST_PROTOCOL)
                '''

                self.gpg.send_keys('pgp.mit.edu',self.keys[self.key_index]['fingerprint'])

        
        def set_file(self,filepath):
            if not filepath: 
                print "No filepath specified."
                return 1
            if os.path.isfile(filepath):
                self.file_to_upload = filepath
                "You're now working with "+filepath
                return 0
            else:
                print "Invalid filepath."

            return 1

        def download_key(self, keyid, server_name = 'pgp.mit.edu'):
            try:
                self.gpg.recv_keys(server_name,keyid)
                print "Successfully downloaded keyid "+str(keyid)+" from '"+str(server_name)+"'."
                return 0
            except:
                print "Unable to download keyid "+str(keyid)+" from '"+server_name+"'."
                return 1

        def set_recipient(self,public_fingerprint):
            found = False
            if len(self.keys)==0:
                print "Your keychain has no public keys. Please use download_key(keyid, server_name) to download this pubkey from a PGP server."
                return 1
            for k in self.keys:
                if public_fingerprint in k['fingerprint']: found = True

            if not found:
                print "Your keychain does not contain public key fingerprint "+public_fingerprint+". Please download this pubkey using method download_key(keyid, server_name)."
                return 1

            self.recipient_pubkey_fingerprint = public_fingerprint
            "Recipient set to "+public_fingerprint
            return 0

        def get_current_key(self):
            if len(self.keys) ==0:
                print "No key selected. Try methods Interface.check_keys and Interface.set_key(index)"
                return 1

            assert(self.key_index < len(self.keys))

            curr_key = self.keys[self.key_index]
            curr_key_id = curr_key['keyid'] 
            print "You are using keyid ",curr_key_id
            return curr_key_id 

        def get_current_file(self):
            if not self.file_to_upload:
                print "No file selected. Use method PGPUser.set_file(filepath) to select a file."
                return 1
            print "You are working with file ",self.file_to_upload,". Use method PGPUser.set_file(filepath) to change current file."
            return self.file_to_upload

        def get_recipient(self):
            if not self.recipient_pubkey_fingerprint:
                print "No recipient pubkey fingerprint selected. All uploaded files will be made public."
                return "public"
            print self.recipient_pubkey_fingerprint
            return self.recipient_pubkey_fingerprint
        
        def delete_last_encrypted(self):
            if not self.last_encrypted_filepath:
                print "No recently encrypted files found."
                return 1
            os.remove(self.last_encrypted_filepath)
            return 0

        def generate_nonce(self,length=8):
            return ''.join([str(random.randint(0, 9)) for i in range(length)])

        def encrypt_with_key(self, encrypted_output=None):
            if not encrypted_output: 
                print "Encrypted files will be saved to: ",self.workdir
                encrypted_output = self.encrypted_file_store+'/'+self.generate_nonce()

            if not self.file_to_upload:
                print "No file selected. Please use set_file(filepath) method to specify a file to upload."
                return 1

            if not self.recipient_pubkey_fingerprint:
                print "No recipient pubkey fingerprint selected. All uploaded files will be made public."
                return 1

            if self.recipient_pubkey_fingerprint:
                print "Encrypting "+self.file_to_upload+" with pubkey fingerprint "+self.recipient_pubkey_fingerprint+"..."

                print "Attempting to encrypt using recipients=",self.recipient_pubkey_fingerprint," and output filepath ",encrypted_output

                if not (os.path.isdir(self.encrypted_file_store)):
                        print "Directory ",self.encrypted_file_store," does not exist. Attempting to create..."
                        os.makedirs(self.encrypted_file_store)


                with open(self.file_to_upload,'rb') as f:
                    status = self.gpg.encrypt_file(f, recipients=[self.recipient_pubkey_fingerprint], output = encrypted_output)

                    print "status: ", status.status
                    print "stderr: ",status.stderr

                self.file_to_upload = encrypted_output
                self.last_encrypted_filepath = encrypted_output

                return 0

        def decrypt(self,encrypted_file_location, output_filepath):
            print "Decrypting file "+encrypted_file_location+"..."
            with open(encrypted_file_location,'rb') as f:
                status = gpg.decrypt_file(f,
                    output=output_filepath)
                print "status: ",status.status
                print "stderr: ",status.stderr
            
            print "Successfully saved decrypted file to ",output_filepath

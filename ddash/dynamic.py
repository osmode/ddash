'''
:::  dynamic.py                                   :::
:::  Read local files in DDASH                    :::
'''
import os

# function my_enode returns a string with the local machine's enode address
# using the contents of the nodeInfo.ds file
def my_enode():
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
				

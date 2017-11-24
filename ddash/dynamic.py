'''
:::  dynamic.py                                   :::
:::  Read local files in DDASH                    :::
'''
import os

# function my_enode returns a string with the local machine's enode address
# using the contents of the nodeInfo.ds file
def my_enode():
	fname=os.getcwd()+'/nodeInfo.ds'
	with open(fname) as f:
	    content=f.readlines()

	enode = content[0].replace('"','').replace('\n','')
	ip = content[1].replace('\n','')

	print enode
	print ip

	if '[::]' in enode:
	    final_enode = enode.replace('[::]',ip).replace('\n','')
	else:
	    final_enode = enode

	print final_enode


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def update_static_nodes(enode):
	fname=os.chwd()+'/ddash/data/static-nodes.json'       
	num_lines = file_len(



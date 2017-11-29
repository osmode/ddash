pragma solidity ^0.4.0;
contract RecordManager {

	struct RecordStruct {

	 string owner_name;
	 address owner_address;
         string ipfs_hash;
         string description;
         string shared_with_fingerprint;
         string shared_by_fingerprint;
	 bool isRecord;
	}
    mapping (string => RecordStruct) recordsByIPFSHash;

    string[] public recordListByIPFSHash;

    
    function is_record(string _ipfs_hash) public constant returns(bool isIndeed) {
	    return recordsByIPFSHash[_ipfs_hash].isRecord;    
    }
    

    function get_record_count() public constant returns(uint recordCount) {
	 return recordListByIPFSHash.length;
    }

    function new_record(string _owner_name, address _owner_address, string _ipfs_hash, string _description, string _shared_with_fingerprint, string _shared_by_fingerprint) public returns(uint rowNumber) {

	if(is_record(_ipfs_hash)) revert();
	recordsByIPFSHash[_ipfs_hash].owner_name=_owner_name;
	recordsByIPFSHash[_ipfs_hash].owner_address=msg.sender;
	recordsByIPFSHash[_ipfs_hash].ipfs_hash=_ipfs_hash;
	recordsByIPFSHash[_ipfs_hash].description=_description;
	recordsByIPFSHash[_ipfs_hash].shared_with_fingerprint=_shared_with_fingerprint;
	recordsByIPFSHash[_ipfs_hash].shared_by_fingerprint=_shared_by_fingerprint;
	recordsByIPFSHash[_ipfs_hash].isRecord=true;
	return recordListByIPFSHash.push(_ipfs_hash)-1;

    }

    address public owner;
    string[5] greetings;

    function RecordManager() payable {
	  owner = msg.sender;
        
	  greetings[0] = "Hi, my name is Omar Metwally.";
	  greetings[1] = "I am the creator of this contract.";
	  greetings[2] = "Black Swan Lives!";
	  greetings[3] = "Watching Parnassus on a beautiful, sunny day in SF...";
	  greetings[4] = "Healthcare is a human right.";
	}
	
	/*
    event NewRecord (
	owner_name, owner_address, ipfs_hash, description, shared_with_fingerprint, shared_by_fingerprint);
    */
    
    function add_record(string _owner_name, address _owner_address, string _ipfs_hash, string _description, string _shared_with_fingerprint, string _shared_by_fingerprint) {
	if (is_record(_ipfs_hash)) {
	    revert();
	} else {
	    new_record(_owner_name, _owner_address, _ipfs_hash, _description, _shared_with_fingerprint, _shared_by_fingerprint);
	    RecordCreated(_owner_name, _owner_address, _ipfs_hash, _description, _shared_with_fingerprint, _shared_by_fingerprint);
	}

    }

    /* Generates a random number from 0 to 10 based on the last block hash */
    function randomGen(uint seed) constant returns (uint randomNumber) {
        return(uint(sha3(block.blockhash(block.number-1), seed ))%10);
    }
	
	event RecordCreated (
		string _owner_name,
		address _owner_address,
		string _ipfs_hash,
		string _description,
		string _shared_with_fingerprint,
		string _shared_by_fingerprint
	);


	function get_record_by_row(uint row) public returns (string _owner_name, address _owner_address,string _ipfs_hash,string _description, string _shared_with_fingerprint, string _shared_by_fingerprint) {

	   require(row<recordListByIPFSHash.length);
	   require(row>=0);

	   _owner_name=recordsByIPFSHash[recordListByIPFSHash[row]].owner_name;
	   _owner_address=recordsByIPFSHash[recordListByIPFSHash[row]].owner_address;

	   _ipfs_hash=recordsByIPFSHash[recordListByIPFSHash[row]].ipfs_hash;
	   _description=recordsByIPFSHash[recordListByIPFSHash[row]].description;
	   _shared_with_fingerprint=recordsByIPFSHash[recordListByIPFSHash[row]].shared_with_fingerprint;

	    _shared_by_fingerprint=recordsByIPFSHash[recordListByIPFSHash[row]].shared_by_fingerprint;

	}

	function get_record_by_ipfs_hash(string ipfs_hash) public returns (string _owner_name, address _owner_address,string _ipfs_hash,string _description, string _shared_with_fingerprint, string _shared_by_fingerprint) {

	   require(is_record(ipfs_hash));

	   _owner_name=recordsByIPFSHash[ipfs_hash].owner_name;
	   _owner_address=recordsByIPFSHash[ipfs_hash].owner_address;

	   _ipfs_hash=recordsByIPFSHash[ipfs_hash].ipfs_hash;
	   _description=recordsByIPFSHash[ipfs_hash].description;
	   _shared_with_fingerprint=recordsByIPFSHash[ipfs_hash].shared_with_fingerprint;

	    _shared_by_fingerprint=recordsByIPFSHash[ipfs_hash].shared_by_fingerprint;

	}

	function greet_omar(uint _i) public returns (string greeting) {
		require(_i>=0);
		require(_i<greetings.length);
		return greetings[_i];
	}

	function die() public {
			if (msg.sender == owner) {

				selfdestruct(owner);
			}
	}
}		


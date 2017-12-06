pragma solidity ^0.4.0;
contract Swap {

	struct SwapTransactionObj {
        uint pvn_to_ether_amt;
        uint eth_to_pvn_amt;
        address eth_addr;
        address pvn_addr;
        uint exchange_rate;
        uint timestamp;
        bytes32 hash;
        bool isTx;
	}
    mapping (bytes32 => SwapTransactionObj) swapTransactions;
    bytes32[] public swapTransactionList;
    mapping (address => uint) eth_balance;
    mapping (address => uint) pvn_balance;

    function is_transaction(bytes32 _transaction_hash) public constant returns(bool isIndeed) {
	    return swapTransactions[_transaction_hash].isTx;    
    }

    function get_transaction_count() public constant returns(uint transactionCount) {
	 return swapTransactionList.length;
    }

    function make_hash(uint _pvn_to_eth_amt, uint _eth_to_pvn_amt, address _eth_addr, address _pvn_addr, uint _exchange_rate) public returns (bytes32 hash) {
        //hash = bytes32(_pvn_to_eth_amt);
        
        hash = bytes32(_pvn_to_eth_amt) | bytes32(_eth_to_pvn_amt);
        hash = hash | bytes32(_eth_addr);
        hash = hash | bytes32(_pvn_addr);
        hash = hash | bytes32(block.timestamp);
        hash = hash | bytes32(_exchange_rate);
    }
    
    function new_transaction(uint _pvn_to_eth_amt, uint _eth_to_pvn_amt, address _eth_addr, address _pvn_addr, uint _exchange_rate) public returns (uint rowNumber) {
        bytes32 _hash = make_hash(_pvn_to_eth_amt, _eth_to_pvn_amt, _eth_addr, _pvn_addr, _exchange_rate);
        
	    if(is_transaction(_hash)) revert();
	    require( _pvn_to_eth_amt * _eth_to_pvn_amt ==0 );
	    require (_pvn_to_eth_amt>0 || _eth_to_pvn_amt>0);
	    
	    // converting from pvn_eth to eth 
	    if (_pvn_to_eth_amt > 0 && _eth_to_pvn_amt ==0) {
	        
	        require( pvn_balance[_pvn_addr] - _pvn_to_eth_amt > 0);
	        eth_balance[_eth_addr] += (_pvn_to_eth_amt / master_exchange_rate);
	        pvn_balance[_pvn_addr] -= (_pvn_to_eth_amt);
	    }
	    
	    // converting from eth to pvn_eth
	    if (_eth_to_pvn_amt > 0 && _pvn_to_eth_amt==0) {
	        
	        require( eth_balance[_eth_addr] - _eth_to_pvn_amt > 0 );
	        eth_balance[_eth_addr] -= _eth_to_pvn_amt;
	        pvn_balance[_pvn_addr] += (_eth_to_pvn_amt * master_exchange_rate);
	    }
	    
	    swapTransactions[_hash] = SwapTransactionObj({
	        pvn_to_ether_amt: _pvn_to_eth_amt,
	        eth_to_pvn_amt: _eth_to_pvn_amt,
	        eth_addr: _eth_addr,
	        pvn_addr: _pvn_addr,
	        exchange_rate: _exchange_rate,
	        timestamp: block.timestamp,
	        hash: _hash,
	        isTx: true
	       
	    });
	
	    return swapTransactionList.push(_hash)-1;

    }

    address public owner;
    uint master_exchange_rate;
    string[5] greetings;

    function Swap() public payable {
	  owner = msg.sender;
	  master_exchange_rate = 1000;
        
	  greetings[0] = "Hi, my name is Omar Metwally.";
	  greetings[1] = "I am the creator of this contract.";
	  greetings[2] = "Black Swan Lives!";
	  greetings[3] = "Watching Parnassus on a beautiful, sunny day in SF...";
	  greetings[4] = "Healthcare is a human right.";
	}
	
	/*
    event NewRecord (
	owner_name, owner_address, ipfs_hash, description, shared_with_fingerprint, shared_by_fingerprint);
    
    function add_record(string _owner_name, address _owner_address, string _fname, string _ipfs_hash, string _description ) public returns (uint rowNumber) {
	if (is_record(_ipfs_hash)) {
        update_record( _owner_name, _owner_address, _fname, _ipfs_hash, _description );
	} else {
	    new_record(_owner_name, _owner_address, _fname, _ipfs_hash, _description );
	   // RecordCreated(_owner_name, _ipfs_hash, _description );
	}

    }
    
    function update_record( string _owner_name, address _owner_address, string _fname, string _ipfs_hash, string _description ) public  {
            if(!is_record(_ipfs_hash)) revert();
            recordStructs[_ipfs_hash].owner_name=_owner_name;
            recordStructs[_ipfs_hash].owner_address=_owner_address;
            recordStructs[_ipfs_hash].fname=_fname;
			recordStructs[_ipfs_hash].ipfs_hash=_ipfs_hash;
            recordStructs[_ipfs_hash].descr=_description;
        } 
    */

    /* Generates a random number from 0 to 10 based on the last block hash */
    function randomGen(uint seed) public constant returns (uint randomNumber) {
        return(uint(sha3(block.blockhash(block.number-1), seed ))%10);
    }
	
	/*
	event RecordCreated (
		string _owner_name,
		address _owner_address,
		string _fname,
		string _ipfs_hash,
		string _description
	);
    */
    

	function get_transaction_by_row(uint row) public constant returns (uint pvn_to_ether_amt, uint eth_to_pvn_amt, address eth_addr, address pvn_addr, uint exchange_rate, uint timestamp, bytes32 hash) {

	   require(row<swapTransactionList.length);
	   require(row>=0);

	   pvn_to_ether_amt=swapTransactions[swapTransactionList[row]].pvn_to_ether_amt;
	   eth_to_pvn_amt=swapTransactions[swapTransactionList[row]].eth_to_pvn_amt;
	   eth_addr=swapTransactions[swapTransactionList[row]].eth_addr;
	   pvn_addr=swapTransactions[swapTransactionList[row]].pvn_addr;
	   exchange_rate=swapTransactions[swapTransactionList[row]].exchange_rate;
	   timestamp=swapTransactions[swapTransactionList[row]].timestamp;
	   hash=swapTransactions[swapTransactionList[row]].hash;
	}
	
	function set_master_exchange_rate(uint new_rate) public constant returns (uint exchange_rate) {
	    require(msg.sender == owner);
	    master_exchange_rate = new_rate;
	    return master_exchange_rate;
	}
    
    /*
	function get_record_by_ipfs_hash(string ipfs_hash) public constant returns (string _owner_name, address _owner_address, string _fname, string _ipfs_hash, string _description ) {

	   require(is_record(ipfs_hash));

	   _owner_name=recordStructs[ipfs_hash].owner_name;
	   _owner_address=recordStructs[ipfs_hash].owner_address;
	   _fname=recordStructs[ipfs_hash].fname;
	   _ipfs_hash=recordStructs[ipfs_hash].ipfs_hash;
	   _description=recordStructs[ipfs_hash].descr;
	}
	*/

	function greet_omar(uint _i) public constant returns (string greeting) {
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



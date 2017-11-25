pragma solidity ^0.4.0;
contract BlackSwan {

	struct EntityStruct {

	    string enode;
	    bool isEntity;
	}

	mapping(address => EntityStruct) public entityStructs;
	address[] public entityList;
	
	function is_entity(address entityAddress) public constant returns(bool isIndeed) {
		return entityStructs[entityAddress].isEntity;
	   }

	function get_entity_count() public constant returns(uint entityCount) {
		return entityList.length;
	}

	function new_entity(address entityAddress, string enode) public returns(uint rowNumber) {

		if(is_entity(entityAddress)) revert();
		entityStructs[entityAddress].enode = enode;
		entityStructs[entityAddress].isEntity = true;
		return entityList.push(entityAddress) -1;
	}

	function update_entity(address entityAddress, string enode) public returns(bool success) {
		if(!is_entity(entityAddress)) revert();
		entityStructs[entityAddress].enode = enode;
		return true;
	}

	address public owner;
	string[5] greetings;

	function BlackSwan() payable {
		owner = msg.sender;
        
		greetings[0] = "Hi, my name is Omar Metwally.";
		greetings[1] = "I am the creator of this contract.";
		greetings[2] = "Black Swan Lives!";
		greetings[3] = "Watching Parnassus on a beautiful, sunny day in SF...";
		greetings[4] = "Healthcare is a human right.";
	}
	
    /* Generates a random number from 0 to 10 based on the last block hash */
    function randomGen(uint seed) constant returns (uint randomNumber) {
        return(uint(sha3(block.blockhash(block.number-1), seed ))%10);
    }
	
	event NewEntity (
		address addr,
		string enode
	);

    function add_entity(string enode) public returns(uint rowNumber) {
	if (is_entity(msg.sender)) {
		update_entity(msg.sender, enode);
	} else {
		new_entity(msg.sender, enode);
	}
    }

	// retrieve record using IPFS hash (input)
	// returns Record elements, namely id, ipfs hash, description, 
	// shared_by_fingerprint and shared_with_fingerprint
	function sender_enode() public returns (string _enode) {

	    //if (isEntity(msg.sender)) {
		//return entityStructs[entityList[0]].enode;
		_enode = entityStructs[entityList[0]].enode;
	    //return entityList[0];
	    //} 

	    //return "null";
	}
	
	function get_enode_by_row(uint row) public returns (string _enode) {

	    //if (isEntity(msg.sender)) {
		//return entityStructs[entityList[0]].enode;
		_enode = entityStructs[entityList[row]].enode;
	    //return entityList[0];
	    //} 

	    //return "null";
	}	
	  
	function greet_omar(uint _i) public returns (string greeting) {
		require(_i>=0);
		require(_i<greetings.length);
		return greetings[_i];
	}

}		



pragma solidity ^0.4.0;
contract BlackSwan {

	struct EntityStruct {

	    string enode;
	    bool isEntity;
	}

	mapping(address => EntityStruct) public entityStructs;
	address[] public entityList;
	
	function isEntity(address entityAddress) public constant returns(bool isIndeed) {
		return entityStructs[entityAddress].isEntity;
	   }

	function getEntityCount() public constant returns(uint entityCount) {
		return entityList.length;
	}

	function newEntity(address entityAddress, string enode) public returns(uint rowNumber) {

		if(isEntity(entityAddress)) revert();
		entityStructs[entityAddress].enode = enode;
		entityStructs[entityAddress].isEntity = true;
		return entityList.push(entityAddress) -1;
	}

	function updateEntity(address entityAddress, string enode) public returns(bool success) {
		if(!isEntity(entityAddress)) revert();
		entityStructs[entityAddress].enode = enode;
		return true;
	}

	address public owner;
	string[6] greetings;

	function BlackSwan()  {
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
	if (isEntity(msg.sender)) {
		updateEntity(msg.sender, enode);
	} else {
		newEntity(msg.sender, enode);
	}
    }

	// retrieve record using IPFS hash (input)
	// returns Record elements, namely id, ipfs hash, description, 
	// shared_by_fingerprint and shared_with_fingerprint
	function get_enode() public returns (string _enode) {

	    if (isEntity(msg.sender)) {
		return entityStructs[msg.sender].enode;
	    } 

	    return "null";
	}
	  
	function greet_omar(uint _i) public returns (string greeting) {
		require(_i>=0);
		require(_i<greetings.length);
		return greetings[_i];
	}

}		


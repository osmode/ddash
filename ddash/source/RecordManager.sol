pragma solidity ^0.4.0;
contract RecordManager {

        struct Record {
		address owner_address;
        string ipfs_hash;
		string fname;
		string desc;
        bool isRecord;
        }

    mapping (string => Record) records;
    string[] public recordList;

        function isRecord(string ipfs_hash) public constant returns(bool isIndeed) {
            return records[ipfs_hash].isRecord;
        }

        function getRecordCount() public constant returns(uint recordCount) {
            return recordList.length;
        }

        function newRecord(string ipfs_hash, string fname, string desc) public returns(uint rowNumber) {
                if(isRecord(ipfs_hash)) throw;
				records[ipfs_hash].owner_address=msg.sender;
                records[ipfs_hash].ipfs_hash=ipfs_hash;
				records[ipfs_hash].fname=fname;
				records[ipfs_hash].desc=desc;
                records[ipfs_hash].isRecord=true;
                return recordList.push(ipfs_hash) -1;
        }


		function addRecord(string ipfs_hash, string fname, string desc) public returns (uint rowNumber) {
				if (isRecord(ipfs_hash)) {
					updateRecord(ipfs_hash, fname, desc);
				} else {
					newRecord(ipfs_hash, fname, desc);
				}
		}

		function updateRecord(string ipfs_hash, string fname, string desc) public {
			if(!isRecord(ipfs_hash)) revert();
			records[ipfs_hash].owner_address=msg.sender;
			records[ipfs_hash].fname=fname;
			records[ipfs_hash].desc=desc;
		}
        address public owner;

        string[6] greetings;

        function RecordManager() payable {
                owner = msg.sender;

                greetings[0] = "Hi, my name is Omar Metwally.";
                greetings[1] = "I am the creator of this contract.";
                greetings[2] = "Black Swan Lives!";
                greetings[3] = "Watching Parnassus on a beautiful, sunny day in SF...";
                greetings[4] = "Healthcare is a human right.";
        }

		function getRecordByRow(uint row) public constant returns (address owner_address,string ipfs_hash, string fname, string desc) {

			if(!isRecord(recordList[row])) throw;
			owner_address = records[recordList[row]].owner_address;
			ipfs_hash = records[recordList[row]].ipfs_hash;
			fname = records[recordList[row]].fname;
			desc = records[recordList[row]].desc;
		}


    /* Generates a random number from 0 to 10 based on the last block hash */
    function randomGen(uint seed) constant returns (uint randomNumber) {
        return(uint(sha3(block.blockhash(block.number-1), seed ))%10);
    }

        function greet_omar(uint _i) public returns (string greeting) {
                require(_i>=0);
                require(_i<greetings.length);
                return greetings[_i];
        }

        function die() public {
                        if (msg.sender == owner) {
                                suicide(owner);
                        }
        }
}


pragma solidity ^0.4.0;

contract owned {
    address public owner;

    function owned() {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function transferOwnership(address newOwner) onlyOwner {
        owner = newOwner;
    }
}

/**
 * The Nilometer contract 
 */
contract Nilometer is owned {

    address public fundsRecipient;
    
	// prevent duplicate proposals
	mapping (bytes32 => bool) recordHashes;
	
	uint public waitingPeriodInDays;

    event ProposalAdded(uint proposalID, uint minWaterLevel, uint supportAmount);
    event ProposalExecuted(uint proposalID);
    event ChangeOfRules(address fundsRecipient, uint daysToWait);

    struct Record {

        uint waterLevel;  // in centimeters 
        uint timestamp;
    }
    
    struct Proposal {
        uint minWaterLevel;
        uint supportAmount;
        address proposer;
        uint votingDeadline;
        uint timestamp;
        bool executed;
    }
    
    Record[] public records;
    Proposal[] public proposals;
    mapping (address => uint256) public balanceOf;
    uint256 public totalFunds;
    
    
    function get_proposal_count() public constant returns (uint count) {
        return proposals.length;
    }
    
    function get_record_count() public constant returns (uint count) {
        return records.length;
    }
    
    function get_record_by_row(uint row) public constant returns (uint waterLevel,
        uint timestamp, bytes32 recordHash) {
            
            require(row<records.length);
            require(row>=0);
            
            Record storage r = records[row];
            waterLevel = r.waterLevel;
            timestamp = r.timestamp;
        }
        
    function get_proposal_by_row(uint row) public constant returns (uint minWaterLevel,
        uint supportAmount, address proposer, uint votingDeadline, uint timestamp, bool executed) {
            
            require(row<proposals.length);
            require(row>=0);
            
            Proposal storage p = proposals[row];
            minWaterLevel = p.minWaterLevel;
            supportAmount = p.supportAmount;
            proposer = p.proposer;
            votingDeadline = p.votingDeadline;
            timestamp = p.timestamp;
            executed = p.executed;
        }

    /**
     * Constructor function
     *
     * First time setup
     */
    function Nilometer() payable {
        // by default, the fundsRecipient is the contract address
        // and daysToWait = 30
        changeVotingRules(this, 30);
    }
    
    // fallback function 
    function() payable public {}

    /**
     * Change voting rules
     *
     * Make so that proposals need to be discussed for at least `minutesForDebate/60` hours
     * and all voters combined must own more than `minimumSharesToPassAVote` shares of token `sharesAddress` to be executed
     */
    function changeVotingRules(address _fundsRecipient, uint _daysToWait) onlyOwner {
        fundsRecipient = _fundsRecipient;
        waitingPeriodInDays = _daysToWait;
        
        ChangeOfRules(_fundsRecipient, _daysToWait);
    }

    /**
     * Add new water level
     * 
     * @param waterLevel - Nile water level in centimeters (not in meters to avoid floating points)
     **/
     
     function newRecord(uint waterLevel) payable public onlyOwner returns (uint recordID)  {
        // prevent duplicate proposals
		bytes32 hash = sha3(waterLevel, now);
		assert( !recordHashes[hash]); 
		
		recordID = records.length++;
        Record storage r = records[recordID];
        r.waterLevel = waterLevel;
        r.timestamp = now;
     }

    /**
     * Add Proposal
     *
     *
     * @param minWaterLevel is the minimum Nile water level which will trigger proposal execution
     * @param supportAmount is the amount of wei the proposer will pay if proposal successfully executes
     */
        
    function newProposal(
        uint minWaterLevel, uint supportAmount
    ) payable
        returns (uint proposalID)
    {
        proposalID = proposals.length++;
        Proposal storage p = proposals[proposalID];
        p.minWaterLevel = minWaterLevel;
        p.supportAmount = supportAmount;
        p.proposer = msg.sender;
        p.votingDeadline = now + waitingPeriodInDays * 1 days;
        p.timestamp = now;
        p.executed = false;

        // transfer supporting funds to contract address
        this.transfer(msg.value);
        ProposalAdded(proposalID, minWaterLevel, supportAmount);

        return proposalID;
    }

    /**
     * Finish vote
     *
     * Count the votes proposal #`proposalNumber` and execute it if approved
     *
     * @param proposalNumber proposal number
     */
    function executeProposal(uint proposalNumber) {
        Proposal storage p = proposals[proposalNumber];

        require(now > p.votingDeadline                                             // If it is past the voting deadline
            && !p.executed);                                                          // and it has not already been executed

        // ensure that the last water level was recorded after the proposal was submitted
        require(records[records.length-1].timestamp > p.timestamp);
        
        // check if p.waterLevel is >= last water level
        require(p.minWaterLevel >= records[records.length-1].waterLevel);
        
        // transfer supporting funds from contract address to fundsRecipient
        fundsRecipient.transfer(p.supportAmount);
        
        p.executed = true;

        // Fire Events
        ProposalExecuted(proposalNumber);
    }
}



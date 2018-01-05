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


contract Token is owned {
    mapping (address => uint256) public balanceOf;
    uint256 public totalSupply;
    
    // This generates a public event on the blockchain that will notify clients
    event Transfer(address indexed from, address indexed to, uint256 value);
    
    /**
     * Internal transfer, only can be called by this contract
     */
    function _transfer_token(address _from, address _to, uint _value) internal {
        // Prevent transfer to 0x0 address. Use burn() instead
        require(_to != 0x0);
        // Check if the sender has enough
        require(balanceOf[_from] >= _value);
        // Check for overflows
        require(balanceOf[_to] + _value > balanceOf[_to]);
        // Save this for an assertion in the future
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        // Subtract from the sender
        balanceOf[_from] -= _value;
        // Add the same to the recipient
        balanceOf[_to] += _value;
        Transfer(_from, _to, _value);
        // Asserts are used to use static analysis to find bugs in your code. They should never fail
        assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
    }
    
    /**
     * Transfer tokens
     *
     * Send `_value` tokens to `_to` from your account
     *
     * @param _to The address of the recipient
     * @param _value the amount to send
     */
    function transfer_token(address _to, uint256 _value) public {
        _transfer_token(msg.sender, _to, _value);
    }

    /// @notice Create `mintedAmount` tokens and send it to `target`
    /// @param target Address to receive the tokens
    /// @param mintedAmount the amount of tokens it will receive
    function mintToken(address target, uint256 mintedAmount) onlyOwner public {
        balanceOf[target] += mintedAmount;
        totalSupply += mintedAmount;
        Transfer(0, this, mintedAmount);
        Transfer(this, target, mintedAmount);
    }
    
    
    
}

/**
 * The Manifesto contract 
 */
contract Manifesto is owned {

    uint public minimumQuorum;
    uint public debatingPeriodInMinutes;
    uint public numProposals;
    
    // shares proportionally give weight to votes 
    mapping (address => uint) sharesTokenAddress; 

	// prevent duplicate proposals
	mapping (bytes32 => bool) proposalHashes;

    event ProposalAdded(uint proposalID, string description);
    event Voted(uint proposalID, bool position, address voter);
    event ProposalTallied(uint proposalID, uint result, uint quorum, bool active);
    event ChangeOfRules(uint newMinimumQuorum, uint newDebatingPeriodInMinutes, bool onlyShareholders);

    struct Proposal {

        string description;
        uint votingDeadline;
        bool executed;
        bool proposalPassed;
        uint numberOfVotes;
        bytes32 proposalHash;
        Vote[] votes;
        mapping (address => bool) voted;
    }
    
    struct Vote {
        bool inSupport;
        address voter;
    }
    
    Proposal[] public proposals;
    
    function get_proposal_count() public constant returns (uint count) {
        return proposals.length;
    }
    
    function setShares(address shareholder, uint shares) {
        // only the owner can dispense shares 
        require(msg.sender == owner);
        sharesTokenAddress[shareholder] = shares;
        
    }
    
    function get_proposal_by_row(uint row) public constant returns (string description,
        uint votingDeadline, bool executed, bool proposalPassed, uint numberOfVotes,
        bytes32 proposalHash) {
            
            require(row<proposals.length);
            require(row>=0);
            
            Proposal storage p = proposals[row];
            
            description = p.description;
            votingDeadline = p.votingDeadline;
            executed = p.executed;
            proposalPassed = p.proposalPassed;
            numberOfVotes = p.numberOfVotes;
            proposalHash = p.proposalHash;
        }

    // Modifier that allows only shareholders to vote and create new proposals
    modifier onlyShareholders {
        require(sharesTokenAddress[msg.sender] > 0);
        _;
    }

    /**
     * Constructor function
     *
     * First time setup
     */
    function Manifesto(uint minimumQuorum, uint minutesForDebate) payable {
        changeVotingRules(minimumQuorum, minutesForDebate);
    }

    /**
     * Change voting rules
     *
     * Make so that proposals need to be discussed for at least `minutesForDebate/60` hours
     * and all voters combined must own more than `minimumSharesToPassAVote` shares of token `sharesAddress` to be executed
     *
     * @param minimumSharesToPassAVote proposal can vote only if the sum of shares held by all voters exceed this number
     * @param minutesForDebate the minimum amount of delay between when a proposal is made and when it can be executed
     */
    function changeVotingRules(uint minimumSharesToPassAVote, uint minutesForDebate) onlyOwner {
        
        if (minimumSharesToPassAVote == 0 ) minimumSharesToPassAVote = 1;
        minimumQuorum = minimumSharesToPassAVote;
        debatingPeriodInMinutes = minutesForDebate;
        ChangeOfRules(minimumQuorum, debatingPeriodInMinutes, true);
    }

    /**
     * Add Proposal
     *
     *
     * @param description of the proposal 
     */
     

    function newProposal(
        string description
    )
        returns (uint proposalID)
    {
        // prevent duplicate proposals
		bytes32 hash = sha3(description);
		assert( !proposalHashes[hash]); 

        proposalID = proposals.length++;
        Proposal storage p = proposals[proposalID];
        p.description = description;
        p.proposalHash = hash;
        p.votingDeadline = now + debatingPeriodInMinutes * 1 minutes;
        p.executed = false;
        p.proposalPassed = false;
        p.numberOfVotes = 0;
		proposalHashes[hash] = true;
        
        ProposalAdded(proposalID, description);
        numProposals = proposalID+1;
        
        return proposalID;
    }
    
    /**
     * Log a vote for a proposal
     *
     * Vote `supportsProposal? in support of : against` proposal #`proposalNumber`
     *
     * @param proposalNumber number of proposal
     * @param supportsProposal either in favor or against it
     */
    function vote(
        uint proposalNumber,
        bool supportsProposal
    )
        returns (uint voteID)
    {
        Proposal storage p = proposals[proposalNumber];
        require(p.voted[msg.sender] != true);

        voteID = p.votes.length++;
        p.voted[msg.sender] = true;
        p.numberOfVotes = voteID +1;
        Voted(proposalNumber,  supportsProposal, msg.sender);
        return voteID;
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


        // ...then tally the results
        uint quorum = 0;
        uint yea = 0;
        uint nay = 0;

        for (uint i = 0; i <  p.votes.length; ++i) {
            Vote storage v = p.votes[i];
            //uint voteWeight = sharesTokenAddress[v.voter];
			uint voteWeight = 1;
            quorum += voteWeight;
            if (v.inSupport) {
                yea += voteWeight;
            } else {
                nay += voteWeight;
            }
        }

        require(quorum >= minimumQuorum); // Check if a minimum quorum has been reached

        if (yea > nay ) {
            // Proposal passed; execute the transaction

            p.executed = true;

            p.proposalPassed = true;
        } else {
            // Proposal failed
            p.proposalPassed = false;
        }

        // Fire Events
        ProposalTallied(proposalNumber, yea - nay, quorum, p.proposalPassed);
    }
}


pragma solidity ^0.4.0;

contract owned {
    address public owner;

    function owned() public {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }
}

/*
interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) public; }

*/
contract TokenERC20 {
    // Public variables of the token
    string public name;
    string public symbol;
    uint8 public decimals = 18;
    // 18 decimals is the strongly suggested default, avoid changing it
    uint256 public totalSupply;

    // This creates an array with all balances
    mapping (address => uint256) public token_balance;  // NFO coin token balance on main net 
    mapping (address => uint256)  public eth_balance;   // associates Ethereum deposited on main net with main net addrress  
    mapping (address => uint256) public pvn_token_balance;  // NFO coin token balance on private net 
    mapping (address => mapping (address => uint256)) public allowance;

    // This generates a public event on the blockchain that will notify clients
    event Transfer(address indexed from, address indexed to, uint256 value);

    // This notifies clients about the amount burnt
    event Burn(address indexed from, uint256 value);

    /**
     * Constrctor function
     *
     * Initializes contract with initial supply tokens to the creator of the contract
     */
    function TokenERC20(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public payable {
				// Update total supply with the decimal amount
				totalSupply = initialSupply * 10 ** uint256(decimals);          

				// Give the creator all initial tokens
				token_balance[msg.sender] = totalSupply;                

				// initialize Ether balance of NFO Coin contract 
				eth_balance[msg.sender] = msg.value;                    
				// Set the name for display purposes

				name = tokenName;                                               
				// Set the symbol for display purposes
				symbol = tokenSymbol;                                   
		}

    /**
     * Internal transfer, only can be called by this contract
     */
    function _transfer_token(address _from, address _to, uint _value) internal {
        // Prevent transfer to 0x0 address. Use burn() instead
        require(_to != 0x0);
        // Check if the sender has enough
        require(token_balance[_from] >= _value);
        // Check for overflows
        require(token_balance[_to] + _value > token_balance[_to]);
        // Save this for an assertion in the future
        uint previousBalances = token_balance[_from] + token_balance[_to];
        // Subtract from the sender
        token_balance[_from] -= _value;
        // Add the same to the recipient
        token_balance[_to] += _value;
        Transfer(_from, _to, _value);
        // Asserts are used to use static analysis to find bugs in your code. They should never fail
        assert(token_balance[_from] + token_balance[_to] == previousBalances);
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

    /**
     * Transfer tokens from other address
     *
     * Send `_value` tokens to `_to` in behalf of `_from`
     *
     * @param _from The address of the sender
     * @param _to The address of the recipient
     * @param _value the amount to send
     */
    function transfer_token_from(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);     // Check allowance
        allowance[_from][msg.sender] -= _value;
        _transfer_token(_from, _to, _value);
        return true;
    }

    /**
     * Set allowance for other address
     *
     * Allows `_spender` to spend no more than `_value` tokens in your behalf
     *
     * @param _spender The address authorized to spend
     * @param _value the max amount they can spend
     */
    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        return true;
    }

    /**
     * Set allowance for other address and notify
     *
     * Allows `_spender` to spend no more than `_value` tokens in your behalf, and then ping the contract about it
     *
     * @param _spender The address authorized to spend
     * @param _value the max amount they can spend
     * @param _extraData some extra information to send to the approved contract
     */
     /*
    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }
    */

    /**
     * Destroy tokens
     *
     * Remove `_value` tokens from the system irreversibly
     *
     * @param _value the amount of money to burn
     */
    function burn(uint256 _value) public returns (bool success) {
        require(token_balance[msg.sender] >= _value);   // Check if the sender has enough
        token_balance[msg.sender] -= _value;            // Subtract from the sender
        totalSupply -= _value;                      // Updates totalSupply
        Burn(msg.sender, _value);
        return true;
    }

    /**
     * Destroy tokens from other account
     *
     * Remove `_value` tokens from the system irreversibly on behalf of `_from`.
     *
     * @param _from the address of the sender
     * @param _value the amount of money to burn
     */
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(token_balance[_from] >= _value);                // Check if the targeted balance is enough
        require(_value <= allowance[_from][msg.sender]);    // Check allowance
        token_balance[_from] -= _value;                         // Subtract from the targeted balance
        allowance[_from][msg.sender] -= _value;             // Subtract from the sender's allowance
        totalSupply -= _value;                              // Update totalSupply
        Burn(_from, _value);
        return true;
    }
}

/******************************************/
/*       ADVANCED TOKEN STARTS HERE       */
/******************************************/

contract NFOCoin is owned, TokenERC20 {

    //uint256 public sellPrice;
    //uint256 public buyPrice;
    uint master_exchange_rate;
    string[5] greetings;

    mapping (address => bool) public frozenAccount;

    /* This generates a public event on the blockchain that will notify clients */
    event FrozenFunds(address target, bool frozen);
    
    struct NFOTransactionObject {
        
        uint pvn_to_eth_token_amt;
        uint eth_to_pvn_token_amt;
        address eth_addr;
        address pvn_addr;
        uint exchange_rate;
        uint timestamp;
        bytes32 hash;
        bool isTx;
    }
    
    mapping (bytes32 => NFOTransactionObject) nfoTransactions;
    bytes32[] public nfoTransactionList;

    function is_transaction(bytes32 _transaction_hash) public constant returns (bool isIndeed) {
        return nfoTransactions[_transaction_hash].isTx;
    }
    
    function get_transaction_count() public constant returns (uint transactionCount) {
        return nfoTransactionList.length;
    }
    
    function get_eth_balance(address eth_addr) public constant returns (uint balance) {
        return eth_balance[eth_addr];
    }
    
    function get_token_balance(address eth_addr) public constant returns (uint balance) {
        return token_balance[eth_addr];
    }
    
    function get_pvn_token_balance(address pvn_addr) public constant returns (uint balance) {
        
        return pvn_token_balance[pvn_addr];
    }
    
    function make_hash(uint _pvn_to_eth_token_amt, uint _eth_to_pvn_token_amt, address _eth_addr, 
        address _pvn_addr, uint _exchange_rate, uint _timestamp) constant public returns (bytes32 hash) {
        
        hash = sha3(_pvn_to_eth_token_amt, _eth_to_pvn_token_amt, _eth_addr, _pvn_addr, block.timestamp, _exchange_rate, _timestamp);

    }
    
   /**
     * Moves tokens across networks
     *
     * Moves tokens between `_token_balance` (tokens on main net)
     * 
     * and `_pvn_token_balance` (tokens on private net) 
     *
     * @param _pvn_to_eth_token_amt number of tokens to move from private net
     * to main net 
     * @param _eth_to_pvn_token_amt number of tokens to move from main net
     * to private net 
     * @param _eth_addr main net Ethereum address
     * @param _pvn_addr private net Ethereum address 
     */    
    function nfo_transaction(uint _pvn_to_eth_token_amt, uint _eth_to_pvn_token_amt, address _eth_addr,
        address _pvn_addr, bytes32 _hash) public returns (uint rowNumber) {
            if (_hash !=0 ) {
                if(is_transaction(_hash)) revert();
            }
            
            _hash = make_hash(_pvn_to_eth_token_amt, _eth_to_pvn_token_amt, _eth_addr, _pvn_addr, master_exchange_rate, block.timestamp);
            
            if(is_transaction(_hash)) revert();
            require( _pvn_to_eth_token_amt * _eth_to_pvn_token_amt ==0 );
            require( _pvn_to_eth_token_amt >0 || _eth_to_pvn_token_amt >0);
            require( _eth_addr != 0x0 );
            require( _pvn_addr != 0x0 );
            
            // sending token from main net to private net 
            if (_eth_to_pvn_token_amt > 0 && _pvn_to_eth_token_amt==0 ) {

                _eth_addr = msg.sender;   // you can only transfer your own tokens
                
                require( token_balance[_eth_addr] - _eth_to_pvn_token_amt >0 );
                token_balance[_eth_addr] -= _eth_to_pvn_token_amt;
                pvn_token_balance[_pvn_addr] += _eth_to_pvn_token_amt;
            }
            
            // sending token from private net to main net   
            if ( _pvn_to_eth_token_amt > 0 && _eth_to_pvn_token_amt == 0) {
            
                _pvn_addr = msg.sender;  // you can only transfer your own tokens
                
                require( pvn_token_balance[_pvn_addr] - _pvn_to_eth_token_amt > 0);
                token_balance[_eth_addr] += _pvn_to_eth_token_amt;
                pvn_token_balance[_pvn_addr] -= _pvn_to_eth_token_amt;
            }
            nfoTransactions[_hash] = NFOTransactionObject({
                pvn_to_eth_token_amt: _pvn_to_eth_token_amt,
                eth_to_pvn_token_amt: _eth_to_pvn_token_amt,
                eth_addr: _eth_addr,
                pvn_addr: _pvn_addr,
                exchange_rate: master_exchange_rate,
                timestamp: block.timestamp,
                hash: _hash,
                isTx: true
            });
            
            return nfoTransactionList.push(_hash)-1;
        
        }
        
    /* Initializes contract with initial supply tokens to the creator of the contract */
    function NFOCoin(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) TokenERC20(initialSupply, tokenName, tokenSymbol) public payable  {
        
        master_exchange_rate = 1000;                        // 1 ETH = 1000 CC 
        greetings[0] = "Hi, my name is Omar Metwally.";
        greetings[1] = "I am the creator of this contract.";
        greetings[2] = "Black Swan Lives!";
        greetings[3] = "Watching Parnassus on a beautiful, sunny day in SF...";
        greetings[4] = "Healthcare is a human right.";        
    }

    /* Internal transfer, only can be called by this contract */
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);                               // Prevent transfer to 0x0 address. Use burn() instead
        require (token_balance[_from] >= _value);               // Check if the sender has enough
        require (token_balance[_to] + _value > token_balance[_to]); // Check for overflows
        require(!frozenAccount[_from]);                     // Check if sender is frozen
        require(!frozenAccount[_to]);                       // Check if recipient is frozen
        token_balance[_from] -= _value;                         // Subtract from the sender
        token_balance[_to] += _value;                           // Add the same to the recipient
        Transfer(_from, _to, _value);
    }

    /// @notice Create `mintedAmount` tokens and send it to `target`
    /// @param target Address to receive the tokens
    /// @param mintedAmount the amount of tokens it will receive
    function mintToken(address target, uint256 mintedAmount) onlyOwner public {
        token_balance[target] += mintedAmount;
        totalSupply += mintedAmount;
        Transfer(0, this, mintedAmount);
        Transfer(this, target, mintedAmount);
    }

    /// @notice `freeze? Prevent | Allow` `target` from sending & receiving tokens
    /// @param target Address to be frozen
    /// @param freeze either to freeze it or not
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }

    /// @notice Allow users to buy tokens for `newBuyPrice` eth and sell tokens for `newSellPrice` eth
    /// @param newSellPrice Price the users can sell to the contract
    /// @param newBuyPrice Price users can buy from the contract
    /*
    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) onlyOwner public {
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }
    */

    /// @notice Buy tokens from contract by sending ether
    function buy() payable public {
        uint amount = msg.value * master_exchange_rate;  // buyPrice;              // calculates the amount
        _transfer(owner, msg.sender, amount);                                // makes the transfers
        eth_balance[msg.sender] += msg.value;                               // update eth_balance 
        token_balance[msg.sender] += amount;  // update token_balance
    }

    /// @notice Sell `amount` tokens to contract
    /// @param amount amount of tokens to be sold
    function sell(uint256 amount) public {
        require(this.balance >= (amount / master_exchange_rate) );      // checks if the contract has enough ether to buy
        _transfer(msg.sender, owner, amount);              // makes the transfers
        msg.sender.transfer(amount / master_exchange_rate);          // sends ether to the seller. It's important to do this last to avoid recursion attacks
        token_balance[msg.sender] -= amount;   // update token_balance
        eth_balance[msg.sender] -= (amount/master_exchange_rate) ;   // update eth_balance
    }
    
    /* Generates a random number from 0 to 10 based on the last block hash */
    function randomGen(uint seed) public constant returns (uint randomNumber) {
        return(uint(sha3(block.blockhash(block.number-1), seed ))%10);
    }

    function get_transaction_by_row(uint row) public constant returns (uint pvn_to_eth_token_amt, uint eth_to_pvn_token_amt, address eth_addr, address pvn_addr, uint exchange_rate, uint timestamp, bytes32 hash) {

       require(row<nfoTransactionList.length);
       require(row>=0);

       pvn_to_eth_token_amt=nfoTransactions[nfoTransactionList[row]].pvn_to_eth_token_amt;
       eth_to_pvn_token_amt=nfoTransactions[nfoTransactionList[row]].eth_to_pvn_token_amt;
       eth_addr=nfoTransactions[nfoTransactionList[row]].eth_addr;
       pvn_addr=nfoTransactions[nfoTransactionList[row]].pvn_addr;
       exchange_rate=nfoTransactions[nfoTransactionList[row]].exchange_rate;
       timestamp=nfoTransactions[nfoTransactionList[row]].timestamp;
       hash=nfoTransactions[nfoTransactionList[row]].hash;
    }
    
    function set_master_exchange_rate(uint new_rate) public  returns (uint exchange_rate) {
        require(msg.sender == owner);
        master_exchange_rate = new_rate;
        return master_exchange_rate;
    }    
    function greet_omar(uint _i) public constant returns (string greeting) {
        require(_i>=0);
        require(_i<greetings.length);
        return greetings[_i];
    }    
}


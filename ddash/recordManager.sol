pragma solidity ^0.4.11;

contract RecordManager {

    struct Record {
        uint id;
        bool initialized;
        bool is_public;
        string ipfs_hash;
        string shared_by_fingerprint;
    }

    event RecordCreated (
        uint _id,
        bool _is_public,
        string _ipfs_hash,
        string _shared_by_fingerprint
    );

    mapping(string => Record) records;
    uint num_records;
    address public owner;

    function RecordManager() {
        owner = msg.sender;
        num_records = 0;
    }

    /**
     * Function to create a new record.
     *
     * Returns 0 if successful, 1 if a record with the ipfs_hash already exists.
     */
    function new_record(uint _id, bool _is_public, string _ipfs_hash, 
            string _shared_by_fingerprint) public returns (uint) {
        if (records[_ipfs_hash].initialized) {
            // Return 1 on duplicate
            return 1;
        }
        records[_ipfs_hash] = Record({
            id: _id,
            initialized: true,
            is_public: _is_public,
            ipfs_hash: _ipfs_hash,
            shared_by_fingerprint: _shared_by_fingerprint
        });
        
        // Emit event: record created.
        RecordCreated(_id, _is_public, _ipfs_hash, _shared_by_fingerprint);
        // Return 0 on success
        return 0;
    }

    function get_record(string _ipfs_hash) public 
            returns (uint _id, string _ipfs_hash, string _shared_by_fingerprint) {
        Record record = records[_ipfs_hash];
        if (!record.initialized) {
            // Record doesn't exist.
            return 1;
        }
        _id = record.id;
        _ipfs_hash = record.ipfs_hash;
        _shared_by_fingerprint = record.shared_by_fingerprint;

        return (_id, _ipfs_hash, _shared_by_fingerprint);
    }

}
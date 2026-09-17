// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract HoneyTrace {
    address public owner;
    struct Batch { string batchId; bytes32 dataHash; uint256 createdAt; bool active; }
    mapping(string => Batch) private batches;
    event BatchRegistered(string indexed batchId, bytes32 dataHash, uint256 createdAt);
    event BatchUpdated(string indexed batchId, bytes32 dataHash, uint256 updatedAt);

    constructor(){ owner=msg.sender; }
    modifier onlyOwner(){ require(msg.sender==owner,"Not authorized"); _; }

    function registerBatch(string calldata id, bytes32 dataHash) external onlyOwner {
        require(bytes(batches[id].batchId).length==0,"Batch exists");
        batches[id]=Batch(id,dataHash,block.timestamp,true);
        emit BatchRegistered(id,dataHash,block.timestamp);
    }
    function updateBatchHash(string calldata id, bytes32 dataHash) external onlyOwner {
        require(batches[id].active,"Unknown batch");
        batches[id].dataHash=dataHash;
        emit BatchUpdated(id,dataHash,block.timestamp);
    }
    function verifyBatch(string calldata id) external view returns(bytes32,uint256,bool){
        Batch memory b=batches[id]; return(b.dataHash,b.createdAt,b.active);
    }
}
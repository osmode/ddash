var contract_abi=web3.eth.contract([{"constant":false,"inputs":[{"name":"entityAddress","type":"address"},{"name":"enode","type":"string"}],"name":"update_entity","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"get_entity_count","outputs":[{"name":"entityCount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"entityList","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"seed","type":"uint256"}],"name":"randomGen","outputs":[{"name":"randomNumber","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"entityStructs","outputs":[{"name":"enode","type":"string"},{"name":"isEntity","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"enode","type":"string"}],"name":"add_entity","outputs":[{"name":"rowNumber","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"entityAddress","type":"address"},{"name":"enode","type":"string"}],"name":"new_entity","outputs":[{"name":"rowNumber","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"entityAddress","type":"address"}],"name":"is_entity","outputs":[{"name":"isIndeed","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"row","type":"uint256"}],"name":"get_enode_by_row","outputs":[{"name":"_enode","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"sender_enode","outputs":[{"name":"_enode","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_i","type":"uint256"}],"name":"greet_omar","outputs":[{"name":"greeting","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":true,"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"addr","type":"address"},{"indexed":false,"name":"enode","type":"string"}],"name":"NewEntity","type":"event"}]);

var contract_obj = contract_abi.new(
{
from: web3.eth.accounts[0],
data: '0x606060405233600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506040805190810160405280601d81526020017f48692c206d79206e616d65206973204f6d6172204d657477616c6c792e000000815250600360006005811015156200008c57fe5b019080519060200190620000a29291906200026e565b50606060405190810160405280602281526020017f4920616d207468652063726561746f72206f66207468697320636f6e7472616381526020017f742e000000000000000000000000000000000000000000000000000000000000815250600360016005811015156200011157fe5b019080519060200190620001279291906200026e565b506040805190810160405280601181526020017f426c61636b205377616e204c6976657321000000000000000000000000000000815250600360026005811015156200016f57fe5b019080519060200190620001859291906200026e565b50606060405190810160405280603581526020017f5761746368696e67205061726e6173737573206f6e206120626561757469667581526020017f6c2c2073756e6e792064617920696e2053462e2e2e0000000000000000000000815250600380600581101515620001f357fe5b019080519060200190620002099291906200026e565b506040805190810160405280601c81526020017f4865616c74686361726520697320612068756d616e2072696768742e00000000815250600360046005811015156200025157fe5b019080519060200190620002679291906200026e565b506200031d565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f10620002b157805160ff1916838001178555620002e2565b82800160010185558215620002e2579182015b82811115620002e1578251825591602001919060010190620002c4565b5b509050620002f19190620002f5565b5090565b6200031a91905b8082111562000316576000816000905550600101620002fc565b5090565b90565b610d3e806200032d6000396000f3006060604052600436106100ba576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063084bbafb146100bf5780630c646fbd14610153578063404cbffb1461017c578063434b14e7146101df5780634dd448bf14610216578063710f3953146102f05780638da5cb5b14610361578063927db81f146103b65780639c8615ac14610446578063d1a6945514610497578063d82beb9e14610533578063f4b96570146105c1575b600080fd5b34156100ca57600080fd5b610139600480803573ffffffffffffffffffffffffffffffffffffffff1690602001909190803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509190505061065d565b604051808215151515815260200191505060405180910390f35b341561015e57600080fd5b6101666106d3565b6040518082815260200191505060405180910390f35b341561018757600080fd5b61019d60048080359060200190919050506106e0565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34156101ea57600080fd5b610200600480803590602001909190505061071f565b6040518082815260200191505060405180910390f35b341561022157600080fd5b61024d600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091905050610762565b6040518080602001831515151581526020018281038252848181546001816001161561010002031660029004815260200191508054600181600116156101000203166002900480156102e05780601f106102b5576101008083540402835291602001916102e0565b820191906000526020600020905b8154815290600101906020018083116102c357829003601f168201915b5050935050505060405180910390f35b34156102fb57600080fd5b61034b600480803590602001908201803590602001908080601f01602080910402602001604051908101604052809392919081815260200183838082843782019150505050505091905050610792565b6040518082815260200191505060405180910390f35b341561036c57600080fd5b6103746107c3565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34156103c157600080fd5b610430600480803573ffffffffffffffffffffffffffffffffffffffff1690602001909190803590602001908201803590602001908080601f016020809104026020016040519081016040528093929190818152602001838380828437820191505050505050919050506107e9565b6040518082815260200191505060405180910390f35b341561045157600080fd5b61047d600480803573ffffffffffffffffffffffffffffffffffffffff16906020019091905050610907565b604051808215151515815260200191505060405180910390f35b34156104a257600080fd5b6104b86004808035906020019091905050610911565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156104f85780820151818401526020810190506104dd565b50505050905090810190601f1680156105255780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b341561053e57600080fd5b610546610a34565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561058657808201518184015260208101905061056b565b50505050905090810190601f1680156105b35780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34156105cc57600080fd5b6105e26004808035906020019091905050610b56565b6040518080602001828103825283818151815260200191508051906020019080838360005b83811015610622578082015181840152602081019050610607565b50505050905090810190601f16801561064f5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b600061066883610907565b151561067357600080fd5b816000808573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060000190805190602001906106c8929190610c2d565b506001905092915050565b6000600180549050905090565b6001818154811015156106ef57fe5b90600052602060002090016000915054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000600a6001430340836040518083600019166000191681526020018281526020019250505060405180910390206001900481151561075a57fe5b069050919050565b600060205280600052604060002060009150905080600001908060010160009054906101000a900460ff16905082565b600061079d33610907565b156107b2576107ac338361065d565b506107be565b6107bc33836107e9565b505b919050565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000816000808573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000019080519060200190610840929190610c2d565b5060016000808573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060010160006101000a81548160ff02191690831515021790555060018080548060010182816108b09190610cad565b9160005260206000209001600086909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555003905092915050565b6000809050919050565b610919610cd9565b60008060018481548110151561092b57fe5b906000526020600020900160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000018054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610a285780601f106109fd57610100808354040283529160200191610a28565b820191906000526020600020905b815481529060010190602001808311610a0b57829003601f168201915b50505050509050919050565b610a3c610cd9565b60008060016000815481101515610a4f57fe5b906000526020600020900160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000206000018054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610b4c5780601f10610b2157610100808354040283529160200191610b4c565b820191906000526020600020905b815481529060010190602001808311610b2f57829003601f168201915b5050505050905090565b610b5e610cd9565b60008210151515610b6e57600080fd5b600582101515610b7d57600080fd5b600382600581101515610b8c57fe5b018054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610c215780601f10610bf657610100808354040283529160200191610c21565b820191906000526020600020905b815481529060010190602001808311610c0457829003601f168201915b50505050509050919050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f10610c6e57805160ff1916838001178555610c9c565b82800160010185558215610c9c579182015b82811115610c9b578251825591602001919060010190610c80565b5b509050610ca99190610ced565b5090565b815481835581811511610cd457818360005260206000209182019101610cd39190610ced565b5b505050565b602060405190810160405280600081525090565b610d0f91905b80821115610d0b576000816000905550600101610cf3565b5090565b905600a165627a7a7230582052bf62828b42d2d5b7b438d8405b09cfa11b69f7c291c829628e87374e4b255e0029',
gas: '2000000'
}, function (e, contract) {
console.log(e, contract);
if (typeof contract.address !== 'undefined') {
console.log('Contract mined! address: ' + contract.address + ' transactionHash: ' + contract.transactionHash);
}
})

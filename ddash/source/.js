var contract_abi=web3.eth.contract()

var contract_obj = contract_abi.new(
{
from: web3.eth.accounts[0],
data: '',
gas: '100000'
}, function (e, contract) {
if (typeof contract.address !== 'undefined') {
}
})

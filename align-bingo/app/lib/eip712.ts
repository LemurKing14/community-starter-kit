export const domain = (chainId:number, verifyingContract:string)=>({
  name:"AlignCardNFT", version:"1", chainId, verifyingContract
});
export const types = {
  AlignCard: [
    { name:"wallet",  type:"address" },
    { name:"tokenId", type:"uint256" },
    { name:"seed",    type:"bytes32" },
    { name:"gameId",  type:"uint256" }
  ]
};
export const truncateSig = (sig:string)=> `${sig.slice(0,10)}…${sig.slice(-8)}`;

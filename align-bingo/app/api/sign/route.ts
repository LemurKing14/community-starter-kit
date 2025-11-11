import { NextRequest, NextResponse } from "next/server";
import { Wallet } from "ethers";

export async function POST(req: NextRequest){
  const { wallet, tokenId, seed, gameId, verifyingContract, chainId } = await req.json();
  const signerKey = process.env.SIGNER_KEY!;
  const signer = new Wallet(signerKey);

  const domain = { name:"AlignCardNFT", version:"1", chainId, verifyingContract };
  const types = { AlignCard: [
    { name:"wallet", type:"address" },
    { name:"tokenId", type:"uint256" },
    { name:"seed", type:"bytes32" },
    { name:"gameId", type:"uint256" }
  ]};
  const value = { wallet, tokenId, seed, gameId };

  const signature = await signer.signTypedData(domain as any, types as any, value);
  return NextResponse.json({ signature });
}

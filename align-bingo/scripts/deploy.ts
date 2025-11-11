import { ethers } from "hardhat";

async function main() {
  const signerAddr = process.env.NEXT_PUBLIC_SIGNER!;
  const C = await ethers.getContractFactory("AlignCardNFT");
  const c = await C.deploy(signerAddr);
  await c.deployed();
  console.log("AlignCardNFT:", c.address);
  if (process.env.GAME_ID) {
    const tx = await c.setGame(Number(process.env.GAME_ID));
    await tx.wait();
  }
}
main().catch((e)=>{ console.error(e); process.exit(1); });

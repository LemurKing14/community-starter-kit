import { keccak256, toBeHex } from "ethers";
export class VerifiableCaller {
  private secret: `0x${string}`; private remaining:number[]; private step=0;
  constructor(secretHex: `0x${string}`){ this.secret = secretHex; this.remaining = Array.from({length:75},(_,i)=>i+1); }
  commitHash(){ return keccak256(this.secret); }
  draw(): number | null {
    if (!this.remaining.length) return null;
    const seed = keccak256((this.secret + toBeHex(this.step).slice(2).padStart(2,'0')) as `0x${string}`);
    this.step++;
    const idx = Number(BigInt(seed) % BigInt(this.remaining.length));
    const [n] = this.remaining.splice(idx,1);
    return n;
  }
}
